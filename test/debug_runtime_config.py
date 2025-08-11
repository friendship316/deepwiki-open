#!/usr/bin/env python3
"""
调试运行时配置加载
"""
import sys
sys.path.append('.')

import os
from dotenv import load_dotenv
load_dotenv()

def debug_config():
    print("=== 运行时配置调试 ===")
    
    # 1. 检查环境变量
    print("\n1. 环境变量检查:")
    print(f"   OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')[:10]}..." if os.getenv('OPENAI_API_KEY') else "   OPENAI_API_KEY: None")
    print(f"   OPENAI_BASE_URL: {os.getenv('OPENAI_BASE_URL')}")
    print(f"   DEEPWIKI_CONFIG_DIR: {os.getenv('DEEPWIKI_CONFIG_DIR', 'Not Set (using default)')}")
    
    # 2. 检查配置文件路径
    print("\n2. 配置文件路径:")
    from pathlib import Path
    config_dir = os.getenv('DEEPWIKI_CONFIG_DIR', None)
    if config_dir:
        embedder_path = Path(config_dir) / "embedder.json"
    else:
        embedder_path = Path(__file__).parent.parent / "api" / "config" / "embedder.json"
    
    print(f"   embedder.json路径: {embedder_path}")
    print(f"   文件存在: {embedder_path.exists()}")
    
    if embedder_path.exists():
        import json
        with open(embedder_path) as f:
            config = json.load(f)
        print(f"   模型配置: {config.get('embedder', {}).get('model_kwargs', {}).get('model', 'Unknown')}")
    
    # 3. 检查实际加载的配置
    print("\n3. 实际加载的配置:")
    try:
        from api.config import configs, get_embedder_config
        print(f"   configs存在embedder: {'embedder' in configs}")
        if 'embedder' in configs:
            embedder_config = configs['embedder']
            print(f"   模型名称: {embedder_config.get('model_kwargs', {}).get('model', 'Not Found')}")
            print(f"   批处理大小: {embedder_config.get('batch_size', 'Not Found')}")
            print(f"   客户端类: {embedder_config.get('model_client', 'Not Found')}")
        
        # 使用get_embedder_config函数
        embedder_config2 = get_embedder_config()
        print(f"   get_embedder_config结果: {embedder_config2}")
        
    except Exception as e:
        print(f"   加载配置出错: {e}")
    
    # 4. 测试实际的嵌入器创建
    print("\n4. 实际嵌入器创建测试:")
    try:
        from api.tools.embedder import get_embedder
        embedder = get_embedder()
        print(f"   ✅ 嵌入器创建成功: {type(embedder)}")
        
        # 测试一个简单的嵌入
        result = embedder("Test embedding")
        if result and hasattr(result, 'data') and result.data:
            print(f"   ✅ 嵌入测试成功，向量长度: {len(result.data[0].embedding) if result.data[0].embedding else 0}")
        else:
            print(f"   ❌ 嵌入测试失败: {result}")
            
    except Exception as e:
        print(f"   ❌ 嵌入器创建/测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_config()