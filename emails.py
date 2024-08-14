import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import os

APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
EMAIL = os.getenv("GMAIL_EMAIL")

def send_email(data):
  subject = "Available Weekend Badminton Slots Found!"
  body = ""
  for court_data in data:
    court_name = court_data["court"]
    available_slots = court_data["data"]
    body += f'''
      Available slots for {court_name}:
        {available_slots[0]['message']} 
        {available_slots[1]['message']} 

    '''

  logging.info("Sending email notification...")
  
  # Create the email
  msg = MIMEMultipart()
  msg['From'] = EMAIL
  msg['To'] = EMAIL
  msg['Subject'] = subject

  # Attach the body with HTML content (optional)
  msg.attach(MIMEText(body, 'plain'))

  try:
    # Connect to Gmail's SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Use TLS encryption
    server.login(EMAIL, APP_PASSWORD)  # Login to the Gmail account

    # Send the email
    server.send_message(msg)
    logging.info("Email sent successfully! 📩")
  except Exception as e:
    logging.error(f"Failed to send email: {e}")
  finally:
    server.quit()  # Close the connection
