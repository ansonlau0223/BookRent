from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import auth, books, rentals, reservations

app = FastAPI(
    title="BookRent API",
    version="0.1.0"
)


app.include_router(books.router)
app.include_router(auth.router)
app.include_router(rentals.router)
app.include_router(reservations.router)


@app.get("/health")
def health():
    return {
        "status": "ok"
    }

app.mount(
    "/",
    StaticFiles(
        directory="frontend",
        html=True
    ),
    name="frontend"
)