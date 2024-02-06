import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints.qubo import router as qubo_router
from app.endpoints.ui import router as ui_router


DESCRIPTION: str = """
Job deployment and registration API @ QuCUN platform
"""

app = FastAPI(
    title="Job deployment API @ QuCUN platform",
    description=DESCRIPTION,
    version=os.getenv("VERSION", "0.0.1"),
    debug=True,
)

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
def configure_api_routing() -> None:
    """Attaches every route for the API to the FastAPI instance."""
    app.include_router(qubo_router)
    app.include_router(ui_router)


if __name__ == "__main__":
    uvicorn.run(app, port=8004)  # noqa
