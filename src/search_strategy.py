from abc import ABC, abstractmethod
from crawler import crawler, SAT_INDEX, SUN_INDEX

def get_message(slot_data, week_name):
  return f"Available 1h slot on the weekend {week_name}: {slot_data['date']} at {slot_data['time']}"

class SearchStrategy(ABC):
  @abstractmethod
  def search(self, week_name):
    pass

class SundaySearch(SearchStrategy):
  '''
    Strategy when today is Sun, search 1st and the last button as they are at the start and the end of the calendar week
  '''
  def search(self, week_name):
    first_slot_data = crawler.get_slot_data(0)
    if first_slot_data['is_weekend']:
      message = get_message(first_slot_data, week_name)
      crawler.update_data(first_slot_data['date'], first_slot_data['time'], message)
      return True
    
    last_index = len(crawler.buttons) - 1
    if last_index < len(crawler.buttons) and last_index > 0: 
      last_slot_data = crawler.get_slot_data(last_index)
      if last_slot_data['is_weekend']:
        message = get_message(last_slot_data, week_name)
        crawler.update_data(last_slot_data['date'], last_slot_data['time'], message)
        return True
    
    return False
  

class ForwardSearch(SearchStrategy):
  '''
  Strategy when today is Thu or Fri or Sat (start day index is 3 or 4 or 5)
  '''
  def __init__(self, today):
    super().__init__()
    self.today_index = today

  def search(self, week_name):
    for button_index in range(len(crawler.buttons)):
      # In case buttons overlap in consecutive slots, we check if the index is still valid
      if button_index >= len(crawler.buttons):
        break

      slot_data = crawler.get_slot_data(button_index)
      if slot_data:
        if slot_data['is_weekend']:
          message = get_message(slot_data, week_name)
          crawler.update_data(slot_data['date'], slot_data['time'], message)
          return True
        elif slot_data['day_index'] < self.today_index:
          # Break if the search passes Sunday
          break
    return False

  
class BackwardSearch(SearchStrategy):
  '''
  Strategy when today is Mon or Tue or Wed (start day index is 0, 1, or 2)
  '''
  def search(self, week_name):
    for button_index in range(len(crawler.buttons), 0, -1):
      # In case buttons overlap in consecutive slots, we check if the index is still valid
      if button_index >= len(crawler.buttons):
        break

      slot_data = crawler.get_slot_data(button_index)
      if slot_data:
        if slot_data['is_weekend']:
          message = get_message(slot_data, week_name)
          crawler.update_data(slot_data['date'], slot_data['time'], message)
          return True
        elif slot_data['day_index'] < SAT_INDEX:
          # Break if pass Saturday
          break
    return False


class SearchContext:
  def __init__(self, strategy: SearchStrategy):
    self.strategy = strategy

  def search(self, week_name):
    return self.strategy.search(week_name)