import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('OPENAI_BASE_URL')

if api_key:
    client = openai.OpenAI(api_key=api_key, base_url=base_url)
    try:
        response = client.chat.completions.create(
            model='deepseek-r1',
            messages=[{'role': 'user', 'content': 'Hello'}],
            max_tokens=10
        )
        print('✓ OpenAI API连接正常')
    except Exception as e:
        print('✗ OpenAI API连接失败:', e)
else:
    print('✗ 未找到OPENAI_API_KEY')
