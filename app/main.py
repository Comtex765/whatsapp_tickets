from os import getenv

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.transferencia import router as transferencia_router
from routes.webhook import router as webhook_router

# Esto hace que después de cada print, se reinicie el color
ENV = getenv("ENV")

IS_PROD = ENV == "production"


API_TITLE = "Webhook WhatsApp"
API_VERSION = "1.0.0"

PORT = int(getenv("PORT"))


# URLs de documentación
DOCS_URL = None if IS_PROD else "/docs"
REDOC_URL = None if IS_PROD else "/redoc"
OPENAPI_URL = None if IS_PROD else "/openapi.json"


app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    docs_url=DOCS_URL,
    redoc_url=REDOC_URL,
    openapi_url=OPENAPI_URL,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite cualquier método (GET, POST, etc.)
    allow_headers=["*"],  # Permite cualquier encabezado
)


# Agregar rutas
app.include_router(webhook_router)
app.include_router(transferencia_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
