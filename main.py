from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import logging
import os
from dotenv import load_dotenv

from login import login
from availability import check_availability
from emails import send_email
from config import RUN_PROGRAM

load_dotenv()

# Configure logging
logging.basicConfig(
  level=logging.INFO,  # Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
  format='%(asctime)s - %(levelname)s - %(message)s',  # Set the log message format
  handlers=[
    logging.FileHandler("logs.log"),  # Log to a file
    logging.StreamHandler()  # Optionally, also print logs to the console
  ]
)

CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")

FACILITY_ID = {
  'East A': '5dd9d9de-c567-472f-8f92-c0b0040fce0b',
  'East B': '4f41d717-8114-4c10-a1ab-2fcbab4c0b73',
  'East C': 'fbed3549-8020-44ae-ba4b-99263eabcca5',
  'East D': '2697bcf7-ff43-4770-a02e-77f3dafe230e',
  'West E': '6b7062e5-30e7-437b-a0d8-5f7fa8957889',
  'West F': '2d88ff48-0c7a-45e9-ad68-7b2f5d99aa0f',
  'West G': '4a1cefdc-7fc6-434b-b1cc-aef762116251',
  'West H': '30d9b4e5-7053-4c66-ae12-2ba86a46bad8'
}


def get_court_url(court_name):
  return f'https://unimelb.perfectmind.com/32617/Clients/BookMe4LandingPages/Facility?facilityId={FACILITY_ID[court_name]}&widgetId=15f6af07-39c5-473e-b053-96653f77a406&calendarId=bce15730-1f38-4e5c-889c-856322a7f877'


def main():
  options = Options()
  options.add_argument("--headless")  

  # Setup the WebDriver
  driver = webdriver.Chrome(options=options)
  driver.maximize_window()

  logging.info("Start crawling...")
  start_time = time.time()

  login(driver)

  data = []
  has_error = False
  try:
    for court_name in FACILITY_ID:
      availability_data = check_availability(driver, get_court_url(court_name), court_name)
      data += availability_data
  except Exception as e:
    logging.error(f"An error occurred: {e}")
    has_error = True

  logging.info("===============================================================================")

  if len(data) > 0:
    logging.info("Available 1h weekend slots found!")
    subject = "Available Weekend Badminton Slots Found!"
    body = ""
    for slot in data:
      body += f"{slot['message']}\n"
    send_email(subject, body)
  else:
    logging.info("Unfortunately, no available 1h weekend slots found.")
  
  driver.quit()

  if has_error:
    logging.info("Job Failed!")
  else:
    logging.info("Job Completed!")

  end_time = time.time()
  elapsed_time = end_time - start_time
  logging.info(f"Time spent: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
  # Clear the logs file
  open("logs.log", "w").close()

  if RUN_PROGRAM:
    main()
  else:
    logging.warn("Program is disabled.")