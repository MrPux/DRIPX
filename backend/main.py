from fastapi import FastAPI
from api.disaster_routes import router as disaster_router
from api.gemini_routes import router as gemini_router

# Initialize FastAPI app
app = FastAPI()

# Include routes
app.include_router(disaster_router)
app.include_router(gemini_router)

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Disaster Recovery API"}

# Run FastAPI Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)