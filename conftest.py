"""Shared pytest options, WebDriver lifecycle, and Excel execution status."""

from __future__ import annotations

from collections.abc import Generator
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import PROJECT_ROOT


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--browser", choices=("chrome", "edge"), default="chrome", help="Browser to run visibly")
    parser.addoption("--pause", type=float, default=5.0, help="Seconds to keep the result visible")
    parser.addoption("--headless", action="store_true", help="Run without opening a visible browser")
    parser.addoption("--case", default=None, help="Run one Test Case ID from the Excel workbook")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    selected_case = config.getoption("--case")
    if not selected_case:
        return
    selected = []
    deselected = []
    for item in items:
        callspec = getattr(item, "callspec", None)
        case_id = callspec.params.get("case_id") if callspec else None
        (selected if case_id == selected_case else deselected).append(item)
    items[:] = selected
    config.hook.pytest_deselected(items=deselected)


@pytest.fixture
def driver(request: pytest.FixtureRequest) -> Generator[WebDriver, None, None]:
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    options = webdriver.ChromeOptions() if browser == "chrome" else webdriver.EdgeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    if headless:
        options.add_argument("--headless=new")

    web_driver = webdriver.Chrome(options=options) if browser == "chrome" else webdriver.Edge(options=options)
    web_driver.set_page_load_timeout(45)
    try:
        yield web_driver
    finally:
        report = getattr(request.node, "rep_call", None)
        if report is not None and report.failed:
            try:
                screenshot = web_driver.get_screenshot_as_png()
                case_id = getattr(request.node, "callspec", None)
                case_id = case_id.params.get("case_id", request.node.name) if case_id else request.node.name
                screenshot_dir = PROJECT_ROOT / "artifacts" / "screenshots"
                screenshot_dir.mkdir(parents=True, exist_ok=True)
                (screenshot_dir / f"{case_id}.png").write_bytes(screenshot)
                allure.attach(screenshot, "Ảnh khi test lỗi", allure.attachment_type.PNG)
                allure.attach(web_driver.page_source, "HTML khi test lỗi", allure.attachment_type.HTML)
            except Exception:
                pass
        web_driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return

    item.rep_call = report


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """Write all execution statuses once, without making Excel lock a test failure."""
    statuses = {}
    for item in session.items:
        callspec = getattr(item, "callspec", None)
        case_id = callspec.params.get("case_id") if callspec else None
        report = getattr(item, "rep_call", None)
        if case_id and report is not None:
            statuses[case_id] = "Passed" if report.passed else "Failed"
    if not statuses:
        return

    from utils.excel_reader import set_case_statuses

    try:
        set_case_statuses(statuses)
    except PermissionError:
        reporter = session.config.pluginmanager.get_plugin("terminalreporter")
        if reporter:
            reporter.write_line(
                "Cảnh báo: Excel đang mở/khóa; giữ nguyên cột Status. Kết quả trong Allure vẫn đầy đủ."
            )
