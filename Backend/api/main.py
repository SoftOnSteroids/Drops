from fastapi import FastAPI
from v1.routers import droppers, doses

app = FastAPI()

# Routers
app.include_router(droppers.router)
app.include_router(doses.router)

@app.get("/")
async def root():
    return "API v1"
