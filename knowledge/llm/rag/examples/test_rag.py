import importlib.util
from io import BytesIO
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("rag", Path(__file__).with_name("rag.py"))
rag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rag)

class RetrievalContracts(unittest.TestCase):
    def test_exclusions_rebuild_and_query_quoting(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ["kubernetes/auth.md", "sources/incoming/raw.md", "sources/processed/old.md", "work/note.md", "templates/sample.md"]:
                p = root/name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("# Identity\n\n## PeerAuthentication\n\nMesh mutual TLS.\n", encoding="utf-8")
            db = root/"index.sqlite"
            first = rag.ingest(root, db)
            hits = rag.search(db, "PeerAuthentication")["hits"]
            self.assertEqual({h["path"] for h in hits}, {"kubernetes/auth.md"})
            self.assertTrue(any(h["anchor"] == "peerauthentication" for h in hits))
            self.assertEqual(rag.ask(db, "zzzxmissingtopic987")["answer"], "NO_EVIDENCE")
            self.assertEqual(rag.search(db, '" OR 1=1 -- zzzxmissingtopic987')["hits"], [])
            self.assertEqual(first, rag.ingest(root, db))
            (root/"kubernetes/auth.md").unlink()
            rag.ingest(root, db)
            self.assertEqual(rag.search(db, "PeerAuthentication")["hits"], [])

    def test_citations_and_code_headings(self):
        rag.validate_citations("Supported claim [1]", 1)
        for answer in ["Uncited claim", "Invented evidence [2]", "Bad evidence [0]"]:
            with self.assertRaises(ValueError):
                rag.validate_citations(answer, 1)
        parts = list(rag.sections("# Topic\n```bash\n# code comment\n```\n## Detail\nEvidence\n"))
        self.assertEqual([p[1] for p in parts], ["Topic", "Detail"])

    def test_source_lifecycle_is_preserved_and_deprecated_is_excluded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "kubernetes").mkdir()
            draft = "---\nstatus: draft\nmaturity: draft\n---\n# Current\n\nLifecycleProbe evidence.\n"
            deprecated = "---\nstatus: deprecated\nmaturity: deprecated\n---\n# Old\n\nLifecycleProbe old recipe.\n"
            (root / "kubernetes/current.md").write_text(draft, encoding="utf-8")
            (root / "kubernetes/old.md").write_text(deprecated, encoding="utf-8")
            database = root / "index.sqlite"
            rag.ingest(root, database)
            hits = rag.search(database, "LifecycleProbe")["hits"]
            self.assertEqual({h["path"] for h in hits}, {"kubernetes/current.md"})
            self.assertEqual(hits[0]["status"], "draft")
            self.assertEqual(hits[0]["maturity"], "draft")

    def test_real_corpus_golden_questions(self):
        root = Path(__file__).resolve().parents[3]
        with tempfile.TemporaryDirectory() as directory:
            db = Path(directory)/"index.sqlite"
            rag.ingest(root, db)
            questions = [
                ("PeerAuthentication", "knowledge/kubernetes/applications-and-tools/istio/"),
                ("BM25", "knowledge/llm/rag/"),
                ("ExternalSecret", "knowledge/kubernetes/applications-and-tools/platform-tooling/"),
                ("dyff", "knowledge/kubernetes/applications-and-tools/manifest-validation/"),
                ("AssumeRoleWithWebIdentity", "knowledge/cloud/aws/security/irsa-"),
                ("ResourceGraphDefinition", "knowledge/kubernetes/applications-and-tools/kro/"),
                ("PEM", "knowledge/kubernetes/observability/"),
                ("CDK", "knowledge/cloud/aws/cdk/"),
                ("watermark", "knowledge/databases/data-aggregation.md"),
                ("Ona", "knowledge/devops/development-environments/"),
            ]
            for question, prefix in questions:
                with self.subTest(question=question):
                    hits = rag.search(db, question)["hits"]
                    self.assertTrue(any(h["path"].startswith(prefix) for h in hits))
            self.assertLessEqual(rag.search(db, "IRSA")["context_characters"], 12000)

    def test_optional_generation_protocol_and_no_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "kubernetes").mkdir()
            (root / "kubernetes/auth.md").write_text("# Identity\n\nIRSA uses OIDC.\n", encoding="utf-8")
            database = root / "index.sqlite"
            rag.ingest(root, database)
            response = BytesIO(json.dumps({"message": {"content": "IRSA uses OIDC [1]"}}).encode())
            with patch.object(rag.urllib.request, "urlopen", return_value=response) as call:
                result = rag.ask(database, "IRSA", model="synthetic-test-model")
                self.assertTrue(result["generated"])
                payload = json.loads(call.call_args.args[0].data)
                self.assertFalse(payload["stream"])
                self.assertIn("kubernetes/auth.md#identity", payload["messages"][1]["content"])
            with patch.object(rag.urllib.request, "urlopen") as call:
                self.assertEqual(rag.ask(database, "zzzxmissingtopic987", model="unused")["answer"], "NO_EVIDENCE")
                call.assert_not_called()
            response = BytesIO(json.dumps({"message": {"content": "Invented source [99]"}}).encode())
            with patch.object(rag.urllib.request, "urlopen", return_value=response):
                with self.assertRaises(ValueError):
                    rag.ask(database, "IRSA", model="synthetic-test-model")

if __name__ == "__main__":
    unittest.main()
