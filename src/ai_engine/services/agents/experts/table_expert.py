import pandas as pd
import io
import logging
from typing import Dict

logger = logging.getLogger("ai_engine.experts.table")

class TableExpert:
    def __init__(self):
        self.name = "Table Data Specialist"

    async def analyze(self, file_data: bytes) -> Dict:
        """
        Đọc dữ liệu bảng và tìm các dòng có dấu hiệu lỗi (status code >= 400, etc.)
        """
        thought = "Expert Table: Đang bắt đầu đọc dữ liệu bảng..."
        try:
            # 1. Đọc bytes vào Pandas (Hỗ trợ cả CSV và Excel)
            try:
                df = pd.read_excel(io.BytesIO(file_data))
            except:
                # Nếu không phải Excel thì thử CSV
                df = pd.read_csv(io.BytesIO(file_data), low_memory=False)

            # 2. TODO: Logic soi lỗi
            #  (Sample)
            critical_rows = df[df.apply(lambda row: any(str(val) in ['500', '502', 'Error', 'Failed'] for val in row), axis=1)]

            if not critical_rows.empty:
                summary = f"Phát hiện {len(critical_rows)} dòng có lỗi nghiêm trọng.\n"
                summary += critical_rows.head(5).to_string()
                thought += f"\n- Phát hiện lỗi trong data. Tổng cộng {len(critical_rows)} lỗi."
            else:
                summary = "Dữ liệu bảng có vẻ sạch, không phát hiện lỗi bất thường."
                thought += "\n- Không tìm thấy lỗi trong các dòng dữ liệu."
            return {
                "file_context": summary,
                "thinking_logs": [thought]
            }
        except Exception as e:
            logger.error(f"Lỗi khi xử lý bảng: {str(e)}")
            return {
                "file_context": "Không thể đọc dữ liệu từ file này.",
                "thinking_logs": [f"Expert Table: Gặp lỗi khi đọc file - {str(e)}"]
            }