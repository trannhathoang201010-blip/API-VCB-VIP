const express = require('express');
const axios = require('axios');
const qs = require('qs');

const app = express();
const PORT = process.env.PORT || 3000;

// Cho phép Server đọc dữ liệu JSON gửi lên (nếu có)
app.use(express.json());

// Định nghĩa API lấy lịch sử biến động số dư Vietcombank
app.get('/api/vcb-history', async (req, res) => {
    try {
        // CHÚ Ý: Điền các tham số trong mục "Preview Form" (Request Body) vào đây nếu có
        const payload = qs.stringify({
            // 'mobile': '09xxxxxxxx',
            // 'page': '1'
        });

        const config = {
            method: 'post',
            url: 'https://vcbottapi.vnpay.vn/vntservice/messageService/getpeddingmsgV2/907436/',
            headers: { 
                'X-User-ID': '4fpzMunUovRseVMb0PMphCK1M55ajGqREizIJeEDmpCDz94T1/IUsEEC+8m2WQSXMYcluD0Vw1wJs3xAKannZs+APIOa5Ww=', 
                'Accept': 'application/json', 
                'Authorization': 'Basic MjNjZjAxNGM4OTc3NDJmNGE4YjJkYWYwYmYmNmNkNjU5OGU2YWU4YWI0NjRmNGEwYW2FjMGU0MGQ3YzliNDM2YWI=', 
                'X-Requested-Timestamp': '177894052968', 
                'Accept-Language': 'vi-VN,vi;q=0.9', 
                'Accept-Encoding': 'gzip, deflate, br', 
                'Cache-Control': 'no-store', 
                'Content-Type': 'application/x-www-form-urlencoded', 
                'User-Agent': 'VCBDigibank/11 CFNetwork/1410.1 Darwin/22.6.0', 
                'Connection': 'keep-alive'
            },
            data: payload
        };

        // Gửi request đến server VNPAY/Vietcombank
        const response = await axios(config);
        
        // Trả về kết quả trực tiếp cho người gọi API của bạn
        return res.status(200).json({
            success: true,
            data: response.data
        });

    } catch (error) {
        console.error("Lỗi gọi API VCB:", error.message);
        return res.status(500).json({
            success: false,
            message: "Không thể lấy dữ liệu từ Vietcombank",
            error: error.message
        });
    }
});

// Khởi chạy server
app.listen(PORT, () => {
    console.log(`API đang chạy tại cổng ${PORT}`);
});
