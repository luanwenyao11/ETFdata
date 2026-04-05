import os
import json
import sys
from firecrawl import FirecrawlApp

def fetch_etf_data():
    # 1. 从环境变量获取 API Key (在 GitHub Secrets 中配置)
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        print("Error: FIRECRAWL_API_KEY not found in environment variables.")
        sys.exit(1)

    # 2. 初始化 Firecrawl
    app = FirecrawlApp(api_key=api_key)

    target_url = "https://www.sse.com.cn/market/funddata/volumn/etfvolumn/"

    # 3. 配置提取模式 (Schema)
    # 定义我们需要的字段结构
    extract_params = {
        "prompt": "从网页表格中提取 ETF 份额数据。请确保抓取所有列，包括日期、基金代码、基金简称和总份额。",
        "schema": {
            "type": "object",
            "properties": {
                "etf_data": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "date": {"type": "string", "description": "业务日期，通常格式为 YYYY-MM-DD"},
                            "fund_code": {"type": "string", "description": "基金代码，6位数字"},
                            "fund_name": {"type": "string", "description": "基金扩位简称"},
                            "total_share_10k": {"type": "string", "description": "总份额（万份）"}
                        },
                        "required": ["date", "fund_code", "fund_name", "total_share_10k"]
                    }
                }
            }
        }
    }

    print(f"Starting to scrape: {target_url}")

    try:
        # 4. 执行抓取
        # 使用 wait_for_selector 确保表格加载完成
        # 使用 formats=["extract"] 启用 AI 结构化提取
        scrape_result = app.scrape(
            url=target_url,
            params={
                "formats": ["extract"],
                "extract": extract_params,
                "waitFor": 3000  # 等待 3 秒确保 JS 渲染完成
            }
        )

        # 5. 验证并保存结果
        if "extract" in scrape_result and scrape_result["extract"]:
            extracted_data = scrape_result["extract"]
            
            # 保存为 JSON 文件
            output_file = "etf_data.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(extracted_data, f, indent=4, ensure_ascii=False)
            
            print(f"Successfully extracted {len(extracted_data.get('etf_data', []))} items.")
            print(f"Data saved to {output_file}")
        else:
            print("Failed to extract structured data. Check if the page structure has changed.")
            sys.exit(1)

    except Exception as e:
        print(f"An error occurred during scraping: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_etf_data()
