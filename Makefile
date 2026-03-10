# Load biến môi trường từ file .env
include .env
export $(shell sed 's/=.*//' .env)

.PHONY: serve tunnel dev install

# 1. Khởi động server Uvicorn
serve:
	uvicorn src.main:app --port 8000 --reload

# 2. Khởi động Ngrok (tunnel)
# Lưu ý: Port phải khớp với port của Uvicorn
tunnel:
	ngrok http 8000

# 3. Cách setup "1 lần ăn ngay": Chạy cả 2 cùng lúc
# -j 2 cho phép chạy 2 command song song
dev:
	make -j 2 serve tunnel

# Cài đặt môi trường
install:
	pip install -r requirements.txt
	@echo "Đừng quên chạy 'ngrok config add-authtoken <your-token>' nếu là máy mới nhé!"