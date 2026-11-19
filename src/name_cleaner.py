import re
import pandas as pd

BRAND_ALIASES = {
    "coca cola": "Coca-Cola",
    "coca-cola": "Coca-Cola",
    "coke": "Coca-Cola",
    "pepsi cola": "Pepsi",
}


def clean_product_name(name):
    """清理商品名称，保留原始商品规格信息。"""
    if pd.isna(name):
        return ""

    text = str(name).strip().lower()
    text = text.replace("×", "x")
    text = re.sub(r"[_\-]+", " ", text)
    text = re.sub(r"[^\w\s.]", " ", text)
    text = re.sub(r"\s+", " ", text)

    text = re.sub(r"(\d+(?:\.\d+)?)\s*fl\s*\.?\s*oz\b", r"\1 fl oz", text)
    text = re.sub(r"(\d+(?:\.\d+)?)\s*oz\b", r"\1 oz", text)
    text = re.sub(r"(\d+(?:\.\d+)?)\s*ml\b", r"\1 ml", text)
    text = re.sub(r"(\d+(?:\.\d+)?)\s*g\b", r"\1 g", text)
    text = re.sub(r"(\d+(?:\.\d+)?)\s*lb\b", r"\1 lb", text)

    return text.strip()


def normalize_brand(name):
    """统一部分常见品牌别名。"""
    text = clean_product_name(name)

    for alias, standard in BRAND_ALIASES.items():
        pattern = r"^" + re.escape(alias) + r"\b"
        if re.search(pattern, text):
            text = re.sub(pattern, standard.lower(), text, count=1)
            break

    return text


def display_product_name(name):
    """生成便于阅读的标准化名称。"""
    text = normalize_brand(name)
    return text.title().replace("Fl Oz", "fl oz")
