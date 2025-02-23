from fastapi import FastAPI
from api.gemini_routes import router as gemini_router

# Initialize FastAPI app
app = FastAPI()

# Include routes
app.include_router(gemini_router)

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to SafeCRASH Disaster Detection API"}

# Run FastAPI Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)