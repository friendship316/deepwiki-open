import sys
sys.path.append('.')

import os
from dotenv import load_dotenv
load_dotenv()

try:
    from api.tools.embedder import get_embedder
    from adalflow.core.types import Document
    
    print('=== DeepWiki 嵌入器测试 ===')
    print(f'OPENAI_API_KEY: {os.getenv("OPENAI_API_KEY")[:10]}...' if os.getenv("OPENAI_API_KEY") else 'None')
    print(f'OPENAI_BASE_URL: {os.getenv("OPENAI_BASE_URL")}')
    print()
    
    print('正在初始化嵌入器...')
    embedder = get_embedder()
    print('✅ 嵌入器初始化成功')
    print()
    
    # 测试单个文档嵌入
    print('测试单个文档嵌入...')
    test_text = 'This is a test document for embedding analysis.'
    
    result = embedder(test_text)
    print(f'Result type: {type(result)}')
    print(f'Result: {result}')
    
    if result and hasattr(result, 'data') and result.data:
        print(f'✅ 单文档嵌入成功!')
        print(f'   数据项数量: {len(result.data)}')
        if len(result.data) > 0:
            first_item = result.data[0]
            print(f'   第一项类型: {type(first_item)}')
            if hasattr(first_item, 'embedding'):
                embedding = first_item.embedding
                print(f'   向量长度: {len(embedding)}')
                print(f'   向量类型: {type(embedding)}')
                print(f'   前5个值: {embedding[:5] if len(embedding) >= 5 else embedding}')
            else:
                print(f'   第一项属性: {dir(first_item)}')
    else:
        print('❌ 单文档嵌入失败 - 无有效结果')
        if result:
            print(f'   Result 属性: {dir(result)}')
            if hasattr(result, 'data'):
                print(f'   Data: {result.data}')
    print()
    
    # 测试批量文档嵌入
    print('测试批量文档嵌入...')
    test_texts = [
        'First document content for batch embedding test.',
        'Second document with different content.',
        'Third document to verify batch processing.'
    ]
    
    batch_result = embedder(test_texts)
    print(f'Batch result type: {type(batch_result)}')
    
    if batch_result and hasattr(batch_result, 'data') and batch_result.data:
        print(f'✅ 批量嵌入成功! 处理了 {len(batch_result.data)} 个文档')
        for i, item in enumerate(batch_result.data):
            if hasattr(item, 'embedding') and item.embedding:
                print(f'   文档 {i+1}: 向量长度 = {len(item.embedding)}')
            else:
                print(f'   文档 {i+1}: ❌ 向量为空或无效')
                print(f'      项目属性: {dir(item)}')
    else:
        print('❌ 批量嵌入失败')
        if batch_result:
            print(f'   Batch result 属性: {dir(batch_result)}')
            if hasattr(batch_result, 'data'):
                print(f'   Data: {batch_result.data}')
    
except Exception as e:
    print(f'❌ 测试失败: {e}')
    import traceback
    traceback.print_exc()