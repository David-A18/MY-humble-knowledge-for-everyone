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

    def test_every_catalog_concept_is_indexed_or_deliberately_excluded(self):
        root = Path(__file__).resolve().parents[4]
        catalog = json.loads((root / "generated/knowledge-catalog.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory)/"index.sqlite"
            rag.ingest(root, database)
            with rag.closing(rag.sqlite3.connect(database)) as db:
                indexed = {row[0] for row in db.execute("SELECT path FROM concepts")}
        excluded = {"knowledge/templates/", "/".join(("knowledge", *rag.EXAMPLE_BUNDLE)) + "/"}
        missing = [c["path"] for c in catalog["concepts"]
                   if c["path"] not in indexed and not c["path"].startswith(tuple(excluded))]
        self.assertEqual(missing, [])

    def test_okf_trust_metadata(self):
        header = "---\ntype: Reference\ntitle: T\ndescription: Long text\n  continued.\ntags:\n- a\n- b\n{extra}---\n# T\n"
        self.assertEqual(rag.metadata(header.format(extra=""))["trust_tier"], "unverified")
        self.assertEqual(rag.metadata(header.format(extra=""))["description"], "Long text continued.")
        self.assertEqual(rag.metadata(header.format(extra=""))["tags"], ["a", "b"])
        machine = "verified:\n- { by: process:nightly, at: 2026-06-26T02:00:00Z }\n"
        self.assertEqual(rag.metadata(header.format(extra=machine))["trust_tier"], "machine-confirmed")
        human = "verified: { by: human:ana, at: 2026-06-25T09:00:00Z }\n"
        self.assertEqual(rag.metadata(header.format(extra=human))["trust_tier"], "human-reviewed")
        sources = "sources:\n  - id: one\n    resource: https://example.invalid\n  - id: two\n    resource: x\n"
        self.assertEqual(rag.metadata(header.format(extra=sources))["source_ids"], ["one", "two"])
        self.assertTrue(rag.is_stale("2026-10-08", rag.date(2026, 10, 8)))
        self.assertFalse(rag.is_stale("2026-10-08T00:00:00Z", rag.date(2026, 10, 7)))
        self.assertFalse(rag.is_stale(""))

    def test_sections_split_on_paragraphs_and_keep_code_whole(self):
        code = "```bash\n" + "\n\n".join(f"echo {n}" for n in range(30)) + "\n```"
        parts = rag.split_body("Intro paragraph.\n\n" + code + "\n\n" + "Word " * 400, limit=300)
        self.assertTrue(any(code in part for part in parts))
        self.assertEqual(rag.split_body("   \n\n  "), [])

    def test_weak_evidence_is_refused_without_calling_the_model(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "kubernetes").mkdir()
            (root / "kubernetes/pods.md").write_text("# Pods\n\nPods restart after probes fail.\n", encoding="utf-8")
            database = root / "index.sqlite"
            rag.ingest(root, database)
            weak = rag.search(database, "pods quantum entanglement photosynthesis")
            self.assertTrue(weak["hits"])
            self.assertFalse(weak["sufficient"])
            with patch.object(rag.urllib.request, "urlopen") as call:
                self.assertEqual(rag.ask(database, "pods quantum entanglement photosynthesis", model="unused")["answer"], "NO_EVIDENCE")
                call.assert_not_called()

    def test_uncited_paragraphs_are_counted_but_not_fatal(self):
        answer = "First claim [1].\n\nA second paragraph without any citation at all."
        rag.validate_citations(answer, 1)
        self.assertEqual(rag.uncited_paragraphs(answer), 1)
        self.assertEqual(rag.uncited_paragraphs("First claim [1].\n\nThird claim [2]."), 0)

    def test_model_reasoning_is_removed_before_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "kubernetes").mkdir()
            (root / "kubernetes/auth.md").write_text("# Identity\n\nIRSA uses OIDC.\n", encoding="utf-8")
            database = root / "index.sqlite"
            rag.ingest(root, database)
            reply = "Let me think about this at some length.\n</think>\n\nIRSA uses OIDC [1]."
            response = BytesIO(json.dumps({"message": {"content": reply}}).encode())
            with patch.object(rag.urllib.request, "urlopen", return_value=response):
                self.assertEqual(rag.ask(database, "IRSA", model="synthetic-test-model")["answer"], "IRSA uses OIDC [1].")
            response = BytesIO(json.dumps({"message": {"content": "NO_EVIDENCE\n\nThe excerpts do not cover this."}}).encode())
            with patch.object(rag.urllib.request, "urlopen", return_value=response):
                self.assertEqual(rag.ask(database, "IRSA", model="synthetic-test-model")["answer"], "NO_EVIDENCE")

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
