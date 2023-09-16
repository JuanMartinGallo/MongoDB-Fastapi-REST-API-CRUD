from fastapi import FastAPI
from routes.users_routes import user
from docs import tags_metadata

app = FastAPI(
    title="REST API CRUD with FastAPI and MongoDB",
    description="This is a simple REST API using FastAPI and MongoDB",
    version="0.0.2",
    openapi_tags=tags_metadata,
)

app.include_router(user)
