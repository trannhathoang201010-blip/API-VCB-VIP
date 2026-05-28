from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/')
def home():
    return "Cổng nhận tin nhắn SMS Vietcombank đang hoạt động ngon lành!"

@app.route('/webhook', methods=['POST'])
def receive_sms():
    try:
        # Lấy dữ liệu JSON do iPhone gửi sang
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"status": "error", "message": "Không nhận được dữ liệu"}), 400
            
        sms_content = data['message']
        print(f"📩 Đã nhận tin nhắn từ iPhone: {sms_content}")

        # --- REGEX BÓC TÁCH NỘI DUNG TIN NHẮN SMS VIETCOMBANK ---
        # Mẫu tin nhắn cộng tiền VCB: "VCB: CC: 123456789 VND; GD: 012345; ND: NAP TIEN HOANG"
        # Hoặc: "Mã GD 12345. Số tiền +100,000 VND. ND: NAP TIEN CUA KHACH"
        
        # 1. Tìm số tiền (bắt các chuỗi đứng sau dấu +)
        money_match = re.search(r'\+([\d.,]+)', sms_content)
        
        # 2. Tìm nội dung chuyển khoản (đứng sau chữ ND: hoặc Noi dung:)
        comment_match = re.search(r'(?:ND|Nội dung|Nd)[:\s]*([^\n;]+)', sms_content, re.IGNORECASE)
        
        # 3. Tìm mã giao dịch / số lệnh (đứng sau chữ GD: hoặc Mã GD:)
        tran_match = re.search(r'(?:Mã GD|GD)[:\s]*([\w\d]+)', sms_content, re.IGNORECASE)

        if money_match:
            # Làm sạch số tiền (xóa dấu chấm, dấu phẩy nếu có để đưa về dạng số thuần)
            money = money_match.group(1).replace('.', '').replace(',', '')
            comment = comment_match.group(1).strip() if comment_match else "Không có nội dung"
            tran_id = tran_match.group(1).strip() if tran_match else "Không rõ"

            print(f"💰 --- CÓ TIỀN VÀO VIETCOMBANK ---")
            print(f"Mã giao dịch: {tran_id}")
            print(f"Số tiền nhận: {money} VND")
            print(f"Nội dung CK: {comment}")
            print(f"---------------------------------")

            # -------------------------------------------------------------
            # [TẠI ĐÂY]: Bạn có thể viết thêm code kết nối Database 
            # để tự động cộng tiền cho khách dựa vào 'comment' và 'money'
            # -------------------------------------------------------------

            return jsonify({"status": "success", "message": "Đã xử lý giao dịch thành công"}), 200
        else:
            print("⚠️ Tin nhắn nhận được không phải là tin nhắn cộng tiền hợp lệ.")
            return jsonify({"status": "ignored", "message": "Không phải tin nhắn cộng tiền"}), 200

    except Exception as e:
        print(f"❌ Lỗi xử lý Webhook trên Render: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # Chạy trên cổng 10000 mặc định của Render
    app.run(host='0.0.0.0', port=10000)
