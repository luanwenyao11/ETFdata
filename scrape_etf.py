import os
import json
import sys
from firecrawl import FirecrawlApp

def fetch_etf_data():
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        print("Error: FIRECRAWL_API_KEY not found.")
        sys.exit(1)

    app = FirecrawlApp(api_key=api_key)
    target_url = "https://www.sse.com.cn/market/funddata/volumn/etfvolumn/"

    # 定义 Schema
    schema = {
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

    print(f"Starting to scrape with latest API structure: {target_url}")

    try:
        # 这种写法是目前最通用的：将 schema 放在 extraction_params 中
        # 如果 scrape_url 报错，请尝试改为 app.scrape
        response = app.scrape_url(
            target_url, 
            {
                'formats': ['extract'],
                'extract': {
                    'schema': schema
                }
            }
        )

        # 检查返回结构 (Firecrawl 有时返回对象，有时返回字典)
        data = None
        if isinstance(response, dict):
            data = response.get("extract") or response.get("data", {}).get("extract")
        else:
            # 如果是对象属性
            data = getattr(response, 'extract', None)

        if data:
            with open("etf_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("Success! Data saved to etf_data.json")
        else:
            print(f"Extraction failed. Full response for debugging: {response}")
            sys.exit(1)

    except Exception as e:
        print(f"Final attempt failed: {str(e)}")
        # 调试信息：打印出当前 SDK 支持的所有方法名，帮你快速定位
        print("\n--- SDK Debug Info ---")
        import inspect
        if hasattr(app, 'scrape_url'):
            print(f"scrape_url signature: {inspect.signature(app.scrape_url)}")
        elif hasattr(app, 'scrape'):
            print(f"scrape signature: {inspect.signature(app.scrape)}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_etf_data()
