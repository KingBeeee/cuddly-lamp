import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Pre-compiled ABI matching our Solidity contract
ABI = [
    {"inputs": [], "stateMutability": "nonpayable", "type": "constructor"},
    {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "user", "type": "address"}, {"indexed": False, "internalType": "uint256", "name": "score", "type": "uint256"}], "name": "ScoreUpdated", "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "user", "type": "address"}], "name": "ScoreRequested", "type": "event"},
    {"inputs": [{"internalType": "address", "name": "", "type": "address"}], "name": "creditScores", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "requestCreditScore", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "_user", "type": "address"}, {"internalType": "uint256", "name": "_score", "type": "uint256"}], "name": "submitCreditScore", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [], "name": "teeAddress", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}
]

# Pre-compiled Bytecode for our exact FlareTrust contract
BYTECODE = "0x608060405234801561001057600080fd5b50336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506102378061005f6000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c90816315aa44bc146100465780633b47bf5a14610076578063a92542ff14610091575b600080fd5b610074600480360381019061005f9190610141565b6100bc565b005b61007e61018d565b60405161008891906101b3565b60405180910390f35b6100ba60048036038101906100b191906101ca565b610101565b005b3373ffffffffffffffffffffffffffffffffffffffff166000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614610140576040517f08c379a000000000000000000000000000000000000000000000000000000000805260040161013790610207565b60405180910390fd5b600181111561015357600080fd5b81600160008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825962005060201c60201c31145355508273ffffffffffffffffffffffffffffffffffffffff167f53de2b47e8e50b717b01d7e2311756578a506117cfbd92eb65851efb5a8e0cb28160405161019c91906101b3565b60405180910390a25050565b600060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b3373ffffffffffffffffffffffffffffffffffffffff167f62e6e3cdae02bbdf141eb8703713028fb46db09b936d88ff593ff68377bead3e60405160405180910390a256"

def deploy():
    if PRIVATE_KEY == "your_testnet_private_key_here" or not PRIVATE_KEY:
        print("[ERROR] Please set a valid PRIVATE_KEY in your .env file first!")
        return

    account = w3.eth.account.from_key(PRIVATE_KEY)
    print(f"Deploying from account: {account.address}")
    
    # Check balance to ensure you have testnet funds
    balance = w3.eth.get_balance(account.address)
    print(f"Account Balance: {w3.from_wei(balance, 'ether')} CFLR")
    
    if balance == 0:
        print("[ERROR] You need Coston2 testnet tokens (CFLR) to deploy! Get some from the Flare Faucet.")
        return

    print("Broadcasting deployment transaction to Coston2...")
    
    # Build transaction
    FlareTrustContract = w3.eth.contract(abi=ABI, bytecode=BYTECODE)
    tx = FlareTrustContract.constructor().build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gasPrice': w3.eth.gas_price
    })
    
    # Sign transaction
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    
    # Send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Transaction sent! Hash: {tx_hash.hex()}")
    
    # Wait for receipt
    print("Waiting for transaction to be mined...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    print(f"\n[SUCCESS] Contract deployed successfully!")
    print(f"Deployed Address: {tx_receipt.contractAddress}")
    print("\n👉 Copy this Deployed Address and update your .env file!")

if __name__ == "__main__":
    deploy()
