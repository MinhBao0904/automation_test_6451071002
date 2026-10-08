"""Excel-driven, visible-browser Selenium tests with Allure metadata."""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import allure
import pytest
from openpyxl import Workbook, load_workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


ROOT = Path(__file__).resolve().parent
CASE_FILE = ROOT / "test_cases" / "login_test_cases.xlsx"
BASE_URL = os.getenv("LOGIN_URL", "https://vanphongdientu.utc.edu.vn/Login")
HEADERS = [
    "Test Case ID", "Module", "Test Case", "Preconditions", "Username",
    "Password", "Steps", "Expected Result", "Action", "Status",
]


def ensure_workbook() -> None:
    CASE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not CASE_FILE.exists():
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Login"
        sheet.append(HEADERS)
        sheet.freeze_panes = "A2"
        sheet.auto_filter.ref = "A1:J1"
        workbook.save(CASE_FILE)


def get_cases() -> list[dict]:
    ensure_workbook()
    sheet = load_workbook(CASE_FILE, data_only=True).active
    return [dict(zip(HEADERS, row)) for row in sheet.iter_rows(min_row=2, values_only=True) if row[0]]


CASES = get_cases()


def make_driver(browser: str):
    if browser == "edge":
        options = webdriver.EdgeOptions()
    else:
        options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Edge(options=options) if browser == "edge" else webdriver.Chrome(options=options)


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["Test Case ID"])
def test_login_case(case: dict, request: pytest.FixtureRequest) -> None:
    """Run one Excel row, emitting an independently visible Allure result."""
    allure.dynamic.title(f"{case['Test Case ID']} - {case['Test Case']}")
    allure.dynamic.description(
        f"**Tiền điều kiện:** {case['Preconditions']}\n\n"
        f"**Các bước:** {case['Steps']}\n\n"
        f"**Kết quả mong đợi:** {case['Expected Result']}"
    )
    allure.dynamic.feature("Đăng nhập Văn phòng điện tử UTC")
    allure.dynamic.story(case["Test Case"])
    allure.dynamic.severity(allure.severity_level.NORMAL)

    browser = request.config.getoption("--browser")
    pause_seconds = request.config.getoption("--pause")
    driver = make_driver(browser)
    wait = WebDriverWait(driver, 20)
    try:
        with allure.step("Mở trang đăng nhập"):
            driver.get(BASE_URL)
            username = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
            password = wait.until(EC.visibility_of_element_located((By.NAME, "userpwd")))
            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.submit_login")))
            assert "Đăng nhập" in driver.title, f"Tiêu đề không đúng: {driver.title!r}"

        with allure.step(case["Steps"]):
            action = case["Action"]
            if action == "page_load":
                assert username.is_displayed() and password.is_displayed() and submit.is_displayed()
                assert submit.get_attribute("value") == "Đăng nhập"

            elif action.startswith("submit_"):
                if case["Username"] is not None:
                    username.send_keys(str(case["Username"]))
                if case["Password"] is not None:
                    password.send_keys(str(case["Password"]))
                submit.click()
                wait.until(EC.presence_of_element_located((By.NAME, "username")))
                assert "/Login" in driver.current_url, f"Không mong đợi chuyển trang: {driver.current_url}"

            elif action == "password_masked":
                assert password.get_attribute("type") == "password"

            elif action == "remember_me_toggle":
                checkbox = driver.find_element(By.ID, "persistent")
                label = driver.find_element(By.CSS_SELECTOR, "label[for='persistent']")
                assert not checkbox.is_selected()
                label.click()
                assert checkbox.is_selected(), "Checkbox không được chọn sau khi nhấn"
                label.click()
                assert not checkbox.is_selected(), "Checkbox không bỏ chọn sau lần nhấn thứ hai"

            elif action == "forgot_password_link":
                driver.find_element(By.CSS_SELECTOR, "a[href='/Login/GetPass']").click()
                wait.until(EC.url_contains("/Login/GetPass"))
                assert "Lấy lại mật khẩu" in driver.title
                assert driver.find_element(By.CSS_SELECTOR, "input[placeholder='Địa chỉ Email']").is_displayed()
                assert driver.find_element(By.CSS_SELECTOR, "input[placeholder='Mã bảo mật']").is_displayed()

            elif action == "google_login_link":
                oauth = driver.find_element(By.CSS_SELECTOR, "a[href^='https://accounts.google.com/o/oauth2/auth']")
                assert oauth.is_displayed()
                assert "Đăng nhập bằng e-mail UTC" in oauth.text

            else:
                raise ValueError(f"Action chưa được hỗ trợ: {action}")

        allure.attach(driver.current_url, "URL sau kiểm thử", allure.attachment_type.TEXT)
        allure.attach(driver.page_source, "HTML trang sau kiểm thử", allure.attachment_type.HTML)
        allure.attach(driver.get_screenshot_as_png(), "Ảnh trang sau kiểm thử", allure.attachment_type.PNG)
        print(f"PASS {case['Test Case ID']}: {case['Test Case']}")
        if pause_seconds > 0:
            print(f"Giữ cửa sổ {pause_seconds:g} giây để quan sát...")
            time.sleep(pause_seconds)
    except Exception:
        if driver:
            allure.attach(driver.get_screenshot_as_png(), "Ảnh khi test lỗi", allure.attachment_type.PNG)
            allure.attach(driver.page_source, "HTML khi test lỗi", allure.attachment_type.HTML)
        raise
    finally:
        driver.quit()


if __name__ == "__main__":
    raise SystemExit(pytest.main(sys.argv[1:]))
