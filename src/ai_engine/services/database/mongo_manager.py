# Logic khởi tạo, tìm kiếm (Query) - Phiên bản TEST & RESET
from pymongo import MongoClient
import os
import logging
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
import numpy as np
from pymongo.operations import SearchIndexModel

logger = logging.getLogger("ai_service.database.mongo_manager")

from ai_engine.core.config import settings

import ollama


class MongoDBVectorManager:
    def __init__(self,
                 db_name: str = "AI_Assistance",
                 collection_name: str = "AI_Service",
                 embed_model: str = "qwen3-embedding:0.6b",
                 dimensions: int = 1024,
    ):
        if not settings.MONGODB_ATLAS_URI:
            raise ValueError("Missing MONGODB_ATLAS_URI in settings")
        self.client = MongoClient(settings.MONGODB_ATLAS_URI, serverSelectionTimeoutMS=10000)
        try:
            self.db = self.client[db_name]

            # Kiểm tra xem collection có tồn tại trong danh sách thực tế không
            existing_collections = self.db.list_collection_names()

            if collection_name not in existing_collections:
                logger.warning(
                    f"⚠️ Collection '{collection_name}' chưa tồn tại. Sẽ được tạo khi insert dữ liệu")
            else:
                logger.info(f"✅ Connected: {db_name}{collection_name}")
            self.embed_model = embed_model
            self.dimensions = dimensions
            self.collection = self.db[collection_name]
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")

    # Hàm bổ trợ để lấy embedding từ Ollama
    def get_embedding(self, text: str) -> List[float]:
        """Create embedding & Normalize (increase accuracy cosine)"""
        try:
            response = ollama.embeddings(model=self.embed_model, prompt=text.strip())
            emb = np.array(response["embedding"], dtype=np.float32)
            norm = np.linalg.norm(emb)
            if norm > 0:
                emb = emb / norm
            return emb.tolist()
        except Exception as e:
            logger.error(f"Error getting embedding: {text[:50]}... {e}")
            return [0.0] * self.dimensions # fallback

    def create_vector_index(self,
                            index_name: str = "vector_index",
                            embedding_field: str = "embedding",
                            similarity: str = "cosine",
                            wait_timeout: int = 120
    ):
        """Create index"""
        definition = {
            "fields": {
                "type": "vector",
                "path": embedding_field,
                "numDimensions": self.dimensions,
                "similarity": similarity,
            }
        }
        search_index_model = SearchIndexModel(definition=definition, name=index_name, type="vectorSearch")

        try:
            result = self.collection.create_search_index(model=search_index_model)
            logger.info(f"Creating index '{result}'... wait for sync...")
            start = time.time()
            while time.time() - start < wait_timeout:  # Timeout 2 phút
                indices = list(self.collection.list_search_indexes(result))
                if indices and indices[0].get("queryable", False):
                    logger.info(f"✅ Index '{result}' is queryable!")
                    return
                time.sleep(5)
            raise TimeoutError(f"Index {index_name} không queryable sau {wait_timeout}s")
        except Exception as e:
            if "already exists" in str(e):
                logger.info(f"Index '{index_name}' already exists!")
            else:
                logger.error(f"Caught exception: {e}")
                raise

    def drop_search_index_safe(self, index_name: str):
        """Drop index nếu tồn tại, không lỗi nếu không có"""
        try:
            self.collection.drop_search_index(index_name)
            logger.info(f"Đã drop index '{index_name}'")
            time.sleep(5)  # Chờ một chút
        except Exception as e:
            if "not found" in str(e).lower():
                logger.info(f"Index '{index_name}' không tồn tại, bỏ qua drop.")
            else:
                logger.error(f"Lỗi drop index: {e}")

    def add_text_chunks(self,
                        texts: List[str],
                        metadatas: Optional[List[dict]] = None,
                        batch_size: int = 50
    ):
        """Thêm nhiều text -> tự động embed bằng Ollama -> insert vào MongoDB"""
        if metadatas is None:
            metadatas = [{} for _ in texts]
        inserted = 0
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_meta = metadatas[i:i + batch_size]

            batch_embs = [self.get_embedding(txt) for txt in batch_texts]

            docs = [{
                "text": txt,
                "embedding": emb,
                "metadata": meta,
                "created_at": datetime.utcnow(),
                }
                for txt, emb, meta in zip(batch_texts, batch_embs, batch_meta)
            ]

            if docs:
                result = self.collection.insert_many(docs)
                inserted += len(result.inserted_ids)
                logger.info(f"Inserted {i//batch_size + 1} documents: {len(result.inserted_ids)} docs")

    def similarity_search(self,
                          query: str,
                          limit: int = 5,
                          filter_query: Optional[Dict] = None,
                          index_name: str = "vec_test_1024",
                          num_candidates_multiplier: int = 20
    ) -> List[Dict]:
        query_embedding = self.get_embedding(query)
        pipeline = [
            {
                "$vectorSearch": {
                    "index": index_name,
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": max(100, limit * num_candidates_multiplier),  # Tăng để chắc chắn
                    "limit": limit,
                    "filter": filter_query or {}
                }
            },
            {
                "$project": {
                    "text": 1,
                    "metadata": 1,
                    "score": {"$meta": "vectorSearchScore"},
                    "_id": 0
                }
            }
        ]

        try:
            results = list(self.collection.aggregate(pipeline))
            logger.info(f"Vector search '{query[:50]}...' {len(results)} kết quả")
            return results
        except Exception as e:
            logger.error(f"Lỗi aggregate: {e}")
            return []

    def add_documents(self, docs: List[Dict]):
        for doc in docs:
            doc.setdefault("created_at", datetime.utcnow())
        result = self.collection.insert_many(docs)
        logger.info(f"Đã insert {len(result.inserted_ids)} documents")
        return len(result.inserted_ids)

# ------------------- TEST & RESET -------------------
if __name__ == "__main__":
    manager = MongoDBVectorManager(collection_name="AI_Service")

    INDEX_NAME = "vector_index"

    # Reset nếu cần (comment nếu không muốn xóa data)
    # manager.drop_search_index_safe(INDEX_NAME)
    # manager.collection.delete_many({})
    # print("Reset xong, docs:", manager.collection.count_documents({}))

    # Tạo index (chạy nếu chưa có)
    # manager.create_vector_index(index_name=INDEX_NAME)

    # Test add & search
    # test_texts = [
    #     "Xin chào thế giới, đây là test vector search MongoDB Atlas",
    #     "MongoDB Atlas hỗ trợ vector search rất tốt cho RAG",
    #     "Ollama + qwen3-embedding hoạt động ổn với Atlas",
    # ]
    # test_metas = [{"user_id": "test_user"} for _ in test_texts]
    #
    # manager.add_text_chunks(test_texts, test_metas)

    # Chờ sync (nếu cần thêm)
    # time.sleep(15)

    results = manager.similarity_search(
        query="Hello",
        limit=5,
        filter_query={},  # hoặc {"metadata.user_id": "test_user"}
        index_name=INDEX_NAME,
    )

    logger.info("\nKẾT QUẢ:")
    for r in results:
        logger.info(f"Score: {r['score']:.4f} | {r['text'][:80]}... | Metadata: {r['metadata']}")