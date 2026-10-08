# Automation test: đăng nhập Văn phòng điện tử UTC

Bộ test dùng Python, Selenium, pytest và Excel. Trình duyệt Chrome hiển thị trực tiếp; sau mỗi case cửa sổ chờ 5 giây (có thể chỉnh) để bạn theo dõi. Test case và trạng thái chạy được lưu tại `test_cases/login_test_cases.xlsx`.

## Cài đặt

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Chạy test và tạo Allure results

```powershell
python -m pytest
```

Pytest ghi dữ liệu report vào `allure-results` và xóa kết quả cũ trước mỗi lượt chạy. Chạy một case bằng:

```powershell
python -m pytest -k TC_LOGIN_006
```

Chọn Edge hoặc tăng thời gian quan sát:

```powershell
python -m pytest --browser=edge --pause=10
```

`python test_login.py` cũng chạy pytest với các tham số tương tự. Selenium Manager tự tìm hoặc tải driver tương thích. Có thể đặt biến môi trường `LOGIN_URL` để kiểm tra một môi trường khác.

## Xem HTML report

Để tạo và mở report HTML, cài Allure Report CLI và Java 8 trở lên, sau đó chạy:

```powershell
allure serve allure-results
```

Hoặc tạo report tĩnh để mở sau:

```powershell
allure generate allure-results --clean -o allure-report
allure open allure-report
```

Nếu đã có Node.js và Java nhưng chưa cài Allure CLI toàn máy, có thể dùng npx:

```powershell
npx --yes --package=allure-commandline allure generate allure-results --clean -o allure-report
```

Allure Pytest tạo dữ liệu kết quả; Allure CLI chuyển dữ liệu đó thành report HTML. Cài CLI trên Windows có thể dùng `scoop install allure`; xem [hướng dẫn cài Allure cho Windows](https://allurereport.org/docs/v2/install-for-windows/).

## Các test case không cần tài khoản

Workbook có các case kiểm tra tải trang, bỏ trống hoặc nhập sai thông tin, kiểu che mật khẩu, checkbox ghi nhớ đăng nhập, liên kết lấy lại mật khẩu và liên kết đăng nhập email UTC. Không case nào cần đăng nhập thành công hay dùng tài khoản thật.
