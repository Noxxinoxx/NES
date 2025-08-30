#this module is called NNSAS
#it stands for Nox Notifications System Alert System
#This module makes the connection to all the send systems
#1. Mails send
#2. Phone Notification
#3. Windows Notification


#from Connections.phone_notification import phone_notification
from Connections.send_mail import send_mail

class NNSAS:
    def __init__(self):
        #self.phone_notification = phone_notification
        self.send_mail = send_mail

    def handle_alert(alert_data):
        #This function handles the alerts that comes in from the different sources.
        #Alerts need two things.
        #1. Alert Title
        #2. Alert Description

        title = alert_data.title
        description = alert_data.description

        send_mail.send_email_with_info(title, description)



