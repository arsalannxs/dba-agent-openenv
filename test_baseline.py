import random
from client import DBAAgentEnv
from models import DBAction

def get_dummy_action(observation, step_count):
    """Ek simple Bot jo bina kisi API ke environment ko test karega"""
    
    
    if step_count >= 3:
        return DBAction(action_type="SUBMIT", table_name="", column_name="")
    
    
    tables = list(observation.schema_info.keys())
    chosen_table = random.choice(tables)
    chosen_column = random.choice(observation.schema_info[chosen_table])
    
   
    return DBAction(
        action_type="CREATE_INDEX", 
        table_name=chosen_table, 
        column_name=chosen_column
    )

def run_baseline():
    print("Connecting to DBA Environment (Local Mode)...")
    
   
    with DBAAgentEnv(base_url="http://127.0.0.1:8000").sync() as env:
        
        
        for i in range(3):
            print(f"\n--- Episode {i+1} ---")
            result = env.reset()
            print(f"Task Level: {result.observation.task_level}")
            print(f"Starting Cost: {result.observation.execution_cost} ms")
            
            step_count = 0
            while not result.done:
                
                action = get_dummy_action(result.observation, step_count)
                
                if action.action_type == "SUBMIT":
                    print("Bot Action: SUBMITTING RESOLUTION")
                else:
                    print(f"Bot Action: {action.action_type} on {action.table_name}.{action.column_name}")
                
            
                result = env.step(action)
                print(f"Feedback: {result.observation.message} | Current Cost: {result.observation.execution_cost} ms")
                
                step_count += 1
            
            print(f"Final Reward for Episode: {result.reward}")

if __name__ == "__main__":
    run_baseline()