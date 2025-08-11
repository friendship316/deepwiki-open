import sys
sys.path.append('.')

import os
from dotenv import load_dotenv
load_dotenv()

try:
    from api.data_pipeline import prepare_data_pipeline
    from adalflow.core.types import Document
    
    print('=== 数据管道测试 ===')
    
    # 初始化管道
    pipeline = prepare_data_pipeline(is_ollama_embedder=False)
    print('✅ 管道初始化成功')
    
    # 创建测试文档
    test_docs = [
        Document(
            text='This is a test document for the data pipeline. ' * 10,
            meta_data={'file_path': 'test.py', 'type': 'py'}
        )
    ]
    
    print(f'输入文档数: {len(test_docs)}')
    print(f'输入文档长度: {len(test_docs[0].text)} 字符')
    
    # 运行管道
    result = pipeline(test_docs)
    
    print(f'输出文档数: {len(result)}')
    
    # 检查每个输出文档
    empty_vectors = 0
    valid_vectors = 0
    
    for i, doc in enumerate(result):
        print(f'\n文档块 {i+1}:')
        print(f'  文本长度: {len(doc.text)}')
        print(f'  有向量属性: {hasattr(doc, "vector")}')
        
        if hasattr(doc, 'vector') and doc.vector:
            print(f'  向量长度: {len(doc.vector)}')
            print(f'  向量类型: {type(doc.vector)}')
            valid_vectors += 1
        else:
            print('  ❌ 向量为空')
            empty_vectors += 1
    
    print(f'\n总结: {valid_vectors} 个有效向量, {empty_vectors} 个空向量')
    
    if empty_vectors == 0:
        print('✅ 数据管道工作正常!')
    else:
        print('❌ 数据管道存在问题')
        
except Exception as e:
    print(f'❌ 测试失败: {e}')
    import traceback
    traceback.print_exc()