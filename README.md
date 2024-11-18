![image](https://github.com/user-attachments/assets/6a82f2fe-f89d-4244-b3f8-7b8532af51b9)# Ứng dụng nhận diện biển số xe
## Đầu tiên
- Bạn cần tải video xuống và đổi tên thành demo: `demo`.  
Link tải xuống [Here](https://www.youtube.com/watch?v=o4bRh9zzJaU)  
- Bạn bỏ file đã tải vào `demo folder`  
- Nếu bạn muốn sử dụng camera của mình làm đầu vào, hãy thay đổi như sau: `main.py`:  
![Đổi camera](https://github.com/user-attachments/assets/771f67cd-97c0-4495-99f0-700b7d18c480)

- Sau khi bạn khởi chạy tệp chính, một cửa sổ sẽ xuất hiện nơi bạn có thể nhập thiết bị bạn muốn làm đầu vào. *(0-99: your webcacme, or rtsp : IP Camera)*  

## Thứ 2
- Thay đổi server, database, username, password database và driver ODBC tại `license_plate_DB.py`
*translate it to vietnamese If you don't have an account or don't want to log in, it will take about 15 seconds to start the software because it can't connect to the database
Dưới đây là bản dịch tiếng Việt của đoạn văn bạn cung cấp:

Nếu bạn không có tài khoản hoặc không muốn đăng nhập, phần mềm sẽ mất khoảng 15 giây để khởi động vì không thể kết nối với cơ sở dữ liệu.*

### Hiện tại, phần mềm đang gặp nhiều lỗi và vấn đề về hiệu suất. Chúng tôi mong nhận được sự đóng góp và lời khuyên từ mọi người.
* Nếu bạn nhấn nút quick_view, một cửa sổ mới sẽ xuất hiện để người khác dễ dàng xem, tuy nhiên nó đang gây ra lỗi khiến một trong hai camera đầu tiên trong cửa sổ chính bị đóng băng hình ảnh.
* Có một lỗi rò rỉ RAM với tần suất tăng 0,1% trong 1 phút, tôi nghĩ vấn đề này là do sử dụng cv2.
* Khi đóng gói với auto-py-to-exe, sử dụng chức năng quẹt thẻ lần đầu tiên sẽ khiến ứng dụng mở lại.

## Thứ 3
- Cam mặc định là video demo (thay số trong main.py để train)
- Nhập 0 & 1 phần chọn camera để được xem app
