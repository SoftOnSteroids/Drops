from fastapi import FastAPI
from v1.routers import droppers, doses, calendar

app = FastAPI()

# Routers
app.include_router(droppers.router)
app.include_router(doses.router)
app.include_router(calendar.router)

@app.get("/")
async def root():
    return "API v1"
