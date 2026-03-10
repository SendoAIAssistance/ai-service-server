import time
import logging
from pathlib import Path
from typing import List, Dict, Any

import yaml
from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_ollama import OllamaEmbeddings

from ai_engine.core.config import settings

logger = logging.getLogger("ai_service.database.mongo_manager")


class MongoDBVectorManager:
    def __init__(
            self,
            db_name: str = "AI_Assistance",
            collection_name: str = "AI_Service",
            embed_model: str = "qwen3-embedding:0.6b",
            index_name: str = "vector_index"
    ):
        if not settings.MONGODB_ATLAS_URI:
            raise ValueError("Missing MONGODB_ATLAS_URI in settings")

        self.index_name = index_name
        self.embeddings = OllamaEmbeddings(model=embed_model)
        self.client = MongoClient(settings.MONGODB_ATLAS_URI)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

        # Khởi tạo LangChain VectorStore
        self.vector_store = MongoDBAtlasVectorSearch(
            collection=self.collection,
            embedding=self.embeddings,
            index_name=self.index_name,
            embedding_key="embedding",
            text_key="text",
            metadata_key="metadata"
        )

    def setup_vector_index(self):
        """
        Tạo Vector Search Index trực tiếp từ code
        """
        # 1. Lấy dimension thực tế của model
        sample_emb = self.embeddings.embed_query("test")
        dimension = len(sample_emb)
        logger.info(f"📐 Model dimension detected: {dimension}")

        # 2. Định nghĩa cấu hình index
        index_definition = {
            "fields": [
                {
                    "numDimensions": dimension,
                    "path": "embedding",
                    "similarity": "cosine",
                    "type": "vector"
                }
            ]
        }

        # 3. Gửi lệnh tạo index lên Atlas
        try:
            # Kiểm tra xem index đã tồn tại chưa
            existing_indexes = list(self.collection.list_search_indexes())
            if any(idx['name'] == self.index_name for idx in existing_indexes):
                logger.info(f"ℹ️ Index '{self.index_name}' đã tồn tại, bỏ qua bước tạo.")
                return

            logger.info(f"🏗️ Đang tạo Vector Index '{self.index_name}' trên Atlas...")
            search_index_model = SearchIndexModel(
                definition=index_definition,
                name=self.index_name,
                type="vectorSearch"
            )
            self.collection.create_search_index(model=search_index_model)

            # Đợi index chuyển sang trạng thái READY (Atlas cần thời gian build)
            self._wait_for_index_ready()

        except Exception as e:
            logger.error(f"❌ Lỗi khi tạo index: {e}")

    def _wait_for_index_ready(self):
        logger.info("⏳ Đang đợi Atlas build index (có thể mất 1-2 phút)...")
        while True:
            indexes = list(self.collection.list_search_indexes(self.index_name))
            if indexes and indexes[0].get("queryable"):
                logger.info("✅ Index đã READY và có thể tìm kiếm!")
                break
            time.sleep(5)

    def load_cases_from_yaml(self, yaml_filename: str = "cases.yaml", reset_first: bool = False):
        yaml_path = Path(settings.DATA_ROOT) / yaml_filename
        if not yaml_path.exists(): raise FileNotFoundError(f"❌ Không thấy file: {yaml_path}")

        with open(yaml_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        cases = data.get("cases", [])
        if reset_first:
            self.collection.delete_many({})
            logger.info("🗑️ Đã reset data")

        documents = []
        metadatas = []
        ids = []

        for case in cases:
            content = f"Problem: {case.get('clarified_problem')}\nSolution: {case.get('solution')}"
            documents.append(content)
            metadatas.append({"case_id": case.get("case_id"), "full_case": case})
            ids.append(str(case.get("case_id")))

        if documents:
            self.vector_store.add_texts(texts=documents, metadatas=metadatas, ids=ids)
            logger.info(f"🎉 Đã nạp {len(documents)} cases.")

    def similarity_search(self, query: str, limit: int = 5) -> List[Dict]:
        logger.info(f"[SEARCH] Query: '{query[:50]}...'")
        try:
            # FIX: Dùng similarity_search_with_score để có score
            results = self.vector_store.similarity_search_with_score(query=query, k=limit)

            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    "text": doc.page_content,
                    "metadata": doc.metadata,
                    "score": score
                })
            return formatted_results
        except Exception as e:
            logger.error(f"[SEARCH ERROR] {e}")
            return []


# if __name__ == "__main__":
#     manager = MongoDBVectorManager()
#
#     # BƯỚC QUAN TRỌNG: Gọi hàm tạo index bằng code
#     manager.setup_vector_index()
#
#     # Nạp data
#     manager.load_cases_from_yaml(reset_first=True)
#
#     # Test search
#     test_query = "Giao dịch ảnh hưởng đến stock mã HNI007230700"
#     results = manager.similarity_search(query=test_query)
#
#     for res in results:
#         print(f"[{res['score']:.4f}] ID: {res['metadata']['case_id']}")