# pip install pytest
# pip install playwright
# pip install pytest-playwright
# playwright install

# playwright codegen djangoalfaromeowebapp.onrender.com  // Does snip your movements and automatically wrights the tests
# python -m pytest tests/UI_tests --headed  // To run all the tests + (--headed) opens the browser

import re
import time

from playwright.sync_api import Page, expect

website_URL = "http://localhost:8000/"


# website_URL = "https://djangoalfaromeowebapp.onrender.com/"

def wait_for_url(page: Page, expected_url: str, timeout_ms: int = 15000) -> None:
    start_time = time.time()
    while time.time() - start_time < timeout_ms / 1000:
        try:
            page.wait_for_url(expected_url, timeout=2000)
            return
        except TimeoutError:
            time.sleep(0.5)
    raise TimeoutError(f"Timed out waiting for URL: {expected_url}")


def register_user(page: Page, website_URL: str, email: str, password: str) -> None:
    page.goto(website_URL + 'accounts/register/')

    email_input = page.locator('input[name="email"]')
    email_input.fill(email)
    password_one = page.locator('input[name="password1"]')
    password_one.fill(password)
    password_two = page.locator('input[name="password2"]')
    password_two.fill(password)

    register_btn = page.locator('button[type="submit"]:text("Register")')
    register_btn.click()


def delete_user(page: Page) -> None:
    user_icon = page.locator('.fa-solid.fa-user')
    user_icon.hover()

    view_profile = page.locator('a', has_text="View Profile")
    view_profile.click()

    delete_profile = page.locator('a', has_text="Delete Profile")
    delete_profile.click()

    yes_btn = page.locator('button', has_text="Yes")
    yes_btn.click()


def test_home_page(page: Page) -> None:
    page.goto(website_URL)
    logo_link = page.locator('a.logo-a')
    logo_link.click()

    expect(page).to_have_title(re.compile("Alfa Romeo"))
    expect(page).to_have_url(website_URL)


# test_register_user will fail if it has been registered already !
def test_register_user(page: Page) -> None:
    page.goto(website_URL)

    # sign_in_btn = page.locator('a[href="/accounts/login/"]').first
    sign_in_btn = page.get_by_role("link", name="Sign In", exact=True)
    sign_in_btn.click()
    expect(page).to_have_url(website_URL + 'accounts/login/')

    register_link = page.locator('a[href="/accounts/register/"]')
    register_link.click()
    expect(page).to_have_url(website_URL + 'accounts/register/')

    # email = page.locator('input[name="email"]')
    # email.fill("test@gmail.com")
    # password_one = page.locator('input[name="password1"]')
    # password_one.fill("test@<PASSWORD>")
    # password_two = page.locator('input[name="password2"]')
    # password_two.fill("test@<PASSWORD>")
    email = 'test@gmail.com'
    password = 'test@<PASSWORD>'

    register_user(page, website_URL, email, password)

    # register_btn = page.locator('button[type="submit"]:text("Register")')
    # register_btn.click()
    wait_for_url(page, website_URL)

    expect(page).to_have_url(website_URL)

    delete_user(page)


def test_museum_page(page: Page) -> None:
    page.goto(website_URL)
    museum_link = page.locator('a[href="/museum/categories/"]:has-text("Museum")')
    museum_link.click()

    expect(page).to_have_url(website_URL + 'museum/categories/')


def test_history_page(page: Page) -> None:
    page.goto(website_URL)
    museum_link = page.locator('a[href="/history/categories/"]:has-text("History")')
    museum_link.click()

    expect(page).to_have_url(website_URL + 'history/categories/')


def test_events_page(page: Page) -> None:
    page.goto(website_URL)
    museum_link = page.locator('a[href="/events/"]:has-text("Events")')
    museum_link.click()

    expect(page).to_have_url(website_URL + 'events/')


def test_news_page(page: Page) -> None:
    page.goto(website_URL)
    museum_link = page.locator('a[href="/news/"]:has-text("News")')
    museum_link.click()

    expect(page).to_have_url(website_URL + 'news/')


def test_tickets_page(page: Page) -> None:
    page.goto(website_URL)
    museum_link = page.locator('a[href="/products/tickets/"]:has-text("Tickets")').first
    museum_link.click()

    expect(page).to_have_url(website_URL + 'products/tickets/')


def test_products_page(page: Page) -> None:
    page.goto(website_URL)
    museum_link = page.locator('a[href="/products/"]:has-text("Store")')
    museum_link.click()

    expect(page).to_have_url(website_URL + 'products/')
