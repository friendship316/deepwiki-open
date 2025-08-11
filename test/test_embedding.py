import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('OPENAI_BASE_URL')

print(f'API Key: {api_key[:10]}...' if api_key else 'API Key: None')
print(f'Base URL: {base_url}')

if api_key:
    try:
        client = openai.OpenAI(api_key=api_key, base_url=base_url)
        # 测试嵌入API
        response = client.embeddings.create(
            model='bge-m3',
            input='Hello, this is a test.'
        )
        print('✓ OpenAI 嵌入API连接成功')
        print(f'向量维度: {len(response.data[0].embedding)}')
    except Exception as e:
        print(f'✗ OpenAI API连接失败: {e}')
else:
    print('✗ 未找到OPENAI_API_KEY')