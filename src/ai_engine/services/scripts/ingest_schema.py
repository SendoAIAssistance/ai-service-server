import argparse
import os

import pandas as pd
import logging
import yaml
from ai_engine.services.database.mongo_manager import MongoDBVectorManager
from ai_engine.core.config import settings
from ai_engine.core.server_logging import setup_logging

setup_logging()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_ingestion(yaml_path):
    abs_path = os.path.abspath(yaml_path)
    logger.info(f"🔍 Đang kiểm tra file tại: {abs_path}")
    file_name = os.path.basename(abs_path)
    if not os.path.exists(abs_path):
        logger.error(f"❌ Không tìm thấy file! Vui lòng kiểm tra lại đường dẫn.")

    db_manager = MongoDBVectorManager(collection_name="sendo_schema_dictionary")
    logger.info(f"Processing {file_name} ...")
    with open(abs_path, "r", encoding="utf-8") as f:
        schema_data = yaml.safe_load(f)

    columns = schema_data.get("columns", [])
    texts = []
    metadatas = []

    if not columns:
        logger.warning("⚠️ File YAML rỗng hoặc sai định dạng.")
        return
    logger.info(f"📦 Đang chuẩn bị nạp {len(columns)} cột vào MongoDB Atlas...")

    for col in columns:
        col_name = col.get("name")
        if not col_name:
            continue
        description = col.get("description") or col_name
        category = col.get("category", "Uncategorized")
        rich_text = f"Cột: '{col_name} | Ý nghĩa: {description}' | Phân loại: {category}"
        texts.append(rich_text)
        metadatas.append({
            "file": file_name,
            "category": category})
    # 4. Thực hiện nạp theo Batch
    db_manager.add_text_chunks(
        texts=texts, metadatas=metadatas, batch_size=20
    )

if __name__ == "__main__":
    run_ingestion(settings.PROJECT_ROOT / "src" / "storage" / "vector_db" / "sendo_dictionary" / "orders.yaml")