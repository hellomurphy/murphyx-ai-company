"""
MurphyX control API — FastAPI entry (scaffold).

Routers mounted from api.routes — all stubs until implementation.
"""

from fastapi import FastAPI

from api.routes import ROUTERS

app = FastAPI(title="MurphyX Control API", version="0.0.0-scaffold")

for router in ROUTERS:
    app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
