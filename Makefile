include .env
export

.PHONY: serve ingest setup-db

# Khởi động server
serve:
	uvicorn src.main:app --port 8000 --reload

# Cài đặt nhanh môi trường
install:
		pip install -r requirements.txt
