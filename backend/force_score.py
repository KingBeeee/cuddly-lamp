import os
from dotenv import load_dotenv
from web3 import Web3
from compute import fetch_mock_web2_data, calculate_credit_score, sign_and_return_onchain

load_dotenv()
w3 = Web3()
account = w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))

print("\n--- INITIATING MANUAL TEE PIPELINE ---")
print(f"Target Wallet: {account.address}")

# 1. Fetch
raw_data = fetch_mock_web2_data(account.address)
# 2. Compute
score = calculate_credit_score(raw_data)
# 3. Sign & Submit
sign_and_return_onchain(account.address, score)
