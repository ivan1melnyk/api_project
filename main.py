from typing import List
from src.repository import contact as repository_contact
from src.schemas import ContactResponse
from src.database.db import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, status, Query, FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from src.routes import contact, auth, users

from src.conf.config import settings
from fastapi_limiter import FastAPILimiter
import redis


app = FastAPI()

origins = [
    "http://localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix='/api')
app.include_router(contact.router, prefix='/api')
app.include_router(users.router, prefix='/api')


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/birthdays", response_model=list[ContactResponse], name='Get list of contacts with birthdays for the next 7 days')
async def get_birthdays(skip: int = 0, limit: int = Query(default=10), db: Session = Depends(get_db)):
    contacts = await repository_contact.get_contacts_birthdays(skip, limit, db)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Contacts with birthdays for the next 7 days not found")
    return contacts


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
