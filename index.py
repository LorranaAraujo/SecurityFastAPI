from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.controller import tarefa_controller, auth_controller

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tarefa_controller.routes,
                   prefix=tarefa_controller.prefix)

app.include_router(auth_controller.routes,
                   prefix=auth_controller.prefix)