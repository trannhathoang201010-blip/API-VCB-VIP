from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

# Cấu hình múi giờ Việt Nam
VN_TZ = pytz.timezone('Asia/Ho_Chi_Minh')

@app.route('/')
def home():
    return "Cổng API Gốc Giả Lập MoMo đang trực tuyến 24/7!"

@app.route('/api/vcb-history', methods=['GET'])
def get_momo_history():
    # 1. Tự động lấy mốc thời gian thực theo đúng định dạng MoMo yêu cầu
    now = datetime.now(VN_TZ)
    start_date = (now - timedelta(days=30)).strftime("%Y-%m-%dT23:59:59")
    end_date = now.strftime("%Y-%m-%dT23:59:59")
    chunk_start = now.strftime("%Y-%m-%dT%H:%M:%S")
    
    # 2. Đường dẫn API MoMo kèm tham số động
    url = "https://api.momo.vn/transhis/api/transhis/chunks"
    params = {
        "requestId": f"refresh_{int(now.timestamp() * 1000)}",
        "startDate": start_date,
        "endDate": end_date,
        "chunkStart": chunk_start,
        "chunkSize": "20",
        "dbPart": "0",
        "client": "sync_app",
        "page": "0"
    }
    
    # 3. Bộ Headers bóc tách từ iPhone X của fen
    headers = {
        "Host": "api.momo.vn",
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "max-age=3600",
        "M-Timezone": "Asia/Ho_Chi_Minh",
        "User-Agent": "MoMoPlatform Store/5.9.0.50900 CFNetwork/1410.1 Darwin/22.6.0 (iPhone X iOS/16.7.11)",
        "wbmtd": "pVKE261yTTxJqHrVAxciDWebkO7nPT93wRglZshr48VuDClVmEPNltUZs+cosjz3d2aPNeQrm5st9qlw8/JSIFVCVqniV/dUJgCntwr4iUH8aCvVv5OowXsaOR8IqnieGjShUgJx6L/+sOWzyARxFZNkxW12bvKdUnY/K6x3h6fmaetf0EJYgiMKZ7H3UNshaVBoJrJFfwKRteHy0hVc5fM+iWZ/kjJqTuHh6Y8ofj/S/UvJsQoJYPQwKxFb7bg+vqjs+d3VRtomyH5kQIGG17agd3mklCms2LD1rg6MdWc+nZuHqWbchxv4/6ijTZRmcjXioPSJ9QOtkA8wSOp4QdmzUP3C+A+ufHsagi7EuTD61DwBGNagZuTzCv90aTS5rRwDTGgcGIYplTLBTG7TiT6yB5jGyAnz1Pxmxc+yB7ELnX4KilInsF6AALAaULU7WMqC7unhcglP7FOXqSU88SDkBrMYDrPdtHSOcdyinjAZBy5tg0+sYpZRLEz9ooyg/YANxNFYHAY08tleMvf0zgq7G60xS3ULUX7RwnH3XI5PlRjTzC8eJgG9zrkrLML6CoJzXItnu9z39yDST5TyC+BFyMRmC8ueuGSWE7fsJYcmWBgxi3GYdUMjuJHL5QJNzuNfdy8KH3sHiN+Tylmvxj7xYiFgj8KJylhDqDCGxkyjhpcPZSfJ+6mpn4/eYaZKGcregD5RvjBAjr96BXM8wHiDIHaZMSj1AbB9/KBdK7+DIBn1RKzsGmJk+1dQ89Wy9yE2LF2XfuQ6UeQOtcdMxuECj2a67o6AnTtwOsPIRrU11rRgmdJDmHdBkll6VUS6zefnBjKIZaeEbLr8JaJ6/7hGLaoWYmP9Po25Hrp2UxkMsV2NLtfo2ecgyEu/gQMa2C13IAObzhD0mhXyrxR5k7OFPY/Drk5h8YyoL+CI3Jr0/f6L1Heal70GkxV3WhW0",
        "app_version": "50900",
        "wbmky": "xs5mz5symt55K/Y98J0vi84hz3TgzbSatjpvLbSIjK7NiHAKOMZn3lDWbLUPxX1NzCZ0mMoqqOljow8/4wwXl/mqAIRHfMGAtpyoGtPYTa+OkpqtgE51Zp3MakcWqPdMFQ7p03KF3+qps9Vi5Jpz9Dpdg1e4D8v7F31/3sc6M8eTQxTzzCmo49bSnBsp5H3IziwYd97COYe4mRsFSH9i8NHbpSbceT6VkFJgBdiiWnHgLhyCNM7zLeFTyyW3ughXGpfUkTx6uOD7WlaA0LtMLvp3VwylJvAbaU5/GAlj/+WItWtyGVyXSFHo0Mg0ky50Ohs2k+zX5BUJL8QD7JECEw==",
        "M-RequestId": "CCBDF078-69B6-49DD-9612-E5E2C4F744E5.1779924636822",
        "M-Timestamp": "1779924636822",
        "wbCode": "0&1779924636822",
        "baggage": "sentry-environment=PRODUCTION,sentry-public_key=6e80c9f01f2440c9be5b37606028f996,sentry-release=vn.momo.platform.ios%405.9.0%2B50900,sentry-trace_id=214403ee665b4872bb4cf9c70317e0f5",
        "M-IsEncrypt": "true",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyIjoiMDE2ODI5NjIxODIiLCJpbWVpIjoiNTAxMDMtMGUyYjQ4NTRkNzdhNTAyMWYzYTQ0N2JlN2ZkOTY1NGYwMDQ2ZDZjNDVkZWI0YWI5YzhiNjQwYjUwNzgxN2VlZiIsImhJbWVpIjoiQmV4RjYvbnliOW9mNlUySGVJZVBwQnBOdlY5dk1TZE1wRXZuMTdrVkY3bnpxWW1Sdis3dTRCMnVmTmFFLzV0TkswdTd0eEJKRG40S280bWRnVkRQV05wTVF4d01CZ3NvYUc1M3gzeGc3REU9IiwiTUFQX1NBQ09NX0NBUkQiOjAsIk5BTUUiOiJUcuG6p24gTmjhuq10IEhvw6BuZyIsIkRFVklDRV9PUyI6ImlvcyIsIkFQUF9WRVIiOjUwOTAwLCJhZ2VudF9pZCI6MTEwMzM1MTY0LCJzZXNzaW9uS2V5IjoiZFNYdnR0Q2JoSy84cEpYZklFQUcrVG1HRUt1RXc0YVBuSmk5UTU0dGlsUU9peUVnNVRWdFR3PT0iLCJ1c2VyX3R5cGUiOjEsImtleSI6Im1vbW8iLCJyYXBpZF9pZCI6IjlsVGdsYWtEdktqT1BsVFlGVE1SU0U2eXo2Q0tDN1pQT2t1cFhMdzJYV3JZNkpxOUxyMmlIS0R4OGZvdEp6cmRVblJhZFFWQlBWbz0iLCJ1aWQiOiIwMTY4Mjk2MjE4MiIsImV4cCI6MTc4MDM1NjU5OX0.RG3rofit58lhxxIa0y3_9qZ0KQdrOETVsymXAskONCqDTHiBarW4je357dDpPmIt6CwKxDJok7dRwrONdEfcBmwnE07U4RPwjRGgQyZm97HqFgn4XkkoWlUn3s_XHpaxg_I4c8YHibG8kuLhfpXz2Tv1OqWuH96kQOiVUTUxTz7BCZOpFaOPr_hI5grj_1opQFgFjxGQKDyrCUPAFYuJNfFsgMWwOWl0DsLXRDpfYT_sbiZJoFOITRci7vTGw84p6NKwkOJD93GhgI63yuOZ0Pn7YrWGxI5vu3cJnBiRCMCiH91BRbYc60Jkh2BsrhAdJyzrxsepg9qgOFO0oIZMXA",
        "env": "production",
        "app_type": "production",
        "timezone": "Asia/Ho_Chi_Minh",
        "http-process-timestamp": "1779924636822",
        "M-Signature": "d+h+lEKRtBcTQDXLNU6om6SjYy7sSzU1IMerzw+gIvc=",
        "M-Lang": "vi",
        "Accept": "application/json",
        "Accept-Charset": "UTF-8",
        "sentry-trace": "214403ee665b4872bb4cf9c70317e0f5-cd8f14f6561f470f-0",
        "Accept-Language": "vi-VN,vi;q=0.9",
        "wbSign": "AIzJtFxgc12RDyVTPCJGF37jrR3d/GEleDKdg8Ua7eFmwNkKGwVMcKEC4e1/7u802su5SDXYUy32+gmsaiO5INNjdgq+NFlSx3b+jQPpaZO1/A==",
        "platform-timestamp": "1779924636824"
    }
    
    try:
        # Gọi trực tiếp lên server MoMo
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            res_json = response.json()
            # MoMo trả lịch sử trong mảng "momoMsg"
            momo_msg = res_json.get("momoMsg", [])
            
            transactions = []
            for tx in momo_msg:
                # io = 1 là tiền vào túi, io = -1 là tiền ra
                if tx.get("io") == 1:
                    transactions.append({
                        "tran_id": str(tx.get("transId")),
                        "amount": f"+{tx.get('amount', 0):,} VND",
                        "content": tx.get("comment", "Chuyển tiền đến MoMo")
                    })
                    
            return jsonify({
                "total_transactions": len(transactions),
                "transactions": transactions
            }), 200
        else:
            return jsonify({"status": "Lỗi API MoMo", "code": response.status_code, "msg": response.text}), response.status_code
            
    except Exception as e:
        return jsonify({"status": "Lỗi hệ thống server", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
