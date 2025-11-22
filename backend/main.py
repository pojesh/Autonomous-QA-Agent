from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.core.config import get_settings
from backend.core.logging import logger

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    docs_url=f"{settings.API_PREFIX}/docs",
    openapi_url=f"{settings.API_PREFIX}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow Streamlit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "details": str(exc)},
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}

# Import and include routers 
from backend.api.routers import ingestion, generation, session
app.include_router(ingestion.router, prefix=f"{settings.API_PREFIX}/ingestion", tags=["Ingestion"])
app.include_router(generation.router, prefix=f"{settings.API_PREFIX}/generation", tags=["Generation"])
app.include_router(session.router, prefix=f"{settings.API_PREFIX}/session", tags=["Session"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
