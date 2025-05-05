from fastapi import FastAPI
from routers import usuarios

app = FastAPI()

app.include_router(usuarios.router)
app.include_router(usuarios.test)
