from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from router import ping, find_places

# Initialize FastAPI
app = FastAPI(
    title="Places Scraper API",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(CORSMiddleware)

# Redirect root to docs
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")


# Include routers
app.include_router(ping.router)
app.include_router(find_places.router)
