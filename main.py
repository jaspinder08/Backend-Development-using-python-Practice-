import uvicorn
from fastapi import FastAPI
import models
from database import engine
from routers import post, user, auth, votes

# from config import settings
from fastapi.middleware.cors import CORSMiddleware


# Here we are telling passlin that we want to use bcrypt algorithm
# models.Base.metadata.create_all(bind=engine)

# print(settings.access_token_expire_minutes)
# app = FastAPI(
#     title="Api Setup Demo ",
#     description="Api for my project",
#     version="0.0.1",
#     contact={"name": "jassi", "email": "jaspinderkaurjk08@gmail.com"},
# )

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(votes.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
