from selenium.webdriver.common.by import By
import time
import datetime
import logging

def check_availability(driver, page_url, court_name):
  logging.info(f"===================== Checking availability for {court_name}... =====================")
  
  driver.get(page_url)
  time.sleep(1)

  WEEK_NAME_1 = "this week"
  WEEK_NAME_2 = "next week"

  data = []

  (found, cur_week_data) = check_week_availability(driver, WEEK_NAME_1)

  if found:
    data = cur_week_data
  else:
    logging.info(f"No 1h weekend slots found for {court_name} this week. Checking next week...")

    go_to_next_week(driver)
    (next_found, next_week_data) = check_week_availability(driver, WEEK_NAME_2)
    found = next_found
    data = next_week_data

  if found:
    logging.info(f"Availability for {court_name}:")
    logging.info(data[0]['message'])
    logging.info(data[1]['message'])
  else:
    logging.info(f"No 1h weekend slots found for {court_name} this week or next week")

  return data

  
def go_to_next_week(driver):
  next_week_button = driver.find_element(By.XPATH, "//div[@class='sheduler-nav-btn next']")
  next_week_button.click()
  time.sleep(1)


def check_week_availability(driver, week_name):
  # Initial setup: Find the parent container with all the "Book Now" buttons
  scheduler_content = driver.find_element(By.CLASS_NAME, "k-scheduler-content")
  book_now_buttons = scheduler_content.find_elements(By.CLASS_NAME, "k-event")

  found = 0
  data = []
  def _update_data(day, time, message):
    data.append({
      "day": day,
      "time": time,
      "message": message
    })
  def _reset_data():
    data = []

  for index in range(len(book_now_buttons)):
  # Re-select the scheduler content and all "Book Now" buttons to avoid stale element reference
    scheduler_content = driver.find_element(By.CLASS_NAME, "k-scheduler-content")
    book_now_buttons = scheduler_content.find_elements(By.CLASS_NAME, "k-event")
    
    # Click the button at the current index
    button = book_now_buttons[index]
    button.click()
    time.sleep(2)  # Wait for the details to load

    # Extract the date and time from the reservation details
    date_element = driver.find_element(By.XPATH, "//div[@class='bm-facility-landing-page-summary']//div[3]")
    time_element = driver.find_element(By.XPATH, "//div[@class='bm-facility-landing-page-summary']//div[4]")
    
    reservation_date = date_element.text.strip()
    reservation_time = time_element.text.strip()
    
    # Check if the date is a weekend (Saturday or Sunday)
    day, month, year = map(int, reservation_date.split('/'))
    reservation_day = datetime.datetime(year, month, day)

    if reservation_day.weekday() in [5, 6]:
      message = f"Available slot on the weekend {week_name}: {reservation_date} at {reservation_time}"
      # logging.info(message)
      if found == 0:
        # 0.5h slot found!
        found = 1
        _update_data(reservation_date, reservation_time, message)
        continue
      elif found == 1:
        # 1h slot found!
        found = 2
        _update_data(reservation_date, reservation_time, message)
        break
      else:
        # non-consecutive slot, reset found
        found = 0
        _reset_data()
        continue
    # else:
    #   logging.info(f"Not a weekend slot: {reservation_date} at {reservation_time}")

  return (found == 2, data)