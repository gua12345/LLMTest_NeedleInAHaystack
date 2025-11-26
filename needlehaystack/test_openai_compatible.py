import asyncio
import os
import sys
import json
from datetime import datetime, timezone

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from needlehaystack.llm_multi_needle_haystack_tester import LLMMultiNeedleHaystackTester
from needlehaystack.providers.openai import OpenAI
from needlehaystack.evaluators.openai import OpenAIEvaluator


async def test_openai_compatible_model():
    """
    测试OpenAI兼容接口的函数
    在这里直接修改模型名称和API接口配置
    """
    
    # ===== 在这里修改你的模型配置 =====
    # 修改为你要测试的OpenAI兼容模型名称
    MODEL_NAME = "GLM-4.6"  # 可以改为其他模型如 "gpt-4" 等
    
    # 修改为你的OpenAI兼容API端点（如果不是使用OpenAI官方API）
    # 如果使用OpenAI官方API，可以保持None
    OPENAI_BASE_URL = "https://oneapi.yesu.eu.org/v1"
    
    # 修改为你的API密钥环境变量名
    API_KEY_ENV = "sk-7Pk2t72PYqkvZxW_HAqprJFxoXVswd06d8iQ0qe8KCQcnxDtY1UXVSbuRuY"
    # ====================================
    
    # 设置API基础URL（如果需要）
    if OPENAI_BASE_URL:
        os.environ["OPENAI_BASE_URL"] = OPENAI_BASE_URL
    
    # 检查API密钥
    api_key = os.getenv(API_KEY_ENV)
    if not api_key:
        print(f"错误: 请设置环境变量 {API_KEY_ENV}")
        return
    
    # 创建模型提供者
    model_provider = OpenAI(model_name=MODEL_NAME)
    
    # 创建评估器
    evaluator = OpenAIEvaluator(
        model_name=MODEL_NAME,
        true_answer="The best thing to do in San Francisco is eat a sandwich and sit in Dolores Park on a sunny afternoon.",
        question_asked="What is the most fun thing to do in San Francisco?"
    )
    
    # 设置测试参数
    needles = [
        "The best thing to do in San Francisco is eat a sandwich and sit in Dolores Park on a sunny afternoon.",
        "The Golden Gate Bridge is a suspension bridge spanning the Golden Gate strait.",
        "San Francisco is known for its fog, steep hills, and eclectic mix of architecture."
    ]
    
    # 创建测试器实例
    tester = LLMMultiNeedleHaystackTester(
        needles=needles,
        model_to_test=model_provider,
        evaluator=evaluator,
        retrieval_question="What is the most fun thing to do in San Francisco?",
        context_lengths_min=64000,
        context_lengths_max=128000,
        context_lengths_num_intervals=5,
        document_depth_percent_min=0,
        document_depth_percent_max=100,
        document_depth_percent_intervals=3,
        num_concurrent_requests=1,
        save_results=True,
        save_contexts=True,
        print_ongoing_status=True
    )
    
    # 运行测试
    print(f"开始测试模型: {MODEL_NAME}")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    try:
        tester.start_test()
        
        # 打印测试结果摘要
        results = tester.get_results()
        print("\n" + "=" * 50)
        print("测试完成!")
        print(f"总测试数: {len(results)}")
        
        if results:
            scores = [r['score'] for r in results]
            print(f"平均分数: {sum(scores) / len(scores):.2f}")
            print(f"最高分数: {max(scores)}")
            print(f"最低分数: {min(scores)}")
            
            # 保存详细结果到JSON文件
            results_file = f"test_results_{MODEL_NAME.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"详细结果已保存到: {results_file}")
        
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_openai_compatible_model())