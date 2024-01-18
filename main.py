from fastapi import FastAPI
from views import configure_routes

app = FastAPI()

configure_routes(app)