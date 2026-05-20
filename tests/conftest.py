import time

import pytest

from framework.core.browser import Browser
from framework.core.logger import get_logger

logger = get_logger("tests")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    setattr(item, f"rep_{call.when}", outcome.get_result())


@pytest.fixture(autouse=True)
def test_logging(request):
    start_time = time.monotonic()
    logger.info("Test started: %s", request.node.nodeid)

    yield

    duration = time.monotonic() - start_time
    report = getattr(request.node, "rep_call", None)
    status = report.outcome if report is not None else "unknown"
    logger.info("Test finished: %s, status=%s, duration=%.2fs", request.node.nodeid, status, duration)


@pytest.fixture
def step(request):
    counter = {"value": 0}

    def _step(text: str) -> None:
        counter["value"] += 1
        logger.info("Step %s: %s | test=%s", counter["value"], text, request.node.nodeid)

    return _step


@pytest.fixture
def browser():
    browser_instance = Browser()
    driver = browser_instance.get_driver()
    yield driver
    browser_instance.quit()