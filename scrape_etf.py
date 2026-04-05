import os
import json
import sys
from firecrawl import FirecrawlApp

def fetch_etf_data():
    # 1. 获取环境变量中的 API Key
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        print("Error: FIRECRAWL_API_KEY not found.")
        sys.exit(1)

    app = FirecrawlApp(api_key=api_key)
    target_url = "https://www.sse.com.cn/market/funddata/volumn/etfvolumn/"

    # 2. 严格按照 params 字典结构组织参数
    # 根据签名，所有配置必须放在这个字典里
    extraction_params = {
        "formats": ["extract"],
        "extract": {
            "prompt": "从网页表格中提取 ETF 份额数据。包括：业务日期、基金代码、基金简称、总份额（万份）。",
            "schema": {
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
        }
    }

    print(f"Starting to scrape: {target_url}")

    try:
        # 3. 严格匹配签名: (url, params)
        # 注意：这里不使用 extract=... 或 formats=...，只传两个位置参数
        response = app.scrape_url(target_url, params=extraction_params)

        # 4. 结果提取
        # SDK 返回的 response 可能是字典，也可能是带有属性的对象
        result_data = None
        if isinstance(response, dict):
            # 尝试多种可能的路径
            result_data = response.get("extract") or response.get("data", {}).get("extract")
        else:
            # 如果返回的是对象，尝试访问其属性
            result_data = getattr(response, "extract", None) or getattr(getattr(response, "data", {}), "extract", None)

        if result_data:
            output_file = "etf_data.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result_data, f, indent=4, ensure_ascii=False)
            
            count = len(result_data.get("etf_data", []))
            print(f"Success! Extracted {count} records. Saved to {output_file}")
        else:
            print("Extraction completed but result_data is empty.")
            print(f"Debug Response: {response}")
            sys.exit(1)

    except Exception as e:
        print(f"Scraping failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_etf_data()
