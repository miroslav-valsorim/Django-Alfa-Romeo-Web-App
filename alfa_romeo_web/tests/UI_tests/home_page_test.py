# pip install pytest
# pip install playwright
# pip install pytest-playwright
# playwright install

# playwright codegen djangoalfaromeowebapp.onrender.com  // Does snip your movements and automatically wrights the tests

# python -m pytest tests/UI_tests --headed  // To run all the tests + (--headed) opens the browser


from playwright.sync_api import Page, expect


website_URL = "http://localhost:8000/"


def test_home_page(page: Page) -> None:
    page.goto(website_URL)
    page.locator('class=logo-a')
