from fastapi.routing import APIRouter
from fastapi_users import FastAPIUsers

from workspacesio import database, schemas
from workspacesio.depends import fastapi_users, get_db

from . import crud
from . import models as deriv_models
from . import schemas as deriv_schemas

router = APIRouter()
tags = ["derivatives"]
