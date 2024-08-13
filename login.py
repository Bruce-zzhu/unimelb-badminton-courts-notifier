from selenium.webdriver.common.by import By
import time
import logging
import os

LOGIN_RUL='https://unimelb.perfectmind.com/SocialSite/MemberRegistration/MemberSignIn'
EMAIL = os.getenv("UNIMELB_EMAIL")
PASSWORD = os.getenv("UNIMELB_PASSWORD")

def login(driver):
  # Navigate to the login page
  driver.get(LOGIN_RUL)

  # Find the email and password fields and enter your credentials
  email_field = driver.find_element(By.NAME, "username")  # Adjust this according to the HTML element name
  password_field = driver.find_element(By.NAME, "password")  # Adjust this according to the HTML element name

  email_field.send_keys(EMAIL)
  password_field.send_keys(PASSWORD)

  # Find the login button and click it
  login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')  # Adjust this according to the HTML element type and attributes
  login_button.click()

  # Wait for the login to complete and redirect
  time.sleep(1)  # Adjust the sleep time according to your page load speed

  logging.info("I have logged in, Yay!")

