import hashlib
import json
from datetime import datetime


def hash_file(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


attestation = {
    "model_hash": hash_file("models/model_card.md"),
    "policy_hash": hash_file("guardrails/policy_engine_rules.yaml"),
    "timestamp": datetime.utcnow().isoformat()
}

with open("attest/deploy_attestation.json", "w") as f:
    json.dump(attestation, f, indent=2)

print("Attestation generated.")
