# Automation test – Đăng nhập Văn phòng điện tử UTC

Dự án dùng Python, Selenium WebDriver, pytest, Excel và Allure. Các case hiện không cần tài khoản đăng nhập thật. Chrome/Edge chạy ở chế độ hiển thị mặc định để có thể quan sát thao tác.

## Cấu trúc dự án

```text
automation_test_6451071002/
├── config/
│   └── settings.py                 # URL, đường dẫn workbook, timeout
├── pages/
│   └── login_page.py               # Page Object cho trang login/khôi phục mật khẩu
├── tests/
│   └── test_login.py               # Test đọc dữ liệu từ Excel, gắn metadata Allure
├── test_cases/
│   └── login_test_cases.xlsx       # Test case và trạng thái chạy
├── utils/
│   └── excel_reader.py             # Đọc/kiểm tra Excel, cập nhật trạng thái
├── artifacts/                      # Ảnh lỗi (nếu có)
├── allure-results/                 # Kết quả thô của Allure
├── allure-report/                   # Report HTML đã tạo
├── conftest.py                     # Fixture WebDriver và tùy chọn pytest
├── pytest.ini
├── requirements.txt
└── run_tests.ps1                   # Chạy test và tạo report trên Windows
```

## Cài đặt

Mở PowerShell tại thư mục dự án:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Selenium Manager tự tìm hoặc tải driver phù hợp cho Chrome/Edge. Phần tạo report HTML cần Java và Node.js (hoặc cài riêng Allure CLI).

## Chạy test

Chạy toàn bộ case; mỗi case mở cửa sổ browser và giữ lại 5 giây sau khi chạy:

```powershell
python -m pytest
```

Chạy một case, đổi browser, chỉnh thời gian quan sát hoặc chạy ẩn:

```powershell
python -m pytest --case=TC_LOGIN_008
python -m pytest --browser=edge --pause=10
python -m pytest --headless --pause=0
```

`python test_login.py` cũng chạy pytest với các tham số tương tự. Có thể đổi URL và timeout bằng biến môi trường:

```powershell
$env:LOGIN_URL = "https://vanphongdientu.utc.edu.vn/Login"
$env:SELENIUM_WAIT_SECONDS = "30"
```

## Tạo và xem Allure report

Mỗi lượt pytest làm mới `allure-results`. Tạo report HTML bằng npx:

```powershell
npx --yes --package=allure-commandline allure generate allure-results --clean -o allure-report
```

Mở `allure-report/index.html` trong trình duyệt, hoặc dùng `allure serve allure-results` nếu Allure CLI đã cài. Có thể chạy test và tạo report liên tiếp bằng:

```powershell
.\run_tests.ps1
```

Allure Pytest ghi dữ liệu test; Allure CLI kết xuất dữ liệu đó thành HTML. CLI cần Java. Tham khảo [hướng dẫn Allure Pytest](https://allurereport.org/docs/pytest/) và [cài Allure trên Windows](https://allurereport.org/docs/v2/install-for-windows/).

## Các case hiện có

Workbook chứa 9 case: hiển thị trang login; submit khi thiếu thông tin hoặc thông tin sai; che mật khẩu; bật/tắt “Ghi nhớ tôi”; mở trang lấy lại mật khẩu; kiểm tra liên kết đăng nhập email UTC. Test không gửi thông tin đăng nhập hợp lệ và không thực hiện đăng nhập thành công.

Trạng thái `Passed`/`Failed` trong workbook được cập nhật sau mỗi lần chạy. Khi test lỗi, Allure đính kèm ảnh chụp màn hình và HTML để tiện xem nguyên nhân.
