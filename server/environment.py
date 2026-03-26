import random
import uuid
from openenv.core.env_server import Environment
from models import DBAction, DBObservation, DBState

class DBAEnvironment(Environment):
    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self):
        self._state = DBState()
        self.task = {}
        self.current_indexes = []
        self.cost = 0.0

    def reset(self, seed=None, episode_id=None, **kwargs) -> DBObservation:
       
        tasks = [
            {
                "level": "easy",
                "query": "SELECT * FROM users WHERE email = 'test@example.com'",
                "schema": {"users": ["id", "name", "email"]},
                "initial_cost": 500.0,
                "solution": ("users", "email")
            },
            {
                "level": "medium",
                "query": "SELECT * FROM orders JOIN users ON orders.user_id = users.id",
                "schema": {"users": ["id", "name"], "orders": ["id", "user_id", "total"]},
                "initial_cost": 1500.0,
                "solution": ("orders", "user_id")
            },
            {
                "level": "hard",
                "query": "SELECT * FROM logs WHERE status = 'ERROR' AND date = 'today'",
                "schema": {"logs": ["id", "status", "date", "message"]},
                "initial_cost": 3000.0,
                "solution": ("logs", "status_date") # Composite index needed
            }
        ]
        
        self.task = random.choice(tasks)
        self.current_indexes = []
        self.cost = self.task["initial_cost"]
        
        self._state = DBState(
            episode_id=episode_id or str(uuid.uuid4()),
            step_count=0,
            max_steps=5
        )
        
        return DBObservation(
            done=False,
            reward=0.0,
            task_level=self.task["level"],
            query=self.task["query"],
            schema_info=self.task["schema"],
            current_indexes=self.current_indexes,
            execution_cost=self.cost,
            message="New DB optimization task started. Create indexes to lower execution cost."
        )

    def step(self, action: DBAction, timeout_s=None, **kwargs) -> DBObservation:
        self._state.step_count += 1
        message = ""
        reward = 0.0
        done = False

        index_name = f"idx_{action.table_name}_{action.column_name}"

        # Action Logic
        if action.action_type == "CREATE_INDEX":
            if index_name not in self.current_indexes:
                self.current_indexes.append(index_name)
                
                # Check if it's the correct solution
                if (action.table_name, action.column_name) == self.task["solution"]:
                    self.cost = self.cost * 0.1 # Cost drops by 90%!
                    reward = 0.5 # Partial reward for taking good step
                    message = "Optimal index created! Cost dropped drastically."
                else:
                    self.cost = self.cost * 0.95 # Slight drop, but mostly useless
                    reward = -0.1 # Penalty for wasting storage
                    message = "Inefficient index created. Wasting storage."
            else:
                reward = -0.2
                message = "Index already exists!"

        elif action.action_type == "DROP_INDEX":
            if index_name in self.current_indexes:
                self.current_indexes.remove(index_name)
                message = f"Dropped {index_name}"
            else:
                message = "Index does not exist."

        elif action.action_type == "SUBMIT":
            # Grader Logic (End of episode)
            done = True
            if self.cost <= (self.task["initial_cost"] * 0.15):
                reward = 1.0 # Perfect Score!
                message = "Task Complete: Database is optimized!"
            else:
                reward = 0.0 # Failed to optimize enough
                message = "Task Failed: Execution cost is still too high."

        # Check Step Limit
        if self._state.step_count >= self._state.max_steps and not done:
            done = True
            reward = -1.0
            message = "Max steps reached. DBA Agent fired!"

        return DBObservation(
            done=done,
            reward=reward,
            task_level=self.task["level"],
            query=self.task["query"],
            schema_info=self.task["schema"],
            current_indexes=self.current_indexes,
            execution_cost=self.cost,
            message=message
        )

    @property
    def state(self) -> DBState:
        return self._state