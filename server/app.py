from openenv.core.env_server import create_fastapi_app
from .environment import DBAEnvironment
from models import DBAction, DBObservation

app = create_fastapi_app(DBAEnvironment, DBAction, DBObservation)