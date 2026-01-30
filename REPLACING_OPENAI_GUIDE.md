# 🔄 Complete Guide: Replacing OpenAI with Free LLMs in CrewAI

## 📋 Table of Contents
1. [Understanding the Problem](#understanding-the-problem)
2. [The Solution: 3-Level LLM Assignment](#the-solution-3-level-llm-assignment)
3. [Step-by-Step Procedure](#step-by-step-procedure)
4. [Free LLM Options](#free-llm-options)
5. [Complete Examples](#complete-examples)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Understanding the Problem

### Why CrewAI Defaults to OpenAI

CrewAI has **3 levels** where it can use an LLM:

```
Level 1: Agent Level    ← Each agent needs an LLM
Level 2: Crew Level     ← Crew manager operations
Level 3: Global Default ← Falls back to OpenAI if not specified
```

**The Problem**: If you don't explicitly set the LLM at ALL levels, CrewAI falls back to OpenAI, causing rate limit errors.

### Before vs After

#### ❌ BEFORE (Wrong - Uses OpenAI)
```python
# LLM defined but NOT assigned to agents
llm = LLM(model="groq/llama-3.1-8b-instant")

agent = Agent(
    role="Researcher",
    goal="Research topics",
    backstory="Expert researcher"
    # ❌ No llm parameter - defaults to OpenAI!
)

crew = Crew(
    agents=[agent],
    tasks=[task]
    # ❌ No manager_llm - defaults to OpenAI!
)
```

#### ✅ AFTER (Correct - Uses Groq)
```python
# LLM defined AND assigned everywhere
llm = LLM(model="groq/llama-3.1-8b-instant")

agent = Agent(
    role="Researcher",
    goal="Research topics",
    backstory="Expert researcher",
    llm=llm  # ✅ Explicitly assigned
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    manager_llm=llm  # ✅ Explicitly assigned
)
```

---

## 🔧 The Solution: 3-Level LLM Assignment

### The Complete Procedure

```python
# STEP 1: Define your LLM (ONCE at the top)
llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# STEP 2: Assign to EVERY agent
agent1 = Agent(
    role="...",
    goal="...",
    backstory="...",
    llm=llm  # ← CRITICAL!
)

agent2 = Agent(
    role="...",
    goal="...",
    backstory="...",
    llm=llm  # ← CRITICAL!
)

# STEP 3: Assign to Crew
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    manager_llm=llm  # ← CRITICAL!
)
```

---

## 📝 Step-by-Step Procedure

### Procedure to Replace OpenAI with ANY Free LLM

Follow these steps for **EVERY CrewAI project**:

#### Step 1: Install Required Packages

```bash
# For Groq
pip install groq

# For Ollama (local)
pip install ollama

# For HuggingFace
pip install huggingface_hub

# For Google Gemini
pip install google-generativeai
```

#### Step 2: Set Up Environment Variables

Create/update `.env` file (NO QUOTES!):

```bash
# For Groq
GROQ_API_KEY=your_groq_api_key_here

# For Ollama (local - no key needed)
# Nothing needed

# For HuggingFace
HUGGINGFACE_API_KEY=your_hf_token_here

# For Google Gemini
GOOGLE_API_KEY=your_google_api_key_here
```

#### Step 3: Import and Load Environment

```python
from crewai import Agent, Crew, Task, Process, LLM
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(override=True)
```

#### Step 4: Define Your LLM (Choose One)

```python
# Option A: Groq (Free, Fast, Cloud)
llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# Option B: Ollama (Free, Local, No API Key)
llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

# Option C: HuggingFace (Free, Cloud)
llm = LLM(
    model="huggingface/meta-llama/Llama-3.1-8B-Instruct",
    api_key=os.getenv("HUGGINGFACE_API_KEY")
)

# Option D: Google Gemini (Free tier available)
llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)
```

#### Step 5: Create Agents with LLM Assignment

```python
def create_agent_with_llm(role, goal, backstory):
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        llm=llm,  # ← ALWAYS include this!
        verbose=True
    )

# Create all your agents
researcher = create_agent_with_llm(
    role="Researcher",
    goal="Research topics thoroughly",
    backstory="Expert researcher with years of experience"
)

writer = create_agent_with_llm(
    role="Writer",
    goal="Write engaging content",
    backstory="Professional content writer"
)
```

#### Step 6: Create Tasks

```python
research_task = Task(
    name="Research Task",
    description="Research the given topic",
    expected_output="A comprehensive research report",
    agent=researcher  # Agent already has llm assigned
)

writing_task = Task(
    name="Writing Task",
    description="Write an article based on research",
    expected_output="A well-written article",
    agent=writer  # Agent already has llm assigned
)
```

#### Step 7: Create Crew with Manager LLM

```python
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    manager_llm=llm,  # ← CRITICAL for crew operations!
    verbose=True
)
```

#### Step 8: Run and Verify

```python
if __name__ == "__main__":
    result = crew.kickoff()
    print(result)
```

---

## 🆓 Free LLM Options

### Comparison Table

| Provider | Speed | Cost | API Key Required | Local/Cloud | Best For |
|----------|-------|------|------------------|-------------|----------|
| **Groq** | ⚡⚡⚡ Very Fast | Free (limited) | ✅ Yes | Cloud | Production, Fast responses |
| **Ollama** | ⚡⚡ Fast | 100% Free | ❌ No | Local | Privacy, Unlimited usage |
| **HuggingFace** | ⚡ Moderate | Free (limited) | ✅ Yes | Cloud | Experimentation |
| **Google Gemini** | ⚡⚡ Fast | Free tier | ✅ Yes | Cloud | Multimodal tasks |

### 1. Groq (Recommended for Cloud)

**Pros**: Very fast, free tier, easy setup
**Cons**: Rate limits on free tier

```python
llm = LLM(
    model="groq/llama-3.1-8b-instant",  # Fast model
    # or "groq/llama-3.1-70b-versatile"  # More capable
    # or "groq/mixtral-8x7b-32768"       # Long context
    api_key=os.getenv("GROQ_API_KEY")
)
```

**Get API Key**: https://console.groq.com/keys

### 2. Ollama (Recommended for Local)

**Pros**: 100% free, unlimited, private, no API key
**Cons**: Requires local installation, uses your GPU/CPU

```python
llm = LLM(
    model="ollama/llama3.1",
    # or "ollama/mistral"
    # or "ollama/codellama"
    base_url="http://localhost:11434"
)
```

**Setup**:
```bash
# Install Ollama
# Windows: Download from https://ollama.ai
# Mac: brew install ollama
# Linux: curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama3.1

# Start Ollama (runs automatically on Windows/Mac)
ollama serve
```

### 3. HuggingFace

**Pros**: Many models available, free tier
**Cons**: Slower than Groq, rate limits

```python
llm = LLM(
    model="huggingface/meta-llama/Llama-3.1-8B-Instruct",
    api_key=os.getenv("HUGGINGFACE_API_KEY")
)
```

**Get API Key**: https://huggingface.co/settings/tokens

### 4. Google Gemini

**Pros**: Free tier, multimodal capabilities
**Cons**: Rate limits, requires Google account

```python
llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)
```

**Get API Key**: https://makersuite.google.com/app/apikey

---

## 💡 Complete Examples

### Example 1: Simple Project with Groq

```python
from crewai import Agent, Crew, Task, Process, LLM
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# Define LLM ONCE
llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# Create agent WITH llm
researcher = Agent(
    role="Researcher",
    goal="Research AI trends",
    backstory="AI research expert",
    llm=llm,  # ← Assigned
    verbose=True
)

# Create task
task = Task(
    name="Research Task",
    description="Research latest AI trends",
    expected_output="AI trends report",
    agent=researcher
)

# Create crew WITH manager_llm
crew = Crew(
    agents=[researcher],
    tasks=[task],
    process=Process.sequential,
    manager_llm=llm,  # ← Assigned
    verbose=True
)

# Run
if __name__ == "__main__":
    result = crew.kickoff()
    print(result)
```

### Example 2: Multi-Agent with Ollama (Local)

```python
from crewai import Agent, Crew, Task, Process, LLM

# Define LLM ONCE (no API key needed for Ollama)
llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

# Create multiple agents (all with same llm)
researcher = Agent(
    role="Researcher",
    goal="Research topics",
    backstory="Expert researcher",
    llm=llm,  # ← Assigned
    verbose=True
)

writer = Agent(
    role="Writer",
    goal="Write articles",
    backstory="Professional writer",
    llm=llm,  # ← Assigned
    verbose=True
)

editor = Agent(
    role="Editor",
    goal="Edit content",
    backstory="Experienced editor",
    llm=llm,  # ← Assigned
    verbose=True
)

# Create tasks
research_task = Task(
    name="Research",
    description="Research AI",
    expected_output="Research report",
    agent=researcher
)

writing_task = Task(
    name="Writing",
    description="Write article",
    expected_output="Article draft",
    agent=writer
)

editing_task = Task(
    name="Editing",
    description="Edit article",
    expected_output="Final article",
    agent=editor
)

# Create crew
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential,
    manager_llm=llm,  # ← Assigned
    verbose=True
)

# Run
if __name__ == "__main__":
    result = crew.kickoff()
    print(result)
```

### Example 3: Using Class Structure (Best Practice)

```python
from crewai import Agent, Crew, Task, Process, LLM
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# Define LLM globally
llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

class MyCrewProject:
    def __init__(self):
        self.llm = llm  # Store LLM reference
    
    def researcher_agent(self) -> Agent:
        return Agent(
            role="Researcher",
            goal="Research topics",
            backstory="Expert researcher",
            llm=self.llm,  # ← Use stored LLM
            verbose=True
        )
    
    def writer_agent(self) -> Agent:
        return Agent(
            role="Writer",
            goal="Write content",
            backstory="Professional writer",
            llm=self.llm,  # ← Use stored LLM
            verbose=True
        )
    
    def research_task(self) -> Task:
        return Task(
            name="Research Task",
            description="Research the topic",
            expected_output="Research report",
            agent=self.researcher_agent()
        )
    
    def writing_task(self) -> Task:
        return Task(
            name="Writing Task",
            description="Write article",
            expected_output="Article",
            agent=self.writer_agent()
        )
    
    def crew(self) -> Crew:
        return Crew(
            agents=[self.researcher_agent(), self.writer_agent()],
            tasks=[self.research_task(), self.writing_task()],
            process=Process.sequential,
            manager_llm=self.llm,  # ← Use stored LLM
            verbose=True
        )

if __name__ == "__main__":
    project = MyCrewProject()
    my_crew = project.crew()
    result = my_crew.kickoff()
    print(result)
```

---

## 🔍 Troubleshooting

### Issue 1: Still Getting OpenAI Errors

**Symptoms**: `openai.RateLimitError` or `openai.AuthenticationError`

**Solution Checklist**:
- ✅ LLM assigned to ALL agents (`llm=llm`)
- ✅ LLM assigned to Crew (`manager_llm=llm`)
- ✅ No agents created without LLM parameter
- ✅ Environment variables loaded correctly

**Debug Script**:
```python
# Add this to verify your setup
print(f"Agent LLM: {agent.llm}")
print(f"Crew Manager LLM: {crew.manager_llm}")
# Both should show your LLM, not None
```

### Issue 2: AgentOps Shows Wrong Model

**Before Fix**: AgentOps dashboard shows "gpt-4" or "gpt-3.5-turbo"
**After Fix**: AgentOps dashboard shows "groq/llama-3.1-8b-instant"

**Why**: AgentOps tracks the actual LLM being used. If you see OpenAI models, it means CrewAI is still using OpenAI somewhere.

**Verification**:
1. Run your script
2. Check AgentOps dashboard
3. Look at "Model" column
4. Should show your configured model (e.g., "groq/llama-3.1-8b-instant")

### Issue 3: Groq Rate Limits

**Error**: `Rate limit exceeded`

**Solutions**:
1. **Use slower requests**: Add delays between crew runs
2. **Switch to Ollama**: Unlimited local usage
3. **Use multiple API keys**: Rotate between keys
4. **Upgrade Groq plan**: Get higher limits

### Issue 4: Ollama Connection Failed

**Error**: `Connection refused` or `Model not found`

**Solutions**:
```bash
# 1. Check Ollama is running
ollama list

# 2. Pull the model
ollama pull llama3.1

# 3. Test the model
ollama run llama3.1 "Hello"

# 4. Check the URL in your code
# Should be: http://localhost:11434
```

---

## 📊 Verification Checklist

Use this checklist for EVERY CrewAI project:

```
□ LLM defined at the top of the file
□ Environment variables loaded (load_dotenv())
□ API key in .env file (no quotes)
□ LLM assigned to EVERY agent (llm=llm)
□ LLM assigned to Crew (manager_llm=llm)
□ No agents created without llm parameter
□ Tested with a simple run
□ Verified on AgentOps dashboard (if using)
```

---

## 🎯 Summary

### The Golden Rule

**ALWAYS assign your LLM at 3 places:**

1. **Each Agent**: `Agent(..., llm=llm)`
2. **Crew Manager**: `Crew(..., manager_llm=llm)`
3. **Define Once**: Create LLM object once at the top

### Quick Template

```python
# 1. Define LLM (ONCE)
llm = LLM(model="groq/llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

# 2. Assign to agents (EVERY agent)
agent = Agent(role="...", goal="...", backstory="...", llm=llm)

# 3. Assign to crew (ALWAYS)
crew = Crew(agents=[...], tasks=[...], manager_llm=llm)
```

### Why This Works

- CrewAI checks for LLM at agent level first
- If not found, checks crew manager level
- If still not found, falls back to OpenAI (causing errors)
- By assigning at all levels, we ensure no OpenAI calls

---

**Result**: ✅ No more OpenAI rate limit errors! Your free LLM is used everywhere!
