#!/usr/bin/env python3
"""
调试完整的数据处理管道，模拟实际项目运行过程
"""
import sys
sys.path.append('.')

import os
from dotenv import load_dotenv
load_dotenv()

def debug_pipeline():
    print("=== 完整管道调试 ===")
    
    try:
        from adalflow.core.types import Document
        from api.data_pipeline import prepare_data_pipeline
        
        print("\n1. 创建测试文档...")
        # 创建一些测试文档，模拟实际的代码文件
        test_docs = [
            Document(text="def hello_world():\n    print('Hello, World!')\n    return True"),
            Document(text="import os\nimport sys\n\nclass TestClass:\n    def __init__(self):\n        self.value = 42"),
            Document(text="# This is a comment\n# Another comment\nfrom typing import Dict, List\n\ndef process_data(data: List[str]) -> Dict[str, int]:"),
            Document(text=""),  # 空文档，测试边界情况
            Document(text="   "),  # 只有空格的文档
            Document(text="a"),  # 极短文档
        ]
        
        print(f"   创建了 {len(test_docs)} 个测试文档")
        for i, doc in enumerate(test_docs):
            print(f"   文档 {i}: 长度={len(doc.text)}, 预览={repr(doc.text[:50])}")
        
        print("\n2. 准备数据管道...")
        data_pipeline = prepare_data_pipeline()
        print(f"   ✅ 数据管道创建成功: {type(data_pipeline)}")
        
        print("\n3. 执行数据管道处理...")
        print("   这会进行文本分割、嵌入向量化等步骤...")
        
        try:
            processed_docs = data_pipeline(test_docs)
            print(f"   ✅ 管道处理完成")
            print(f"   输入文档数: {len(test_docs)}")
            print(f"   输出文档数: {len(processed_docs) if processed_docs else 0}")
            
            if processed_docs:
                print("\n4. 检查处理结果...")
                empty_vectors = 0
                valid_vectors = 0
                
                for i, doc in enumerate(processed_docs):
                    print(f"\n   文档 {i}:")
                    print(f"      类型: {type(doc)}")
                    print(f"      文本长度: {len(doc.text) if hasattr(doc, 'text') else 'N/A'}")
                    print(f"      文本预览: {repr(doc.text[:50]) if hasattr(doc, 'text') else 'N/A'}")
                    
                    if hasattr(doc, 'vector'):
                        if doc.vector is None:
                            print(f"      向量: None")
                            empty_vectors += 1
                        elif isinstance(doc.vector, list):
                            if len(doc.vector) == 0:
                                print(f"      向量: 空列表")
                                empty_vectors += 1
                            else:
                                print(f"      向量: 列表，长度={len(doc.vector)}")
                                valid_vectors += 1
                        else:
                            print(f"      向量: {type(doc.vector)}")
                            if hasattr(doc.vector, '__len__'):
                                try:
                                    length = len(doc.vector)
                                    if length == 0:
                                        empty_vectors += 1
                                        print(f"      向量长度: 0 (空向量)")
                                    else:
                                        valid_vectors += 1
                                        print(f"      向量长度: {length}")
                                except Exception as e:
                                    print(f"      向量长度检查失败: {e}")
                    else:
                        print(f"      向量: 不存在vector属性")
                        empty_vectors += 1
                
                print(f"\n   📊 统计结果:")
                print(f"      有效向量: {valid_vectors}")
                print(f"      空向量: {empty_vectors}")
                print(f"      总计: {len(processed_docs)}")
                
                if empty_vectors > 0:
                    print(f"\n   ⚠️  发现 {empty_vectors} 个空向量！")
                    return False
                else:
                    print(f"\n   ✅ 所有向量都有效")
                    return True
            else:
                print("   ❌ 管道处理返回空结果")
                return False
                
        except Exception as e:
            print(f"   ❌ 管道处理失败: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"❌ 管道调试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_pipeline()
    if success:
        print("\n🎉 管道调试成功！")
    else:
        print("\n💥 管道调试发现问题！")