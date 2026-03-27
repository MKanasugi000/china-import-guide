"""SEO関連のユーティリティ。構造化データ、サイトマップ生成。"""
import json
from datetime import datetime
from models import Article
from config import SITE_URL, SITE_NAME


def generate_structured_data_article(article: Article) -> str:
    """記事の構造化データ (JSON-LD) を生成"""
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article.title,
        "description": article.meta_description,
        "datePublished": article.published_at.isoformat(),
        "dateModified": article.updated_at.isoformat(),
        "author": {
            "@type": "Organization",
            "name": SITE_NAME
        },
        "publisher": {
            "@type": "Organization",
            "name": SITE_NAME,
            "logo": {
                "@type": "ImageObject",
                "url": f"{SITE_URL}/static/images/logo.png"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"{SITE_URL}/article/{article.slug}"
        }
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def generate_faq_structured_data(article: Article) -> str:
    """FAQ構造化データ (JSON-LD) を生成"""
    if not article.faq:
        return ""
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["answer"]
                }
            }
            for faq in article.faq
        ]
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def generate_product_structured_data(article: Article, tag: str) -> str:
    """商品の構造化データ (JSON-LD) を生成"""
    if not article.products:
        return ""
    products = []
    for p in article.products:
        products.append({
            "@type": "Product",
            "name": p.name,
            "description": p.description,
            "url": p.affiliate_url(tag),
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": str(p.rating),
                "reviewCount": str(p.review_count)
            } if p.review_count > 0 else None
        })
    data = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "item": p
            }
            for i, p in enumerate(products)
        ]
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def generate_sitemap(articles: list[Article]) -> str:
    """サイトマップXMLを生成"""
    now = datetime.now().strftime("%Y-%m-%d")
    urls = [
        f"""  <url>
    <loc>{SITE_URL}/</loc>
    <lastmod>{now}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>"""
    ]
    for article in articles:
        urls.append(f"""  <url>
    <loc>{SITE_URL}/article/{article.slug}</loc>
    <lastmod>{article.updated_at.strftime("%Y-%m-%d")}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""


def generate_robots_txt() -> str:
    """robots.txtを生成"""
    return f"""User-agent: *
Allow: /
Sitemap: {SITE_URL}/sitemap.xml
"""
