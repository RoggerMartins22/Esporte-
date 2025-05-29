from fastapi import FastAPI
from routers import usuarios, quadras, agendamentos
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173", 
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
