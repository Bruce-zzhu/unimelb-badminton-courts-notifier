from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import datetime

MON_INDEX = 0
TUE_INDEX = 1
WED_INDEX = 2
THU_INDEX = 3
FRI_INDEX = 4
SAT_INDEX = 5
SUN_INDEX = 6

class Crawler:
  def __init__(self):
    self.slots_explored = 0
    self.total_slots = 0
    self.driver = None
    self.buttons = []
    self.curr_court = ""
    self.data = {}
    self.has_error = False

  def init_driver(self):
    options = Options()
    # options.add_argument("--headless")  
    # Disable driver logs
    options.add_argument("--log-level=3")  # INFO = 0, WARNING = 1, LOG_ERROR = 2, LOG_FATAL = 3

    # Setup the WebDriver
    self.driver = webdriver.Chrome(options=options)
    self.driver.maximize_window()

  def update_total_slots(self, num):
    self.total_slots += num

  def update_data(self, day, time, message):
    if self.curr_court not in self.data:
      self.data[self.curr_court] = []

    self.data[self.curr_court].append({
      "day": day,
      "time": time,
      "message": message
    })

  def refresh_buttons(self):
    # Re-select the scheduler content and all "Book Now" buttons to avoid stale element reference
    scheduler_content = self.driver.find_element(By.CLASS_NAME, "k-scheduler-content")
    buttons = scheduler_content.find_elements(By.XPATH, "//div[contains(@class, 'k-event-template') and not(contains(@class, 'disabled-event'))]")
    self.buttons = buttons
    return len(buttons)
  
  def go_to_next_week(self):
    next_week_button = self.driver.find_element(By.XPATH, "//div[@class='sheduler-nav-btn next']")
    next_week_button.click()
    self.buttons = []
    self.curr_button_index = -1
    time.sleep(2)
  
  def select_duration(self):
    # Open the dropdown
    details = self.driver.find_element(By.XPATH, "//div[@class='facility-service-details']")
    # get the 3rd child
    items = details.find_elements(By.XPATH, "./*")[2]
    # get the 1st child
    item = items.find_elements(By.XPATH, "./*")[0]
    # get the 1st child
    select = item.find_elements(By.XPATH, "./*")[0]
    select.click()
    time.sleep(1)

    # Select the 1h duration
    dropdown = self.driver.find_element(By.XPATH, "//ul[@class='k-list k-reset']")
    dropdown_items = dropdown.find_elements(By.XPATH, "//li[@role='option']")
    for item in dropdown_items:
      if item.text == "1 h":
        item.click()
        break

    time.sleep(1)

  def get_slot_data(self, index):
    button = self.buttons[index]
    self.slots_explored += 1

    button.click()
    time.sleep(2)

    self.refresh_buttons()
  
    # Extract the date and time from the reservation details
    date_element = self.driver.find_element(By.XPATH, "//div[@class='bm-facility-landing-page-summary']//div[3]")
    reservation_date = date_element.text.strip()

    # No valid info shown
    if not reservation_date:
      return None

    time_element = self.driver.find_element(By.XPATH, "//div[@class='bm-facility-landing-page-summary']//div[4]")
    reservation_time = time_element.text.strip()

    day, month, year = map(int, reservation_date.split('/'))
    reservation_day = datetime.datetime(year, month, day)

    day_index = reservation_day.weekday()
    is_weekend = day_index in [SAT_INDEX, SUN_INDEX]

    data = {
      "date": reservation_date,
      "time": reservation_time,
      "is_weekend": is_weekend,
      "day_index": day_index
    }

    return data


crawler = Crawler()
