import dashscope
from dashscope import MultiModalConversation

# ⚠️ 请在这里填入你的 DashScope API Key
# 或者确保你已经设置了环境变量 DASHSCOPE_API_KEY
dashscope.api_key = "sk-bcc154aeda0a4d4a90955d22bd341195"

def test_stock_chart_vision(image_path):
    print(f"👀 正在分析图片: {image_path} ...")
    
    # 构建消息，包含文本和图片
    # 注意：VL 模型支持本地文件路径，也支持 http 链接
    messages = [
        {
            "role": "user",
            "content": [
                {"image": image_path},  # 这里传入图片路径
                {"text": "请分析这张图表中的股票走势。是上升趋势还是下降趋势？如果你能看清，请告诉我股票代码或名称。"}
            ]
        }
    ]

    try:
        # 调用 qwen-vl-plus 模型
        response = MultiModalConversation.call(
            model='qwen-vl-plus', 
            messages=messages
        )

        if response.status_code == 200:
            print("\n✅ 模型返回结果：")
            print("-" * 30)
            print(response.output.choices[0].message.content[0]["text"])
            print("-" * 30)
        else:
            print(f"\n❌ 请求失败: {response.code} - {response.message}")
            
    except Exception as e:
        print(f"\n💥 发生错误: {str(e)}")

if __name__ == "__main__":
    # 这里替换成你本地的一张股票 K 线图路径
    # 如果没有图片，脚本会报错，请确保路径正确
    local_image_path = "test_stock_chart.png" 
    
    # 为了防止你直接运行报错，我加了一个简单的判断
    import os
    if os.path.exists(local_image_path):
        test_stock_chart_vision(local_image_path)
    else:
        print(f"⚠️ 提示：请在同目录下放一张名为 '{local_image_path}' 的图片，或者修改代码中的图片路径。")