import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from compute import fetch_mock_web2_data, calculate_credit_score, sign_and_return_onchain

load_dotenv()

app = FastAPI()

# Allow your frontend to talk to your backend safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestModel(BaseModel):
    wallet_address: str

@app.post("/api/calculate-score")
async def trigger_pipeline(data: RequestModel):
    try:
        wallet = data.wallet_address
        print(f"[API] Received request for wallet: {wallet}")
        
        # Run the complete TEE pipeline we engineered!
        raw_data = fetch_mock_web2_data(wallet)
        score = calculate_credit_score(raw_data)
        sign_and_return_onchain(wallet, score)
        
        return {
            "status": "success",
            "wallet": wallet,
            "score": score,
            "message": "Score successfully computed by TEE and signed on-chain!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
