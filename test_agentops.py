"""
AgentOps API Key Diagnostic Script
This script helps verify your AgentOps configuration
"""

import os
from dotenv import load_dotenv
import agentops

# Load environment variables
load_dotenv(override=True)

# Get the API key
api_key = os.getenv("AGENTOPS_API_KEY")

print("="*80)
print("AGENTOPS DIAGNOSTIC")
print("="*80)

# Check if API key exists
if not api_key:
    print("❌ ERROR: AGENTOPS_API_KEY not found in environment variables")
    print("\nPlease check your .env file")
else:
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
    print(f"   Length: {len(api_key)} characters")
    
    # Check for common issues
    if api_key.startswith('"') or api_key.endswith('"'):
        print("⚠️  WARNING: API key contains quotes - this may cause issues")
    
    if ' ' in api_key:
        print("⚠️  WARNING: API key contains spaces - this may cause issues")
    
    # Try to initialize AgentOps
    print("\n" + "="*80)
    print("TESTING AGENTOPS INITIALIZATION")
    print("="*80)
    
    try:
        agentops.init(
            api_key=api_key,
            default_tags=["diagnostic-test"],
            auto_start_session=True
        )
        print("✅ AgentOps initialized successfully!")
        
        # Try to end the session
        agentops.end_session("Success")
        print("✅ Session ended successfully!")
        
        print("\n" + "="*80)
        print("RESULT: AgentOps configuration is WORKING!")
        print("="*80)
        
    except Exception as e:
        print(f"❌ ERROR: Failed to initialize AgentOps")
        print(f"   Error: {e}")
        print("\n" + "="*80)
        print("TROUBLESHOOTING STEPS:")
        print("="*80)
        print("1. Verify your API key at: https://app.agentops.ai/settings/projects")
        print("2. Make sure you've selected the correct project")
        print("3. Try regenerating your API key")
        print("4. Check if your account is active and has proper permissions")
