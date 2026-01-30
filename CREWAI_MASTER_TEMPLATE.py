
"""
🚀 CREWAI MASTER TEMPLATE (NO OPENAI ERRORS)
--------------------------------------------
Use this template for all new projects to avoid "RateLimitError".
It implements the "3-Step Rule" to ensure your free LLM is used everywhere.

PREREQUISITES:
1. pip install crewai langchain-groq python-dotenv
2. Create a .env file with: GROQ_API_KEY=your_key_here
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Task, Process, LLM

# ----------------------------------------------------------------------
# 🔧 STEP 0: SETUP
# ----------------------------------------------------------------------
load_dotenv(override=True)

# Define your LLM *ONCE* here. Switch comments to use Ollama/Gemini.
# ----------------------------------------------------------------------

# Option 1: Groq (Fast, Free Cloud)
LLM_CONFIG = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# Option 2: Ollama (Local, Unlimited)
# LLM_CONFIG = LLM(
#     model="ollama/llama3.1",
#     base_url="http://localhost:11434"
# )

# ----------------------------------------------------------------------
# 🤖 STEP 1: DEFINE AGENTS (Assign LLM to EVERY Agent)
# ----------------------------------------------------------------------

def create_researcher():
    return Agent(
        role="Senior Researcher",
        goal="Uncover groundbreaking information about {topic}",
        backstory="Driven by curiosity, you're at the forefront of innovation.",
        verbose=True,
        allow_delegation=False,
        # 🔑 CRITICAL FIX: Always pass the llm parameter!
        llm=LLM_CONFIG
    )

def create_writer():
    return Agent(
        role="Tech Content Strategist",
        goal="Craft compelling content on {topic}",
        backstory="You are a renowned Content Strategist, known for simplifying complex topics.",
        verbose=True,
        allow_delegation=False,
        # 🔑 CRITICAL FIX: Always pass the llm parameter!
        llm=LLM_CONFIG
    )

# ----------------------------------------------------------------------
# 📋 STEP 2: DEFINE TASKS
# ----------------------------------------------------------------------

def create_tasks(researcher_agent, writer_agent, topic):
    task1 = Task(
        description=f"Conduct a comprehensive analysis on {topic}.",
        expected_output="A detailed report summarizing key findings.",
        agent=researcher_agent
    )

    task2 = Task(
        description=f"Using the insights provided, write an engaging blog post about {topic}.",
        expected_output="A blog post of at least 4 paragraphs.",
        agent=writer_agent
    )
    return [task1, task2]

# ----------------------------------------------------------------------
# 🚀 STEP 3: DEFINE CREW (Assign Manager LLM)
# ----------------------------------------------------------------------

def run_crew(topic_name):
    # Instantiate agents
    researcher = create_researcher()
    writer = create_writer()

    # Instantiate tasks
    tasks = create_tasks(researcher, writer, topic_name)

    # Create Crew
    my_crew = Crew(
        agents=[researcher, writer],
        tasks=tasks,
        process=Process.sequential,  # Sequential execution is usually safer for rate limits
        verbose=True,
        # 🔑 CRITICAL FIX: Always pass the manager_llm!
        manager_llm=LLM_CONFIG
    )

    print(f"\n🚀 Starting Crew on topic: {topic_name}\n")
    result = my_crew.kickoff(inputs={'topic': topic_name})
    return result

# ----------------------------------------------------------------------
# 🏁 MAIN EXECUTION
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Test the setup
    topic = "The Future of AI Agents"
    result = run_crew(topic)
    
    print("\n\n########################")
    print("##     FINAL OUTPUT   ##")
    print("########################\n")
    print(result)
