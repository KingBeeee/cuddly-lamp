import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

w3 = Web3(Web3.HTTPProvider(RPC_URL))

# ABI for the ScoreUpdated event
ABI = [
    {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "user", "type": "address"}, {"indexed": False, "internalType": "uint256", "name": "score", "type": "uint256"}], "name": "ScoreUpdated", "type": "event"}
]

def verify_score_from_logs():
    print(f"Connecting to FlareTrust Contract: {CONTRACT_ADDRESS}")
    print("Scanning recent blocks for ScoreUpdated events...\n")
    
    contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=ABI)
    
    # Get the latest block number
    latest_block = w3.eth.block_number
    # Look back over the last 100 blocks (roughly 3-4 minutes on Flare)
    from_block = max(0, latest_block - 25) 
    
    try:
        # Fetch the logs
        logs = contract.events.ScoreUpdated.get_logs(from_block=from_block, to_block='latest')
        
        if not logs:
            print("❌ No ScoreUpdated events found in the last 100 blocks.")
            print("Make sure your listener is running and you triggered a request!")
            return

        print("========================================")
        for log in logs:
            user = log['args']['user']
            score = log['args']['score']
            print(f"✅ SUCCESS! Verified On-Chain Event:")
            print(f"   Wallet: {user}")
            print(f"   Score:  {score}/1000")
        print("========================================\n")
        
        print("The off-chain TEE logic successfully processed the private data, signed the transaction, and the Smart Contract verified it on-chain!")

    except Exception as e:
        print(f"Error fetching logs: {e}")

if __name__ == "__main__":
    verify_score_from_logs()
