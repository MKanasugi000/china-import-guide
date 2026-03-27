from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Product(BaseModel):
    name: str
    asin: str
    price: str
    image_url: str = ""
    rating: float = 0.0
    review_count: int = 0
    description: str = ""
    pros: list[str] = []
    cons: list[str] = []

    def affiliate_url(self, tag: str) -> str:
        return f"https://www.amazon.co.jp/dp/{self.asin}?tag={tag}"


class Article(BaseModel):
    slug: str
    title: str
    meta_description: str
    keyword: str
    h1: str
    intro: str
    sections: list[dict]  # {"heading": str, "content": str}
    products: list[Product] = []
    published_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    faq: list[dict] = []  # {"question": str, "answer": str}
