"""Excel-driven UI checks for the UTC e-Office login module."""

from __future__ import annotations

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.login_page import LoginPage
from utils.excel_reader import load_test_cases


_CASES = {case["Test Case ID"]: case for case in load_test_cases()}


@pytest.mark.parametrize("case_id", list(_CASES), ids=list(_CASES))
def test_login_case(case_id: str, driver: WebDriver, request: pytest.FixtureRequest) -> None:
    case = _CASES[case_id]
    page = LoginPage(driver)

    allure.dynamic.title(f"{case_id} - {case['Test Case']}")
    allure.dynamic.description(
        f"**Tiền điều kiện:** {case['Preconditions']}\n\n"
        f"**Các bước:** {case['Steps']}\n\n"
        f"**Kết quả mong đợi:** {case['Expected Result']}"
    )
    allure.dynamic.feature("Đăng nhập Văn phòng điện tử UTC")
    allure.dynamic.story(case["Test Case"])
    allure.dynamic.severity(allure.severity_level.NORMAL)

    with allure.step("Mở trang đăng nhập"):
        page.open()
        assert "Đăng nhập" in driver.title

    with allure.step(case["Steps"]):
        action = case["Action"]
        if action == "page_load":
            assert page.login_form_is_visible()
            assert page.submit_button().get_attribute("value") == "Đăng nhập"
        elif action.startswith("submit_"):
            page.submit_login(case["Username"], case["Password"])
            assert "/Login" in driver.current_url
            assert page.login_form_is_visible()
        elif action == "password_masked":
            assert page.password_is_masked()
        elif action == "remember_me_toggle":
            assert page.remember_me_can_toggle()
        elif action == "forgot_password_link":
            page.open_password_recovery()
            assert page.recovery_form_is_visible()
        elif action == "google_login_link":
            assert page.google_login_link_is_valid()
        else:
            pytest.fail(f"Action chưa được hỗ trợ trong Excel: {action}")

    allure.attach(driver.current_url, "URL sau kiểm thử", allure.attachment_type.TEXT)
    allure.attach(driver.page_source, "HTML trang sau kiểm thử", allure.attachment_type.HTML)
    allure.attach(driver.get_screenshot_as_png(), "Ảnh trang sau kiểm thử", allure.attachment_type.PNG)

    pause_seconds = request.config.getoption("--pause")
    if pause_seconds > 0:
        import time

        time.sleep(pause_seconds)
