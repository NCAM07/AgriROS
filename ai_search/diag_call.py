import os
from dotenv import load_dotenv
from groq import Groq
import traceback

load_dotenv()
key = os.getenv('GROQ_API_KEY')
print('Using key loaded:', bool(key), 'len=', len(key) if key else 0)
client = Groq(api_key=key if key else 'x')
try:
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"system","content":"diag"},{"role":"user","content":"Say hi"}],
        max_tokens=10,
        temperature=0
    )
    print('Response type:', type(resp))
    try:
        print('Response repr:', repr(resp))
    except Exception:
        pass
except Exception as e:
    print('EXCEPTION:', type(e), e)
    traceback.print_exc()
