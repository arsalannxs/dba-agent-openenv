# DBA Agent Environment (OpenEnv)

## Environment Description & Motivation
Database optimization is a critical real-world engineering task. In modern cloud architectures, slow SQL queries cost companies millions in compute resources. 
This OpenEnv environment simulates a **Database Administrator (DBA)** scenario. The AI agent is given a slow-running SQL query, the database schema, and the current execution cost. The agent's goal is to analyze the query and create the optimal database index to drastically reduce the execution cost.

## Observation & Action Space
- **Observation Space (`DBObservation`)**: 
  - `task_level`: Difficulty of the task (easy, medium, hard).
  - `query`: The slow SQL query.
  - `schema_info`: Available tables and columns.
  - `current_indexes`: List of active indexes.
  - `execution_cost`: Current simulated cost in ms.
  - `message`: System feedback.
- **Action Space (`DBAction`)**: 
  - `action_type`: Can be "CREATE_INDEX", "DROP_INDEX", or "SUBMIT".
  - `table_name`: Target table.
  - `column_name`: Target column.

## Task Descriptions (Expected Difficulty)
1. **Easy:** Single table optimization (e.g., adding a missing index on an email column for a simple WHERE clause).
2. **Medium:** JOIN optimization (e.g., identifying and indexing missing foreign keys across two tables).
3. **Hard:** Composite index requirements (e.g., indexing multiple columns used in a complex AND condition).

## Setup & Usage Instructions
1. Install dependencies:
   ```bash
   pip install openenv-core pydantic fastapi uvicorn openai