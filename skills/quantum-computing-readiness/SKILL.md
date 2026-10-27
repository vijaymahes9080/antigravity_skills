---
name: quantum-computing-readiness
description: Post-Quantum Cryptography (PQC) migration, NIST PQC standards (FIPS 203 ML-KEM/Kyber, FIPS 204 ML-DSA/Dilithium, FIPS 205 SLH-DSA/SPHINCS+), cryptographic inventory scanning, hybrid classical-quantum TLS, and harvest-now-decrypt-later defense.
---

# Quantum Computing Readiness & Post-Quantum Cryptography (PQC)

## 1. Intended Role & Domain
- **Primary Domain**: Cybersecurity, Privacy & Gov.
- **Target Roles**: Post-Quantum Cryptography Specialist, Cryptographic Security Architect, Infrastructure Security Engineer
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "post-quantum cryptography", "pqc migration", "fips 203", "fips 204", "fips 205", "ml-kem", "kyber", "ml-dsa", "dilithium", "sphincs+", "hybrid tls", "harvest now decrypt later", "quantum resistance".
- **Contextual Inferences**: Upgrading cryptographic algorithms before RSA/ECC vulnerability to Shor's algorithm, establishing cryptographic inventory, implementing hybrid key exchange.
- **Chained Predecessors**: `appsec-owasp-audit`, `cybersecurity-sast-vulnerability-scan`, `cloud-security-hardening`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Performing routine frontend UI styling without cryptographic implications.
  - Writing simple web application database queries.

## 4. Required Inputs & Context
- Cryptographic inventory (TLS certificates, SSH keys, VPN configurations, database encryption at rest).
- Target systems: API gateways, microservices, secure communication channels.
- Target standards: NIST Post-Quantum Cryptography Standards (FIPS 203 ML-KEM, FIPS 204 ML-DSA, FIPS 205 SLH-DSA).

## 5. Expected Outputs & Artifacts
- Cryptographic Bill of Materials (CBOM) inventory identifying quantum-vulnerable algorithms (RSA, ECDSA, ECDH).
- Hybrid TLS 1.3 configuration (X25519 + ML-KEM-768).
- Migration roadmap (`pqc_migration_plan.md`) prioritizing high-retention data vulnerable to "Harvest Now, Decrypt Later" (HNDL) attacks.
- Automated scanning script (`cbom_scanner.py`) asserting quantum-safe crypto agility.

## 6. Step-by-Step Operating Procedure
1. **Cryptographic Bill of Materials (CBOM) Discovery**:
   - Scan codebases and infrastructure for vulnerable primitives: RSA keys (< 3072-bit), ECC curves (secp256r1, secp256k1), DH/ECDH.
2. **Threat Prioritization (Harvest Now, Decrypt Later)**:
   - Identify data with secrecy lifespans > 5-10 years (health records, financial contracts, government telemetry).
3. **Hybrid Key Encapsulation (ML-KEM / Kyber)**:
   - Configure TLS 1.3 endpoints to utilize hybrid key exchange (combining classical X25519 with post-quantum ML-KEM-768).
4. **Digital Signature Migration (ML-DSA & SLH-DSA)**:
   - Prepare transition plans for software code signing, PKI root certificates, and document signing to ML-DSA (Dilithium).
5. **Crypto Agility Architecture**:
   - Abstract cryptographic operations behind modular interfaces so algorithms can be swapped without rewriting business logic.

## 7. Repository Inspection & Planning Requirements
- Non-destructive inspection of certificates and cryptographic configurations:
  ```bash
  grep -rnE "(RSA|ECDSA|ECDH|secp256k1|crypto/tls|OpenSSL)" . 2>/dev/null
  ```
- Preservation rule: Always implement hybrid classical/quantum algorithms during migration to guarantee safety against implementation defects.

## 8. Tool & Dependency Requirements
- OpenSSL 3.3+ with liboqs (Open Quantum Safe), BoringSSL, Python `oqs` bindings, Go 1.24+ (with native ML-KEM support).

## 9. Implementation Guidelines & Best Practices
- Python post-quantum hybrid key encapsulation and cryptographic agility wrapper:

```python
from typing import Tuple, Dict
import os
import hashlib

class QuantumSafeKEM:
    # Simulated Cryptographic Agility wrapper for NIST FIPS 203 (ML-KEM-768).
    # In production environments, binds to liboqs (Open Quantum Safe library).
    def __init__(self, algorithm: str = "ML-KEM-768"):
        self.algorithm = algorithm
        self.classical_supported = "X25519"

    def generate_hybrid_keypair(self) -> Dict[str, bytes]:
        # Generate classical seed and quantum seed
        classical_priv = os.urandom(32)
        classical_pub = hashlib.sha256(b"classical:" + classical_priv).digest()
        
        quantum_priv = os.urandom(64)
        quantum_pub = hashlib.sha3_256(b"pqc_ml_kem_768:" + quantum_priv).digest()
        
        return {
            "public_key": classical_pub + quantum_pub,
            "private_key": classical_priv + quantum_priv
        }

    def encapsulate_shared_secret(self, hybrid_public_key: bytes) -> Tuple[bytes, bytes]:
        classical_pub = hybrid_public_key[:32]
        quantum_pub = hybrid_public_key[32:]
        
        # Ephemeral shared secret derivation
        ephemeral = os.urandom(32)
        ciphertext = hashlib.sha256(b"kem_ciphertext:" + ephemeral + quantum_pub).digest()
        shared_secret = hashlib.sha3_256(ephemeral + classical_pub).digest()
        
        return ciphertext, shared_secret

# Example verification
if __name__ == "__main__":
    pqc = QuantumSafeKEM("ML-KEM-768")
    keys = pqc.generate_hybrid_keypair()
    ciphertext, secret = pqc.encapsulate_shared_secret(keys["public_key"])
    print(f"Algorithm: {pqc.algorithm} + {pqc.classical_supported}")
    print(f"Hybrid Public Key Length: {len(keys['public_key'])} bytes")
    print(f"Shared Secret Derived: {secret.hex()[:32]}...")
```

## 10. Error Handling & Recovery Procedures
- Packet fragmentation from larger PQC key sizes: ML-KEM-768 public keys are ~1,184 bytes (vs classical ECC 32 bytes). Ensure MTU sizes and TCP windowing accommodate larger TLS ClientHello packets.
- Hardware accelerator incompatibility: Ensure software fallbacks are available if AVX-512 or specialized vector extensions are absent.

## 11. Security & Privacy Constraints
- Never rely exclusively on pure post-quantum algorithms without classical hybrid pairing until NIST FIPS production hardening matures across all vendors.

## 12. Verification & Testing Requirements
- Verify TLS handshakes succeed with hybrid `X25519MLKEM768` cipher suites.
- Cryptographic inventory scanner accurately identifies 100% of legacy RSA/ECC keys in the repository.

## 13. Completion Criteria
- Complete Cryptographic Bill of Materials (CBOM) generated.
- Hybrid quantum-classical TLS 1.3 configured on public ingress endpoints.
- PQC migration roadmap published with risk prioritization.

## 14. Relevant Official References
- NIST FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism (ML-KEM).
- NIST FIPS 204: Module-Lattice-Based Digital Signature Algorithm (ML-DSA).
- NIST FIPS 205: Stateless Hash-Based Digital Signature Algorithm (SLH-DSA).
- CISA / NSA / NIST Quantum-Readiness Roadmap.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with OpenSSL 3.x, liboqs, and IETF hybrid TLS 1.3 draft standards.
