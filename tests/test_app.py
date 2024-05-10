from playwright.sync_api import Page, expect
from lib.booking_repository import *
# Tests for your routes go here

# """
# We can render the index page
# """
# def test_get_index(page, test_web_address):
#     # We load a virtual browser and navigate to the /index page
#     page.goto(f"http://{test_web_address}/index")

#     # We look at the <p> tag
#     p_tag = page.locator("p")

#     # We assert that it has the text "This is the homepage."
#     expect(p_tag).to_have_text("This is the homepage.")


"""
We can render a homepage
"""


def test_get_homepage(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    page.goto(f"http://{test_web_address}")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Feel at home, anywhere")
    h2_tag = page.locator("h2")
    expect(h2_tag).to_have_text("Sign up to MakersBnB")


def test_sign_up_inputs(page, test_web_address, db_connection):
    page.set_default_timeout(1000)
    page.goto(f"http://{test_web_address}")
    page.fill("input[name=email]", "123@gmail.com")
    page.fill("input[name=password]", "P12345678!")
    page.fill("input[name=password_confirmation]", "P12345678!")
    page.click("text='Sign up'")
    title_element = page.locator("h1")
    expect(title_element).to_have_text("Login to MakersBnB")

def test_sign_up_inputs_with_email_indatabase_error(page, test_web_address):
    page.set_default_timeout(1000)
    page.goto(f"http://{test_web_address}")
    page.fill("input[name=email]", "matthew@gmail.com")
    page.fill("input[name=password]", "P12345678!")
    page.fill("input[name=password_confirmation]", "P12345678!")
    page.click("text='Sign up'")
    errors_tag = page.locator(".t-email_error")
    expect(errors_tag).to_have_text("There were errors in your submission: Email already registered")

def test_sign_up_inputs_with_password_invalid_confirmation_error(page, test_web_address, db_connection):
    page.set_default_timeout(1000)
    page.goto(f"http://{test_web_address}")
    page.fill("input[name=email]", "ifdhdi@gmail.com")
    page.fill("input[name=password]", "P12345678!")
    page.fill("input[name=password_confirmation]", "P12345678!!")
    page.click("text='Sign up'")
    errors_tag = page.locator(".t-password_error")
    expect(errors_tag).to_have_text("There were errors in your submission: Passwords must be indentical")

def test_sign_up_inputs_with_invalid_entry_all_error(page, test_web_address, db_connection):
    page.set_default_timeout(1000)
    page.goto(f"http://{test_web_address}")
    page.fill("input[name=email]", "")
    page.fill("input[name=password]", "")
    page.fill("input[name=password_confirmation]", "")
    page.click("text='Sign up'")
    errors_tag = page.locator(".t-password_error")
    expect(errors_tag).to_have_text("There were errors in your submission: Password must not be blank")

def test_login_link(page, test_web_address):
    page.set_default_timeout(1000)
    page.goto(f"http://{test_web_address}")
    page.click("text='Login'")
    title_element = page.locator("h1")
    expect(title_element).to_have_text("Login to MakersBnB")


def test_about_link(page, test_web_address):
    page.set_default_timeout(1000)
    page.goto(f"http://{test_web_address}")
    page.click("text='About'")
    title_element = page.locator("h1")
    expect(title_element).to_have_text("About MakersBnB")


def test_login_inputs(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    page.set_default_timeout(1000)
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name=email]", "matthew@gmail.com")
    page.fill("input[name=password]", "Password123!")
    page.click("text='Log in'")
    title_element = page.locator("h1")
    expect(title_element).to_have_text("Book a Space")

def test_login_inputs_email_invalid(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    page.set_default_timeout(1000)
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name=email]", "")
    page.fill("input[name=password]", "Hello12345@")
    page.click("text='Log in'")
    errors_tag = page.locator(".t-email_error")
    expect(errors_tag).to_have_text("There were errors in your submission: Email not registered, please sign up")

def test_login_inputs_password_invalid(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    page.set_default_timeout(1000)
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name=email]", "matthew@gmail.com")
    page.fill("input[name=password]", "He2345@")
    page.click("text='Log in'")
    errors_tag = page.locator(".t-password_error")
    expect(errors_tag).to_have_text("There were errors in your submission: Incorrect password, please try again")


def test_list_a_space_link_from_spaces_page(page, test_web_address):
    page.set_default_timeout(1000)
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name=email]", "matthew@gmail.com")
    page.fill("input[name=password]", "Password123!")
    page.click("text='Log in'")
    title_element = page.locator("h1")
    expect(title_element).to_have_text("Book a Space")
    page.click("text='Create A Space'")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("List a Space")


def test_list_a_space_form(page, test_web_address):
    page.set_default_timeout(1000)
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name=email]", "matthew@gmail.com")
    page.fill("input[name=password]", "Password123!")
    page.click("text='Log in'")
    title_element = page.locator("h1")
    expect(title_element).to_have_text("Book a Space")
    page.click("text='Create A Space'")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("List a Space")
    page.fill("input[name=title]", "Beautiful Space")
    page.fill("input[name=price_per_night]", "100")
    page.fill("input[name=available_from]", "2024-01-06")
    page.fill("input[name=available_to]", "2025-06-01")
    page.click("text=List my Space")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Book a Space")


def test_book_a_space_has_spaces_link(page, test_web_address,db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    page.set_default_timeout(1000)
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name=email]", "matthew@gmail.com")
    page.fill("input[name=password]", "Password123!")
    page.click("text='Log in'")
    page.click("text='Spaces'")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Book a Space")


def test_book_a_space_has_requests_link(page, test_web_address, db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    page.set_default_timeout(1000)
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name=email]", "matthew@gmail.com")
    page.fill("input[name=password]", "Password123!")
    page.click("text='Log in'")
    page.click("text='Requests'")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Requests")
    h2_tag = page.locator("h2")
    expect(h2_tag).to_have_text(
        [" Requests I've made ", " Requests I've received "])


def test_book_a_space_has_signout_link(page, test_web_address):
    page.set_default_timeout(1000)
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name=email]", "matthew@gmail.com")
    page.fill("input[name=password]", "Password123!")
    page.click("text='Log in'")
    page.click("text='Sign out'")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Feel at home, anywhere")





def test_spaces_display_chosen_date(page, test_web_address):
    page.set_default_timeout(1000)
    page.goto(f"http://{test_web_address}/1/spaces")
    page.fill("input[name='Pick A Date']", "2024-07-09")
    page.screenshot(path='screenshot.png')
    page.click('input[type="submit"][value="List Available Spaces"]')
    h3_tag = page.locator("h3")
    expect(h3_tag).to_have_text("Available Spaces on 2024-07-09")


def test_spaces_display_booking_confirmation(page, test_web_address,db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    page.set_default_timeout(1000)
    bookingrepo = BookingRepository(db_connection)
    page.goto(f"http://{test_web_address}/1/spaces")
    page.fill("input[name='Pick A Date']", "2026-10-27")
    #page.screenshot(path='screenshot.png')
    page.click('input[type="submit"][value="List Available Spaces"]')
    h3_tag = page.locator("h3")
    expect(h3_tag).to_have_text("Available Spaces on 2026-10-27")
    page.click('input[type="submit"][value="Book"]')
    #page.screenshot(path='screenshot.png')
    page.click('input[type="submit"][value="Confirm Booking"]')
    new_booking = Booking(5,'2026-10-27',1,4)
    assert new_booking == bookingrepo.find_by_id(5)
    
    


def test_create_new_space_error(page, test_web_address):
    page.set_default_timeout(1000)
    page.goto(f"http://{test_web_address}/1/spaces")
    page.click("text='Create A Space'")
    page.fill("input[name=available_from]", "2024-05-10")
    page.fill("input[name=available_to]", "2025-05-10")
    page.click("text='List my Space'")
    error_tag = page.locator('.errors')
    expect(error_tag).to_have_text(
        "Your form contained some errors: Title can't be blank, Price can't be blank, Price has to be a number (up to 2 decimals)")

