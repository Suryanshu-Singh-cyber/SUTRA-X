# test_openai.py - Updated for OpenAI 1.0.0+
import openai

OPENAI_API_KEY = "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"

try:
    # New OpenAI 1.0.0+ API
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say hello"}],
        max_tokens=10
    )
    print("✅ OpenAI API (1.0.0+) is working!")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"❌ OpenAI API Error: {e}")