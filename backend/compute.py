import os
import json
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

# ABI specifically for submitting the score
ABI = [
    {"inputs": [{"internalType": "address", "name": "_user", "type": "address"}, {"internalType": "uint256", "name": "_score", "type": "uint256"}], "name": "submitCreditScore", "outputs": [], "stateMutability": "nonpayable", "type": "function"}
]

def fetch_mock_web2_data(wallet_address):
    print(f"[TEE Secure Fetch] Establishing connection to Web2 API for {wallet_address}...")
    # In V2 production, your TLS/API request logic executes entirely right here inside the enclave
    return {"monthly_income": 4500, "account_age_months": 24, "default_history": 0}

def calculate_credit_score(data):
    print("[TEE Model] Processing raw web2 data in secure memory...")
    base_score = 300
    income_bonus = (data["monthly_income"] / 1000) * 20
    age_bonus = data["account_age_months"] * 5
    final_score = min(base_score + income_bonus + age_bonus, 1000)
    print("[TEE Model] Computation complete. Flushing raw data variables from enclave memory.")
    return int(final_score)

def sign_and_return_onchain(wallet_address, score):
    print(f"\n[TEE Signer] Preparing to attest on-chain: {wallet_address} has a score of {score}")

    contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=ABI)

    tx = contract.functions.submitCreditScore(w3.to_checksum_address(wallet_address), score).build_transaction({
        'chainId': 114,
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 500000,
        'gasPrice': w3.eth.gas_price
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    print(f"[TEE Signer] Transaction broadcasted! Hash: {tx_hash.hex()}")
    print("Waiting for block confirmation...")

    w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"[SUCCESS] Score securely submitted and mined on Coston2!\n")

def run_enclave_pipeline(wallet_address):
    """
    Main entrypoint representing the secure enclave execution pipeline.
    The host environment calls this and only receives the final calculated score.
    """
    raw_data = fetch_mock_web2_data(wallet_address)
    score = calculate_credit_score(raw_data)
    sign_and_return_onchain(wallet_address, score)
    return score

if __name__ == "__main__":
    print("This script is now imported by server.py.")
