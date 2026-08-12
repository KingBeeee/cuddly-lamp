# 🚀 FlareTrust: Confidential Off-Chain Credit Scoring for DeFi

FlareTrust bridges the gap between traditional Web2 financial credit histories and Web3 DeFi lending. Built for the Flare network, it allows users to unlock under-collateralized loans (e.g., FAsset borrowing) by verifying their credit score using a Trusted Execution Environment (TEE) without ever exposing their raw private data on-chain.

## 💡 The Problem & Solution
* **The Problem:** Current DeFi lending requires massive over-collateralization because protocols cannot trust or verify off-chain creditworthiness without breaking user privacy or exposing sensitive financial APIs.
* **The Solution:** FlareTrust shifts data ingestion entirely inside an off-chain secure enclave pipeline. The host application handles zero personal identity parameters, while the enclave securely fetches encrypted banking metrics, computes a standardized risk profile in protected memory, and signs cryptographic attestations directly to the blockchain.

## 📸 Interface Preview

### 1. Request Stage (Initial State)
<p align="center">
  <img src="frontend/Picture1.png" width="550" alt="FlareTrust Initial Connection Screen">
</p>

### 2. Confidential Execution & Verified Outcome
<p align="center">
  <img src="frontend/Picture2.png" width="550" alt="FlareTrust Successful Pipeline Run">
</p>

---

## 🛡️ Secure TEE Architecture Flow

To ensure zero-knowledge data exposure and absolute privacy, the Web2 data orchestrator has been isolated into a strict Trusted Execution Environment (TEE) boundary:

1. **Host API Isolation:** The client frontend hits the public FastAPI backend passing *only* the user's `wallet_address`. The external host server never sees, fetches, or processes any financial metadata locally.
2. **Secure Enclave Ingestion:** The backend triggers the isolated TEE Enclave pipeline. The enclave connects directly to the off-chain banking API over a secure, TLS-encrypted connection to pull raw scoring inputs.
3. **In-Memory Computation:** Credit scoring models evaluate raw profile parameters exclusively inside the protected enclave memory registers. All raw inputs are completely flushed as soon as the baseline score is produced.
4. **On-Chain Cryptographic Attestation:** The enclave uses its private key variables to assemble, sign, and broadcast the transaction via the `submitCreditScore` function directly to the Coston2 Testnet—ensuring the external backend host cannot modify or intercept the credit scores.

---

## 🏗️ Technical Stack & Live Deployments

* **Blockchain:** Flare Coston2 Testnet
* **Smart Contract Address:** `0x1E06535c70594CAB7a701f5F3447cD0b264DC0a5`
* **Backend Stack:** Python 3.12, Web3.py, FastAPI, Uvicorn
* **Frontend Stack:** Clean Semantic HTML5, CSS3 Grid/Flexbox, Ethers.js (v5)

---

## 🏃‍♂️ How to Run Locally

### 1. Backend Setup
```bash
cd flaretrust-backend
source venv/bin/activate
pip install -r backend/requirements.txt
python backend/server.py
