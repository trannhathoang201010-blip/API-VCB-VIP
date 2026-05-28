from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Mảng lưu lịch sử giao dịch (Fake mẫu 1 cái để fen thấy giao diện lúc đầu)
momo_history = [
    {
        "tran_id": "22147483647",
        "amount": "+20,000 VND",
        "content": "Giao dich mau - He thong da san sang"
    }
]

# GIAO DIỆN WEB ĐẸP ĐẼ, GỌN GÀNG (HIỂN THỊ KHI VÀO TRANG CHỦ)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lịch Sử Nhận Tiền MoMo</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f6f9;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
        }
        .container {
            width: 100%;
            max-width: 600px;
            background: #ffffff;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #f0f2f5;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }
        .header h2 {
            margin: 0;
            color: #a50064; /* Màu hồng MoMo */
            font-size: 20px;
        }
        .status {
            background-color: #e6f7ed;
            color: #2e7d32;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }
        .card {
            background: #fff;
            border: 1px solid #eef0f4;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: transform 0.2s;
        }
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        }
        .left-info {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        .content {
            font-weight: 600;
            color: #2c3e50;
            font-size: 15px;
        }
        .txid {
            color: #95a5a6;
            font-size: 12px;
        }
        .amount {
            color: #2e7d32;
            font-weight: bold;
            font-size: 16px;
            background: #edf7ed;
            padding: 6px 12px;
            border-radius: 8px;
        }
        .no-data {
            text-align: center;
            color: #7f8c8d;
            padding: 40px 0;
        }
    </style>
    <script>
        setInterval(function(){
            window.location.reload();
        }, 5000);
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🔮 LỊCH SỬ MOMO REALTIME</h2>
            <span class="status">Đang quét ngầm...</span>
        </div>
        
        <div id="history-list">
            {% if logs %}
                {% for tx in logs %}
                <div class="card">
                    <div class="left-info">
                        <span class="content">{{ tx.content }}</span>
                        <span class="txid">Mã GD: {{ tx.tran_id }}</span>
                    </div>
                    <div class="amount">{{ tx.amount }}</div>
                </div>
                {% endfor %}
            {% else %}
                <div class="no-data">Chưa có giao dịch nào phát sinh...</div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

# TRANG CHỦ HIỂN THỊ GIAO DIỆN ĐẸP
@app.route('/')
def home():
    global momo_history
    return render_template_string(HTML_TEMPLATE, logs=momo_history)

# CỔNG WEBHOOK NHẬN DỮ LIỆU TỪ TRUNG GIAN BẮN SANG
@app.route('/webhook', methods=['POST'])
def receive_momo_webhook():
    global momo_history
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": 1, "message": "Dữ liệu trống"}), 400

        # Bóc tách an toàn các trường số tiền, nội dung, mã GD
        amount = data.get("amount") or data.get("money") or data.get("Data", {}).get("amount", 0)
        description = data.get("description") or data.get("comment") or data.get("Data", {}).get("description", "Chuyển tiền MoMo")
        tran_id = data.get("tranId") or data.get("id") or data.get("Data", {}).get("tranId", "Không rõ")

        try:
            amount = int(amount)
        except:
            amount = 0

        # Nếu có tiền vào thật, xóa cái giao dịch mẫu đầu tiên đi và ghi đè dữ liệu thật
        if amount > 0:
            if len(momo_history) == 1 and momo_history[0]["tran_id"] == "22147483647":
                momo_history.clear()

            log_item = {
                "tran_id": str(tran_id),
                "amount": f"+{amount:,} VND",
                "content": description
            }
            momo_history.insert(0, log_item)
            return jsonify({"error": 0, "message": "Thành công"}), 200
            
        return jsonify({"error": 1, "message": "Số tiền bằng 0"}), 400

    except Exception as e:
        return jsonify({"error": 500, "message": str(e)}), 500

# API BACKUP NẾU VẪN MUỐN XEM DẠNG JSON
@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify({"transactions": momo_history}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
