# Add API KEY in .env file, get from https://app.agentops.ai/settings/projects
# Install pip install agentops or pip install 'crewai[agentops]'

from crewai import Agent, Crew, Task, Process, LLM
from dotenv import load_dotenv
import os
import agentops
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Changed from DEBUG to reduce noise
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment variables first
load_dotenv(override=True)

# Initialize LLM
llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

class YourCrewName:
    def agent_one(self) -> Agent:
        return Agent(
            role="Data Analyst",
            goal="Analyze data trends in the market",
            backstory="An experienced data analyst with a background in economics",
            verbose=True,
            llm=llm,  # Use Groq LLM
        )

    def agent_two(self) -> Agent:
        return Agent(
            role="Market Researcher",
            goal="Gather information on market dynamics",
            backstory="A diligent researcher with a keen eye for detail",
            verbose=True,
            llm=llm,  # Use Groq LLM
        )

    def task_one(self) -> Task:
        return Task(
            name="Collect Data Task",
            description="Collect recent market data and identify trends.",
            expected_output="A report summarizing key trends in the market.",
            agent=self.agent_one(),
        )

    def task_two(self) -> Task:
        return Task(
            name="Market Research Task",
            description="Research factors affecting market dynamics.",
            expected_output="An analysis of factors influencing the market.",
            agent=self.agent_two(),
        )

    def crew(self) -> Crew:
        return Crew(
            agents=[self.agent_one(), self.agent_two()],
            tasks=[self.task_one(), self.task_two()],
            process=Process.sequential,
            verbose=True,
            manager_llm=llm,  # Use Groq for any manager operations
        )

if __name__ == "__main__":
    # Initialize AgentOps BEFORE creating the crew
    try:
        agentops.init(
            api_key=os.getenv("AGENTOPS_API_KEY"),
            default_tags=["crewai", "market-analysis"],
            auto_start_session=True,
            skip_auto_end_session=False  # Let AgentOps handle session ending
        )
        print("✅ AgentOps initialized successfully!")
    except Exception as e:
        print(f"⚠️  Warning: AgentOps initialization failed: {e}")
        print("   Continuing without AgentOps tracking...")
    
    # Create the crew
    my_crew = YourCrewName().crew()

    retry_attempts = 3
    for attempt in range(retry_attempts):
        try:
            logging.info("Starting crew kickoff...")
            result = my_crew.kickoff()
            logging.info("Crew kickoff completed successfully.")
            
            print("\n" + "="*80)
            print("FINAL RESULT:")
            print("="*80)
            print(result)
            print("="*80)
            
            # Try to end the session (use new API)
            try:
                agentops.end_trace("Success")
                print("\n✅ AgentOps session ended successfully!")
                print("📊 View your session at: https://app.agentops.ai/sessions")
            except Exception as e:
                logging.debug(f"Note: {e}")
            
            break
            
        except Exception as e:  # Generic exception to catch all errors
            logging.error(f"Error encountered: {e}")
            logging.debug("Traceback:", exc_info=True)
            print(f"Error encountered: {e}. Retrying in {2 ** attempt} seconds...")
            time.sleep(2 ** attempt)
    else:
        logging.error("Failed to complete the task after multiple attempts due to errors.")
        print("Failed to complete the task after multiple attempts due to errors.")
        try:
            agentops.end_trace("Fail")
        except:
            pass