import os
import json
import sys
from firecrawl import FirecrawlApp

def fetch_etf_data():
    # 1. 获取环境变量
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        print("错误: 未找到 API KEY")
        sys.exit(1)

    # 2. 初始化
    app = FirecrawlApp(api_key=api_key)
    target_url = "https://www.sse.com.cn/market/funddata/volumn/etfvolumn/"
    
    print(f"正在尝试稳定版抓取: {target_url}")

    # 3. 稳定版参数格式
    params = {
        "extractorOptions": {
            "prompt": "提取表格中的 ETF 数据：基金代码、基金扩位简称、总份额(万份)。",
            "extractionSchema": {
                "type": "object",
                "properties": {
                    "etf_data": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "date": {"type": "string"},
                                "fund_code": {"type": "string"},
                                "fund_name": {"type": "string"},
                                "total_share_10k": {"type": "string"}
                            }
                        }
                    }
                }
            }
        },
        "waitFor": 5000
    }

    try:
        # 在 0.0.20 版本中，scrape_url 是最稳的方法
        result = app.scrape_url(target_url, params=params)

        if result:
            with open("etf_data.json", "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
            print("--- 终于成功了！稳定版万岁！ ---")
        else:
            print("抓取完成但无数据。")

    except Exception as e:
        print(f"运行失败: {str(e)}")

if __name__ == "__main__":
    fetch_etf_data()
