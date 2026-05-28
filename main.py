from flask import Flask, request, jsonify

app = Flask(__name__)

# Mảng lưu lịch sử hiển thị lên giao diện web
history_logs = []

@app.route('/')
def home():
    return "Hệ thống Webhook Vietcombank chính thức đang hoạt động!"

# CỔNG WEBHOOK CHÍNH THỨC NHẬN DỮ LIỆU TỪ CASSO/PAYOS BẮN SANG
@app.route('/webhook', methods=['POST'])
def receive_bank_webhook():
    global history_logs
    try:
        # Lấy dữ liệu cấu trúc chuẩn JSON từ Casso gửi sang
        data = request.get_json()
        
        # Kiểm tra nếu có danh sách giao dịch gửi tới
        if data and "data" in data:
            transactions = data["data"]
            
            for tx in transactions:
                amount = tx.get("amount", 0)
                description = tx.get("description", "")
                tran_id = tx.get("id", "Không rõ")
                
                # Chỉ xử lý các giao dịch TIỀN VÀO (Cộng tiền)
                if amount > 0:
                    log_item = {
                        "tran_id": str(tran_id),
                        "amount": f"+{amount:,} VND",
                        "content": description
                    }
                    # Đẩy giao dịch mới nhất lên đầu danh sách hiển thị
                    history_logs.insert(0, log_item)
            
            return jsonify({"error": 0, "message": "Xử lý thành công"}), 200
            
        return jsonify({"error": 1, "message": "Không có dữ liệu hợp lệ"}), 400

    except Exception as e:
        print(f"❌ Lỗi xử lý Webhook: {e}")
        return jsonify({"error": 500, "message": str(e)}), 500

# ĐƯỜNG DẪN XEM LỊCH SỬ TRÊN TRÌNH DUYỆT
@app.route('/api/vcb-history', methods=['GET'])
def get_history():
    return jsonify({
        "total_transactions": len(history_logs),
        "transactions": history_logs
    }), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
