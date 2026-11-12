import os
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama
from supabase import create_client, Client

# Initialize Supabase client
url: str = os.environ.get("SUPABASE_URL", "http://localhost:54321")
key: str = os.environ.get("SUPABASE_ANON_KEY", "your-anon-key")
supabase: Client = create_client(url, key)

# Initialize Hermes LLM via Ollama (or TogetherAI/etc based on .env)
# Using local qwen3.5:9b as requested
llm = Ollama(model="qwen3.5:9b")

def update_task_status(task_id: str, status: str, result: str = None):
    # Log to event_logs
    supabase.table("event_logs").insert({
        "task_id": task_id,
        "event_type": "status_update",
        "details": {"status": status}
    }).execute()
    
    # Update task record
    data = {"status": status}
    if result:
        data["result"] = result
    supabase.table("tasks").update(data).eq("id", task_id).execute()

# --- Custom Tools ---
# In a full implementation, you would define custom LangChain tools here
# to "parse, prioritize, and structure incoming unstructured organizational data"
# e.g., using @tool decorator from langchain.tools

def run_crew_task(title: str, description: str):
    """
    Executes a crew workflow.
    In a real app, this takes a task_id and updates Supabase asynchronously.
    """
    
    # Define Agents
    researcher = Agent(
        role='Senior Data Analyst',
        goal='Analyze unstructured data and extract key priorities',
        backstory='Expert at parsing organizational data and finding bottlenecks.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Define Tasks
    analysis_task = Task(
        description=f"Analyze the following request: {title} - {description}. Extract actionable structured data.",
        expected_output="A structured JSON format containing the extracted priorities and bottlenecks.",
        agent=researcher
    )
    
    # Assemble Crew
    crew = Crew(
        agents=[researcher],
        tasks=[analysis_task],
        process=Process.sequential,
        verbose=True
    )
    
    # Execute (Mocked execution if LLM not running)
    try:
        result = crew.kickoff()
        return result
    except Exception as e:
        print(f"CrewAI Execution Error (Ensure Hermes/Ollama is running): {e}")
        return "Task finished with simulated output because LLM was unreachable."
