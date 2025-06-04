from fastapi import FastAPI
from routers import usuarios, quadras, agendamentos, ping
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv() 
FRONTEND_URL = os.getenv("FRONTEND_URL") 

app = FastAPI()

origins = [
    FRONTEND_URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,
    allow_methods=["*"],       
    allow_headers=["*"],
)

app.include_router(usuarios.router)
app.include_router(usuarios.routerUser)
app.include_router(quadras.router)
app.include_router(agendamentos.router)
app.include_router(ping.router)

