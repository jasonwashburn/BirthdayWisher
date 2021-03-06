"""
A script that sends a randomly chosen, customized birthday message to contacts listed in birthdays.csv
"""
import smtplib
import datetime as dt
import config  # Import secret login information, stored separately to keep it out of git/github
import random
import pandas as pd


def send_email(to_address, subject, message):
    """
    Sends an email message with gmail using the account info provided in config.py

    :param to_address: email address of the recipient
    :param subject: subject of email
    :param message: message to send
    :return: None
    """

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=config.my_email, password=config.password)
        connection.sendmail(
            from_addr=config.my_email,
            to_addrs=to_address,
            msg=f"Subject: {subject}\n\n{message}"
        )


# Get the current date
now = dt.datetime.now()

birthdays_df = pd.read_csv("birthdays.csv")  # Read in birthdays from birthdays.csv file

# Create a new dataframe containing birthdays that match today's month and day
todays_birthdays_df = birthdays_df[(birthdays_df.month == now.month) & (birthdays_df.day == now.day)]

# Iterate through the dataframe of matching birthdays then customize and send a randomly chosen message for each
for index, row in todays_birthdays_df.iterrows():
    with open(f"letter_templates/letter_{random.choice([1, 2, 3])}.txt") as letter_file:
        custom_message = letter_file.read()

    custom_message = custom_message.replace("[NAME]", row['name'])
    custom_message = custom_message.replace("[FROM]", config.my_name)
    print(f"Sending message to {row['name']} - {row['email']}")
    send_email(to_address=row['email'], subject='Happy Birthday', message=custom_message)
