from fastapi import FastAPI
from v1.routers import droppers, doses

app = FastAPI()

# Routers
app.include_router(droppers.router)
app.include_router(doses.router)

@app.get("/")
async def root():
    return "API v1"

# Iniciar el server: uvicorn main:app --reload
# Detener el server: CTRL+C

# Iniciar MongoDB: brew services start mongodb-community
# Detener MongoDB: brew services stop mongodb-community

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc