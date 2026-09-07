import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import DateTime, String, Text, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.exc import SQLAlchemyError

BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:shreyas@localhost/postgres",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


class Base(DeclarativeBase):
    pass


class Wish(Base):
    __tablename__ = "wishes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))
    message: Mapped[str] = mapped_column(Text())
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class WishCreate(BaseModel):
    name: str = Field(min_length=1, max_length=60)
    message: str = Field(min_length=1, max_length=280)


app = FastAPI(title="For your favorite human")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

DEMO_WISHES = [
    {"name": "The universe", "message": "Keep taking up space. You make every room more alive."},
    {"name": "Future you", "message": "More brave choices, slow mornings, and wildly good surprises."},
]


@app.on_event("startup")
def create_tables() -> None:
    try:
        Base.metadata.create_all(engine)
    except SQLAlchemyError:
        pass


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    html = (BASE_DIR / "templates" / "index.html").read_text(encoding="utf-8")
    return HTMLResponse(html)


@app.get("/api/wishes")
def get_wishes() -> list[dict[str, str]]:
    try:
        with Session(engine) as session:
            wishes = session.scalars(select(Wish).order_by(Wish.created_at.desc()).limit(12)).all()
            return [{"name": wish.name, "message": wish.message} for wish in wishes]
    except SQLAlchemyError:
        return DEMO_WISHES


@app.post("/api/wishes", status_code=201)
def create_wish(payload: WishCreate) -> dict[str, str]:
    try:
        with Session(engine) as session:
            wish = Wish(name=payload.name.strip(), message=payload.message.strip())
            session.add(wish)
            session.commit()
            return {"name": wish.name, "message": wish.message}
    except SQLAlchemyError as error:
        raise HTTPException(status_code=503, detail="The wish book is resting. Try again in a moment.") from error
