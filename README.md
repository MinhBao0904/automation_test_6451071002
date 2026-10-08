# Selenium automation: UTC e-Office login

Bộ kiểm thử Python đọc test case từ `test_cases/login_test_cases.xlsx` và mở Chrome hiển thị để theo dõi.

## Chạy

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python test_login.py
```

Chạy riêng một case: `python test_login.py --case TC_LOGIN_001`. Đổi sang Edge bằng `--browser edge`; điều chỉnh thời gian quan sát bằng `--pause 10` (mặc định 5 giây). Selenium Manager tự tìm hoặc tải WebDriver tương thích khi cần. Mỗi case chạy trong cửa sổ trình duyệt mới. Có thể đặt `LOGIN_URL` để đổi URL kiểm thử.

Các case hiện tập trung vào giao diện và xử lý đăng nhập bị từ chối, không cần tài khoản thật. Để kiểm thử đăng nhập thành công, hãy thêm tài khoản kiểm thử được cấp phép vào môi trường cục bộ; không lưu thông tin xác thực vào Excel hoặc Git.
