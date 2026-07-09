import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

# Minimal ABI just for the request function
ABI = [
    {"inputs": [], "name": "requestCreditScore", "outputs": [], "stateMutability": "nonpayable", "type": "function"}
]

def simulate_user_request():
    print(f"Simulating User Wallet: {account.address}")
    print(f"Connecting to FlareTrust Contract: {CONTRACT_ADDRESS}")
    
    contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=ABI)
    
    print("\n[USER] Requesting a confidential credit score computation...")
    
    # Build the transaction with explicit Chain ID and Gas to bypass estimation RPC errors
    tx = contract.functions.requestCreditScore().build_transaction({
        'chainId': 114,
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 500000,
        'gasPrice': w3.eth.gas_price
    })
    
    # Sign and send
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    print(f"[USER] Transaction sent! Hash: {tx_hash.hex()}")
    print("Waiting for transaction to be mined...\n")
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print("[USER] Transaction confirmed on Coston2! The event has been emitted.")

if __name__ == "__main__":
    simulate_user_request()
