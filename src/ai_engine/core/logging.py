import logging
import sys

from contextvars import ContextVar

# Biến này dùng để lưu ID của mỗi request, giúp đơn giản hóa trace log
request_id_var: ContextVar[str] = ContextVar("requests_id", default="Global")

# Filter để bốc Request ID bỏ vào log
class RequestIDFilter(logging.Filter):
    def filter(self, record):
        # Lấy ID từ ContextVar ném vào bản ghi log
        record.request_id = request_id_var.get("SYSTEM")
        return True


# 3) Formatter có màu sắc cho đẹp
class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[37m",  # Xám
        "INFO": "\033[36m",  # Xanh cực quang (Cyan)
        "WARNING": "\033[33m",  # Vàng
        "ERROR": "\033[31m",  # Đỏ
        "CRITICAL": "\033[41m"  # Nền đỏ
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        # Định dạng chuẩn: Thời gian | RequestID | Level | Tên Logger | Tin nhắn
        format_str = f"{color}%(asctime)s | %(request_id)s | %(levelname)s | %(name)s | %(message)s{self.RESET}"

        # Tạo tạm một formatter để format nội dung
        formatter = logging.Formatter(format_str, datefmt="%H:%M:%S")
        return formatter.format(record)


def setup_logging(level: int = logging.INFO) -> None:
    """
    Thiết lập logging theo cách thủ công để tránh lỗi dictConfig trên Python 3.13.
    """
    # Khởi tạo Handler xuất ra console
    handler = logging.StreamHandler(sys.stdout)

    # Thêm filter và formatter vào handler
    handler.addFilter(RequestIDFilter())
    handler.setFormatter(ColorFormatter())

    # Cấu hình Root Logger (thằng trùm cuối)
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Xoá các handler cũ để tránh bị lặp log
    root_logger.handlers = []
    root_logger.addHandler(handler)

    # Ép các logger của uvicorn và ai_engine phải dùng chung cấu hình này
    for logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access", "ai_engine"]:
        specific_logger = logging.getLogger(logger_name)
        specific_logger.handlers = []
        specific_logger.propagate = True  # Cho phép log bay ngược lên root_logger để dùng chung handler

    root_logger.info("✅ Logging system initialized (No-dictConfig mode).")
