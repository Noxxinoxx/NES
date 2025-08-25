#####################################
#                                   #
#   Handels the notifiation send    # 
#                                   #           
#####################################
## I can use this chatgpt info to connct it to my mail server
## https://chatgpt.com/share/68acd4ed-1ecc-8005-a3c2-94b77b74e806
class sender:
    def __init__(self, email):
        self.email = email
        self.info = ""

    def send_email_with_info(self):
        print("Sending email")
        print("Email info: ", self.info)


    def set_email_info(self, information):
        self.info = information

