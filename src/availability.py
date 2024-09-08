import datetime
import time
import logging
from crawler import crawler, SAT_INDEX, MON_INDEX, TUE_INDEX, WED_INDEX, THU_INDEX, FRI_INDEX, SAT_INDEX
from search_strategy import SunSearch, ForwardSearch, BackwardSearch, SearchContext


def check_availability(page_url, court_name):
  logging.info(f"===================== Checking availability for {court_name}... =====================")

  crawler.driver.get(page_url)
  time.sleep(1)

  WEEK_NAME_1 = "this week"
  WEEK_NAME_2 = "next week"

  crawler.curr_court = court_name
  crawler.select_duration()

  found = check_week_availability(WEEK_NAME_1)

  if not found:
    logging.info(f"No 1h weekend slots found for {court_name} this week. Checking next week...")
    crawler.go_to_next_week()
    found = check_week_availability(WEEK_NAME_2)

  if found:
    logging.info(f"Availability for {court_name}:")
    for one_hour_slot in crawler.data[court_name]:
      logging.info(one_hour_slot['message'])
  else:
    logging.info(f"No 1h weekend slots found for {court_name} this week or next week")


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
    search_context = SearchContext(ForwardSearch())
  else:
    search_context = SearchContext(SunSearch())

  if search_context.search(week_name):
    return True
  
  return False
  

