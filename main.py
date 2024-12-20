import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import cluster
from services.cluster import load_startup
load_dotenv(dotenv_path=".env")
        
version = os.getenv("VERSION")
app = FastAPI(openapi_url="")

@app.on_event("startup")
async def startup():
    await load_startup()

    
# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(cluster.router, prefix="/api/" + version)
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8001)))
