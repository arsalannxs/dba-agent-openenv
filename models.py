from typing import List, Dict
from openenv.core.env_server import Action, Observation, State

class DBAction(Action):
    """Agent kya karega?"""
    action_type: str  
    table_name: str
    column_name: str

class DBObservation(Observation):
    """Agent kya dekhega? (Note: done aur reward by default inherit hote hain)"""
    task_level: str         
    query: str                
    schema_info: Dict[str, List[str]] 
    current_indexes: List[str] 
    execution_cost: float   
    message: str             

class DBState(State):
    """Background Episode Info"""
    max_steps: int = 5