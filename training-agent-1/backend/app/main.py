from fastapi import FastAPI
from routes.training_routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Python Training Agent")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(router)

@app.get("/")
def root():
    return {"message": "AI Python Trainer Running"}