"""
中国輸入おすすめ商品比較サイト - FastAPI アプリケーション
自動アフィリエイト/SEOサイトのメインアプリ。
"""
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from apscheduler.schedulers.background import BackgroundScheduler

from config import (
    SITE_NAME, SITE_DESCRIPTION, SITE_URL,
    AMAZON_ASSOCIATE_TAG, TEMPLATES_DIR
)
from article_generator import generate_articles, save_articles_as_json, load_articles_from_json
from seo import (
    generate_structured_data_article,
    generate_faq_structured_data,
    generate_product_structured_data,
    generate_sitemap,
    generate_robots_txt,
)

app = FastAPI(title=SITE_NAME, description=SITE_DESCRIPTION)

# 静的ファイル
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# テンプレート
templates = Jinja2Templates(directory=TEMPLATES_DIR)


def refresh_articles():
    """記事データを再生成して保存（定期実行用）"""
    articles = generate_articles()
    save_articles_as_json(articles)
    print(f"[Scheduler] Refreshed {len(articles)} articles")


# 起動時に記事を生成
@app.on_event("startup")
def startup_event():
    articles = load_articles_from_json()
    if not articles:
        refresh_articles()
    # 24時間ごとに記事を更新
    scheduler = BackgroundScheduler()
    scheduler.add_job(refresh_articles, "interval", hours=24)
    scheduler.start()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    articles = load_articles_from_json()
    return templates.TemplateResponse(request, "index.html", {
        "site_name": SITE_NAME,
        "site_description": SITE_DESCRIPTION,
        "site_url": SITE_URL,
        "articles": articles,
    })


@app.get("/article/{slug}", response_class=HTMLResponse)
async def article_page(request: Request, slug: str):
    articles = load_articles_from_json()
    article = next((a for a in articles if a.slug == slug), None)
    if not article:
        return HTMLResponse(content="記事が見つかりません", status_code=404)

    other_articles = [a for a in articles if a.slug != slug][:4]

    return templates.TemplateResponse(request, "article.html", {
        "site_name": SITE_NAME,
        "site_url": SITE_URL,
        "article": article,
        "other_articles": other_articles,
        "amazon_tag": AMAZON_ASSOCIATE_TAG,
        "structured_data_article": generate_structured_data_article(article),
        "structured_data_faq": generate_faq_structured_data(article),
        "structured_data_product": generate_product_structured_data(article, AMAZON_ASSOCIATE_TAG),
    })


@app.get("/sitemap.xml", response_class=Response)
async def sitemap():
    articles = load_articles_from_json()
    content = generate_sitemap(articles)
    return Response(content=content, media_type="application/xml")


@app.get("/robots.txt", response_class=Response)
async def robots():
    content = generate_robots_txt()
    return Response(content=content, media_type="text/plain")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
