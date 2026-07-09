import os
import time
from dotenv import load_dotenv
from web3 import Web3
from compute import fetch_mock_web2_data, calculate_credit_score, sign_and_return_onchain

load_dotenv()
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

w3 = Web3(Web3.HTTPProvider(RPC_URL))

CONTRACT_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "user", "type": "address"}
        ],
        "name": "ScoreRequested",
        "type": "event"
    }
]

# Set memory to remember transactions we've already processed
processed_txs = set()

def handle_event(event):
    tx_hash = event['transactionHash'].hex()
    
    # If we already did this one, ignore it
    if tx_hash in processed_txs:
        return
        
    # Mark as processed
    processed_txs.add(tx_hash)
    
    user_wallet = event['args']['user']
    print(f"\n[LISTENER] 🚨 Detected ScoreRequested event for: {user_wallet}", flush=True)
    try:
        raw_data = fetch_mock_web2_data(user_wallet)
        score = calculate_credit_score(raw_data)
        sign_and_return_onchain(user_wallet, score)
    except Exception as e:
        print(f"[TEE ERROR] Failed during compute/signing: {e}", flush=True)

def main():
    print("[LISTENER] Booting up overlapping block-polling...", flush=True)
    contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)
    
    print(f"[LISTENER] Monitoring contract {CONTRACT_ADDRESS}...", flush=True)
    
    while True:
        try:
            current_block = w3.eth.block_number
            # Always look back 10 blocks to conquer RPC lag!
            from_block = max(0, current_block - 10)
            
            logs = contract.events.ScoreRequested.get_logs(from_block=from_block, to_block=current_block)
            for log in logs:
                handle_event(log)
            
            time.sleep(3) # Rest for 3 seconds
        except Exception as e:
            print(f"[POLL ERROR] {e}", flush=True)
            time.sleep(5)

if __name__ == "__main__":
    main()
