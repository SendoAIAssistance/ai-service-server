import requests
import json
import sys

# ================== CẤU HÌNH ==================
URL = "http://127.0.0.1:8000/api/v1/chat"
CONVERSATION_ID = "test_1"
MESSAGE = "hi"
# =============================================

if __name__ == "__main__":
    print(f"🚀 Test streaming → {URL}")
    print("=" * 70)

    # Biến để kiểm soát việc in Header
    header_flags = {
        "reasoning": True,
        "chunk": True  # Hoặc 'call' tùy theo type agent bạn trả về
    }

    try:
        with requests.post(
                URL,
                data={"conversationId": CONVERSATION_ID, "message": MESSAGE},
                stream=True,
                timeout=50
        ) as r:
            r.raise_for_status()
            print("\n")
            for line in r.iter_lines():
                if not line:
                    continue

                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    try:
                        event = json.loads(line_str[6:])
                        event_type = event.get('type', '')
                        content = event.get('content', '')

                        # 1. Xử lý phần Reasoning (Thinking)
                        if "reasoning" in event_type.lower():
                            if not header_flags["reasoning"]:
                                print(f"\n\n\033[1;33m===== Reasoning =====\033[0m")  # Màu vàng cho xịn
                                header_flags["reasoning"] = True
                            sys.stdout.write(content)
                            sys.stdout.flush()

                        # 2. Xử lý phần Nội dung trả về (Final Answer)
                        elif event_type == "text":  # Tùy vào type bạn yield từ server
                            if not header_flags["chunk"]:
                                print(f"\n\n\033[1;32m===== Response =====\033[0m")  # Màu xanh lá
                                header_flags["chunk"] = True

                            # Nếu content là object (content_blocks), lấy text ra
                            text = content if isinstance(content, str) else str(content)
                            sys.stdout.write(text)
                            sys.stdout.flush()

                        # 3. Kết thúc
                        elif event_type == 'done':
                            print(f"\n\n\033[1;34m" + "=" * 30 + " FINISHED " + "=" * 30 + "\033[0m")
                            break

                    except Exception as e:
                        # Nếu không parse được JSON thì in thô ra để debug
                        pass

    except Exception as e:
        print(f"\n❌ Lỗi: {e}")