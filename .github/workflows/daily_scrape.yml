name: Daily ETF Scrape

# 触发条件
on:
  schedule:
    # 每天北京时间上午 9:00 运行 (UTC 时间 1:00)
    - cron: '0 1 * * *'
  workflow_dispatch: # 允许在 GitHub Actions 页面手动点击运行

# 核心权限设置：允许工作流向仓库写入文件
permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      # 1. 检出代码
      - name: Checkout Code
        uses: actions/checkout@v4

      # 2. 设置 Python 环境
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      # 3. 安装依赖项
      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; else pip install firecrawl-py; fi

      # 4. 运行爬虫脚本
      - name: Run Scraper
        env:
          FIRECRAWL_API_KEY: ${{ secrets.FIRECRAWL_API_KEY }}
        run: python scrape_etf.py

      # 5. 将生成的 JSON 文件提交并推送到仓库
      - name: Commit and Push Data
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          
          # 检查文件是否有变化，避免无意义的提交报错
          if git diff --quiet etf_data.json; then
            echo "No changes in ETF data, skipping commit."
          else
            git add etf_data.json
            git commit -m "Update ETF data: $(date +'%Y-%m-%d %H:%M:%S')"
            git push
          fi

      # 6. (可选) 将数据作为 Artifact 备份，方便手动下载
      - name: Upload Data Artifact
        uses: actions/upload-artifact@v4
        with:
          name: etf-json-backup
          path: etf_data.json
