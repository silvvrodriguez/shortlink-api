import secrets
import string

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session

from app.database import Base, engine, SessionLocal
from app.models.link import Link


app = FastAPI(
    title="ShortLink API",
    version="1.0.0"
)


Base.metadata.create_all(bind=engine)


class LinkCreate(BaseModel):
    url: HttpUrl


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def generate_short_code(length: int = 6):
    characters = string.ascii_letters + string.digits

    return "".join(
        secrets.choice(characters)
        for _ in range(length)
    )


def generate_unique_short_code(
    db: Session,
    length: int = 6,
    max_attempts: int = 5
):
    for _ in range(max_attempts):
        short_code = generate_short_code(length)

        existing_link = (
            db.query(Link)
            .filter(Link.short_code == short_code)
            .first()
        )

        if existing_link is None:
            return short_code

    raise HTTPException(
        status_code=500,
        detail="Could not generate a unique short code"
    )


@app.get("/")
def root():
    return {
        "message": "ShortLink API is running"
    }


@app.post("/links")
def create_link(
    link: LinkCreate,
    db: Session = Depends(get_db)
):
    short_code = generate_unique_short_code(db)

    new_link = Link(
        original_url=str(link.url),
        short_code=short_code
    )

    db.add(new_link)
    db.commit()
    db.refresh(new_link)

    return {
        "id": new_link.id,
        "original_url": new_link.original_url,
        "short_code": new_link.short_code,
        "short_url": f"http://127.0.0.1:8000/{new_link.short_code}",
        "created_at": new_link.created_at
    }


@app.get("/{short_code}")
def redirect_link(
    short_code: str,
    db: Session = Depends(get_db)
):
    link = (
        db.query(Link)
        .filter(Link.short_code == short_code)
        .first()
    )

    if link is None:
        raise HTTPException(
            status_code=404,
            detail="Short link not found"
        )

    return RedirectResponse(url=link.original_url)