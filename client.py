from openenv.core.env_client import EnvClient
from openenv.core.client_types import StepResult
from models import DBAction, DBObservation, DBState

class DBAAgentEnv(EnvClient[DBAction, DBObservation, DBState]):
    def _step_payload(self, action: DBAction) -> dict:
        return {
            "action_type": action.action_type, 
            "table_name": action.table_name, 
            "column_name": action.column_name
        }

    def _parse_result(self, payload: dict) -> StepResult:
        obs_data = payload.get("observation", {})
        return StepResult(
            observation=DBObservation(**obs_data),
            reward=payload.get("reward"),
            done=payload.get("done", False),
        )

    def _parse_state(self, payload: dict) -> DBState:
        return DBState(**payload)