import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from compute import run_enclave_pipeline

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
        print(f"[API] Request received for wallet: {wallet}. Routing directly to TEE...")

        # The API server passes ONLY the wallet identifier.
        # The TEE handles fetching, scoring, and signing entirely inside its boundary.
        score = run_enclave_pipeline(wallet)

        return {
            "status": "success",
            "wallet": wallet,
            "score": score,
            "message": "Enclave successfully fetched data, calculated score, and signed on-chain!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
