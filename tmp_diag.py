import os
from dotenv import load_dotenv
from groq import Groq
import inspect

load_dotenv()
key = os.getenv('GROQ_API_KEY')
print('GROQ_API_KEY loaded:', bool(key), 'length=', len(key) if key else 0)
client = Groq(api_key=key if key else 'x')
print('has_chat:', hasattr(client, 'chat'))
print('type_completions:', type(client.chat.completions))
print('completions_dir:', [a for a in dir(client.chat.completions) if not a.startswith('_')])
if hasattr(client.chat.completions, 'create'):
    print('create_sig:', inspect.signature(client.chat.completions.create))
