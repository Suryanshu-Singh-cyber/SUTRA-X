# test_groq.py - Test Groq API
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("❌ No GROQ_API_KEY found in .env file!")
    print("Get your free key at: https://console.groq.com")
    exit()

print("=" * 50)
print("🔄 Testing Groq API (FREE)...")
print("=" * 50)
print(f"API Key: {GROQ_API_KEY[:10]}...{GROQ_API_KEY[-10:]}")

try:
    client = Groq(api_key=GROQ_API_KEY)
    
    # UPDATED: Changed from deprecated 'llama3-70b-8192' to an active model
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello SUTRA-X!'"}
        ],
        temperature=0.7,
        max_tokens=20
    )
    
    print("✅ Groq API is working!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n🔧 Fixes:")
    print("1. Check API key is correct")
    print("2. Check internet connection")
    print("3. Try: pip install groq --upgrade")

print("=" * 50)
