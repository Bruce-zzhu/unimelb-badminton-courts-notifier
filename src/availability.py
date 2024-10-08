import datetime
import time
import logging
from crawler import crawler, SAT_INDEX, MON_INDEX, TUE_INDEX, WED_INDEX, THU_INDEX, FRI_INDEX, SAT_INDEX
from search_strategy import SundaySearch, ForwardSearch, BackwardSearch, SearchContext


def check_availability(page_url, court_name):
  logging.info(f"===================== Checking availability for {court_name}... =====================")

  crawler.driver.get(page_url)
  time.sleep(1)

  WEEK_NAME_1 = "this week"
  WEEK_NAME_2 = "next week"

  crawler.curr_court = court_name
  crawler.select_duration()

  try:
    found_this = check_week_availability(WEEK_NAME_1)
  except Exception as e:
    logging.error(f"An error occurred: {e}")
    crawler.has_error = True
    found_this = False

  if found_this:
    logging.info(f"Availability for {court_name}:")
    for one_hour_slot in crawler.data[court_name]:
      logging.info(one_hour_slot['message'])
    logging.info(f"Checking next week...")
  else:
    logging.info(f"No 1h weekend slots found for {court_name} this week. Checking next week...")
    
  try:
    crawler.go_to_next_week()
    found_next = check_week_availability(WEEK_NAME_2)
  except Exception as e:
    logging.error(f"An error occurred: {e}")
    crawler.has_error = True
    found_next = False

  if found_next:
    if not found_this:
      logging.info(f"Availability for {court_name}:")
    for one_hour_slot in crawler.data[court_name]:
      logging.info(one_hour_slot['message'])
  else:
    logging.info(f"No 1h weekend slots found for {court_name} next week")


def check_week_availability(week_name):
  buttons_count = crawler.refresh_buttons()
  crawler.update_total_slots(buttons_count)

  if buttons_count == 0:
    # No slots for this week
    return False
  
  today = datetime.datetime.now().weekday()

  if today in [MON_INDEX, TUE_INDEX, WED_INDEX]:
    search_context = SearchContext(BackwardSearch())
  elif today in [THU_INDEX, FRI_INDEX, SAT_INDEX]:
    search_context = SearchContext(ForwardSearch(today))
  else:
    search_context = SearchContext(SundaySearch())

  if search_context.search(week_name):
    return True
  
  return False
  

