from flask import Flask, jsonify
import requests
import time
import threading

app = Flask(__name__)

# --- CẤU HÌNH SỐ TÀI KHOẢN VIETCOMBANK CỦA BẠN TẠI ĐÂY ---
VCB_ACCOUNT = "3382962182"  # Số tài khoản của bạn (lấy từ ảnh thông báo)
# -----------------------------------------------------

history_logs = []

def fetch_vcb_history_loop():
    """Hàm chạy ngầm tự động quét lịch sử Vietcombank mỗi 10 giây"""
    global history_logs
    print("🚀 Khởi động bot quét lịch sử Vietcombank tự động...")
    
    # Sử dụng API public/free ổn định để đọc lịch sử giao dịch VCB công khai
    api_url = f"https://api.web23s.com/api/vcb/{VCB_ACCOUNT}" 
    
    while True:
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Lấy danh sách giao dịch từ API trả về
                transactions = data.get("transactions", []) or data.get("data", [])
                
                new_logs = []
                for tx in transactions[:10]: # Lấy 10 giao dịch mới nhất
                    amount = tx.get("amount", "0")
                    description = tx.get("description", tx.get("content", ""))
                    tran_id = tx.get("tran_id", tx.get("reference", "Không rõ"))
                    
                    # Chỉ lọc các giao dịch cộng tiền vào (tiền vào tài khoản)
                    if "+" in str(amount) or (isinstance(amount, (int, float)) and amount > 0):
                        new_logs.append({
                            "tran_id": tran_id,
                            "amount": f"+{amount} VND",
                            "content": description
                        })
                
                if new_logs:
                    history_logs = new_logs
                    
        except Exception as e:
            print(f"⚠️ Lỗi khi quét API Vietcombank: {e}")
            
        time.sleep(10) # Cứ 10 giây tự động quét một lần

@app.route('/')
def home():
    return "Hệ thống tự động quét Vietcombank đang hoạt động ngầm 24/7!"

@app.route('/api/vcb-history', methods=['GET'])
def get_history():
    return jsonify({
        "total_transactions": len(history_logs),
        "transactions": history_logs
    }), 200

# Kích hoạt luồng chạy ngầm song song với server web
threading.Thread(target=fetch_vcb_history_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
