from fastapi import FastAPI

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../shared/', 'models'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../shared/', 'schemas'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../shared/', 'db'))
sys.path.append(os.path.join(os.path.dirname(__file__), '', 'routes'))

from db_setup import engine
import activities_routes
import activity_models
from fastapi.middleware.cors import CORSMiddleware

activity_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Strava API",
    version="0.0.1",
    contact={
        "name": "Matheus Vasconcellos",
        "email": "matheus@example.com",
    }
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(activities_routes.router)

