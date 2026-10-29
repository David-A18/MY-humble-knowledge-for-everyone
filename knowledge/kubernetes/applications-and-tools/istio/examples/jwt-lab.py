"""Generate synthetic, one-hour JWT fixtures; private key remains in memory."""
import base64
import json
from pathlib import Path
import sys
import time
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes

def b64(value):
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode()

def integer(value):
    return b64(value.to_bytes((value.bit_length() + 7) // 8, "big"))

def generate(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public = key.public_key().public_numbers()
    jwks = {"keys": [{"kty": "RSA", "kid": "lab", "use": "sig", "alg": "RS256",
                      "n": integer(public.n), "e": integer(public.e)}]}
    now = int(time.time())
    header = b64(json.dumps({"alg": "RS256", "kid": "lab", "typ": "JWT"}).encode())
    claims = b64(json.dumps({"iss": "https://issuer.example.test", "aud": "demo",
                             "sub": "student", "iat": now, "exp": now + 3600}).encode())
    unsigned = (header + "." + claims).encode()
    signature = key.sign(unsigned, padding.PKCS1v15(), hashes.SHA256())
    token = unsigned.decode() + "." + b64(signature)
    def policy(kind, name, spec):
        return {"apiVersion": "security.istio.io/v1", "kind": kind,
                "metadata": {"name": name, "namespace": "istio-lab"}, "spec": spec}
    selector = {"matchLabels": {"app": "web"}}
    policies = [
        policy("PeerAuthentication", "strict", {"mtls": {"mode": "STRICT"}}),
        policy("RequestAuthentication", "jwt", {"selector": selector, "jwtRules": [
            {"issuer": "https://issuer.example.test", "audiences": ["demo"],
             "jwks": json.dumps(jwks)}]}),
        policy("AuthorizationPolicy", "allow-client-with-jwt", {"selector": selector,
            "action": "ALLOW", "rules": [{"from": [{"source": {
                "principals": ["cluster.local/ns/istio-lab/sa/allowed"],
                "requestPrincipals": ["*"]}}]}]})]
    (output / "policies.json").write_text(json.dumps({"apiVersion": "v1", "kind": "List",
                                                      "items": policies}, indent=2) + "\n")
    (output / "token.txt").write_text(token + "\n")
    return token, jwks

if __name__ == "__main__":
    generate(sys.argv[1])
    print("Created public-key policies and a disposable token; no private key was saved.")
