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

    # 2. 直接定义抽取模式
    schema = {
        "type": "object",
        "properties": {
            "etf_data": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "date": {"type": "string", "description": "业务日期"},
                        "fund_code": {"type": "string", "description": "基金代码"},
                        "fund_name": {"type": "string", "description": "基金简称"},
                        "total_share_10k": {"type": "string", "description": "总份额（万份）"}
                    }
                }
            }
        }
    }

    print(f"Starting to scrape: {target_url}")

    try:
        # 3. 修正后的调用：直接传递参数，不再嵌套在 params 里
        # 根据最新 SDK，formats 和 extract 现在是平级参数
        response = app.scrape_url(
            url=target_url,
            formats=["extract"],
            extract={
                "schema": schema,
                "prompt": "从网页表格中提取 ETF 份额数据列表。"
            }
        )

        # 4. 提取结果
        # 注意：部分版本结果在 response['extract']，部分在 response['data']['extract']
        # 这里做一个健壮性取值
        extracted_content = response.get("extract") or response.get("data", {}).get("extract")

        if extracted_content:
            output_file = "etf_data.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(extracted_content, f, indent=4, ensure_ascii=False)
            print(f"Success! Extracted {len(extracted_content.get('etf_data', []))} records.")
        else:
            print("Response received but no extraction data found.")
            print(f"Debug Response: {response}")
            sys.exit(1)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_etf_data()
