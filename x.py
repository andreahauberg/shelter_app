from flask import request
import mysql.connector
import re

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from icecream import ic
ic.configureOutput(prefix=f'***** | ', includeContext=True)


##############################
def db():
    db = mysql.connector.connect(
        host = "mysql",      # Replace with your MySQL server's address or docker service name "mysql"
        user = "root",  # Replace with your MySQL username
        password = "password",  # Replace with your MySQL password
        database = "company"   # Replace with your MySQL database name
    )
    cursor = db.cursor(dictionary=True)
    return db, cursor


##############################
USER_USERNAME_MIN = 2
USER_USERNAME_MAX = 20
USER_USERNAME_REGEX = f"^.{{{USER_USERNAME_MIN},{USER_USERNAME_MAX}}}$"
def validate_user_username():
    error = f"username {USER_USERNAME_MIN} to {USER_USERNAME_MAX} characters"
    user_username = request.form.get("user_username", "").strip()
    if not re.match(USER_USERNAME_REGEX, user_username): raise Exception(error)
    return user_username


##############################
USER_NAME_MIN = 2
USER_NAME_MAX = 20
USER_NAME_REGEX = f"^.{{{USER_NAME_MIN},{USER_NAME_MAX}}}$"
def validate_user_name():
    error = f"name {USER_NAME_MIN} to {USER_NAME_MAX} characters"
    user_name = request.form.get("user_name", "").strip()
    if not re.match(USER_NAME_REGEX, user_name): raise Exception(error)
    return user_name


##############################
USER_LAST_NAME_MIN = 2
USER_LAST_NAME_MAX = 20
USER_LAST_NAME_REGEX = f"^.{{{USER_LAST_NAME_MIN},{USER_LAST_NAME_MAX}}}$"
def validate_user_last_name():
    error = f"last name {USER_LAST_NAME_MIN} to {USER_LAST_NAME_MAX} characters"
    user_last_name = request.form.get("user_last_name", "").strip()
    if not re.match(USER_LAST_NAME_REGEX, user_last_name): raise Exception(error)
    return user_last_name

##############################
USER_EMAIL_REGEX = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
def validate_user_email():
    error = f"Invalid email"
    user_email = request.form.get("user_email", "").strip()
    if not re.match(USER_EMAIL_REGEX, user_email): raise Exception(error)
    return user_email

##############################
USER_PASSWORD_MIN = 6
USER_PASSWORD_MAX = 20
USER_PASSWORD_REGEX = f"^.{{{USER_PASSWORD_MIN},{USER_PASSWORD_MAX}}}$"
def validate_user_password():
    error = f"password {USER_PASSWORD_MIN} to {USER_PASSWORD_MAX} characters"
    user_password = request.form.get("user_password", "").strip()
    if len(user_password) < USER_PASSWORD_MIN: raise Exception(error)
    if len(user_password) > USER_PASSWORD_MAX: raise Exception(error)
    return user_password

##############################
PAGE_NUMBER_REGEX = "^[1-9][0-9]*$"
def validate_page_number(page_number):
    error = "page number not valid"
    if not re.match(PAGE_NUMBER_REGEX, page_number): raise Exception(error)
    return int(page_number)

##############################
ITEM_NAME_MIN = 2
ITEM_NAME_MAX = 50
ITEM_NAME_REGEX = f"^.{{{ITEM_NAME_MIN},{ITEM_NAME_MAX}}}$"
def validate_item_name():
    error = f"Shelter name must be {ITEM_NAME_MIN} to {ITEM_NAME_MAX} characters"
    item_name = request.form.get("item_name", "").strip()
    if not re.match(ITEM_NAME_REGEX, item_name): raise Exception(error)
    return item_name

##############################
ITEM_ADDRESS_MIN = 5
ITEM_ADDRESS_MAX = 100
ITEM_ADDRESS_REGEX = f"^.{{{ITEM_ADDRESS_MIN},{ITEM_ADDRESS_MAX}}}$"
def validate_item_address():
    error = f"Address must be {ITEM_ADDRESS_MIN} to {ITEM_ADDRESS_MAX} characters"
    item_address = request.form.get("item_address", "").strip()
    if not re.match(ITEM_ADDRESS_REGEX, item_address): raise Exception(error)
    return item_address

##############################
LAT_LON_REGEX = "^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$"
def validate_item_lat():
    error = "Invalid latitude format"
    item_lat = request.form.get("item_lat", "").strip()
    if not re.match(LAT_LON_REGEX, item_lat): raise Exception(error)
    return float(item_lat)

def validate_item_lon():
    error = "Invalid longitude format"
    item_lon = request.form.get("item_lon", "").strip()
    if not re.match(LAT_LON_REGEX, item_lon): raise Exception(error)
    return float(item_lon)

##############################
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp")
def validate_item_image():
    error = "Invalid image format"
    item_image = request.files.get("item_image")
    if not item_image or item_image.filename == "":  # Sikrer, at filen faktisk eksisterer
        raise Exception("No image uploaded")
    if not item_image.filename.lower().endswith(IMAGE_EXTENSIONS):
        raise Exception(error)
    return item_image





# def send_email(user_name, user_email, verification_key):
#     try:
#         sender_email = "andrea.hauberg1@gmail.com"
#         password = "ekkf vzjf untw jref"  
#         receiver_email = user_email  
#         message = MIMEMultipart()
#         message["From"] = "My company name"
#         message["To"] = user_email
#         message["Subject"] = "Welcome"

#         body = f"""Hello {user_name} To verify your account, please <a href="http://127.0.0.1/verify/{verification_key}">click here</a>"""
#         message.attach(MIMEText(body, "html"))

#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()
#             server.login(sender_email, password)
#             server.sendmail(sender_email, receiver_email, message.as_string())

#         ic("Email sent successfully!")

#         return "email sent"
#     except Exception as ex:
#         ic(ex)
#         raise Exception("Cannot send email")




##############################
def send_email(user_name, user_last_name, verification_key):
    try:
        # Create a gmail
        # Enable (turn on) 2 step verification/factor in the google account manager
        # Visit: https://myaccount.google.com/apppasswords

        # Email and password of the sender's Gmail account
        sender_email = "andrea.hauberg1@gmail.com"
        password = "ekkf vzjf untw jref"  # If 2FA is on, use an App Password instead

        # Receiver email address
        receiver_email = "andrea.hauberg1@gmail.com"
        
        # Create the email message
        message = MIMEMultipart()
        message["From"] = "My company name"
        message["To"] = "andrea.hauberg1@gmail.com"
        message["Subject"] = "Welcome"

        # Body of the email
        body = f"Thank you {user_name} {user_last_name} for signing up. Welcome."
        body = f"""To verify your account, please <a href="http://127.0.0.1/verify/{verification_key}">click here</a>"""
        message.attach(MIMEText(body, "html"))

        # Connect to Gmail's SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        ic("Email sent successfully!")

        return "email sent"
       
    except Exception as ex:
        ic(ex)
        raise Exception("cannot send email")
    finally:
        pass