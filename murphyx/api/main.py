"""
MurphyX control API — FastAPI entry point.
Part of framework; lives under murphyx/api per repo layout.
"""

from fastapi import FastAPI

from murphyx.api.routes import ROUTERS

app = FastAPI(title="MurphyX Control API", version="0.1.0")

for router in ROUTERS:
    app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
