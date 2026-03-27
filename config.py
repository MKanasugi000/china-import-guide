import os
from dotenv import load_dotenv

load_dotenv()

AMAZON_ASSOCIATE_TAG = os.getenv("AMAZON_ASSOCIATE_TAG", "your-tag-22")
SITE_URL = os.getenv("SITE_URL", "http://localhost:8000")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
SITE_NAME = "中国輸入おすすめ商品比較サイト"
SITE_DESCRIPTION = "中国輸入ビジネスの商品比較、始め方、利益計算ツールなど最新情報を網羅的にお届けします。"

ARTICLES_DIR = os.path.join(os.path.dirname(__file__), "articles")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
