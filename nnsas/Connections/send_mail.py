#####################################
#                                   #
#   Handels the notifiation send    # 
#                                   #           
#####################################
## I can use this chatgpt info to connct it to my mail server
## https://chatgpt.com/share/68acd4ed-1ecc-8005-a3c2-94b77b74e806
class send_mail:
    def __init__(self, email):
        self.email = email
        self.info = ""

    def send_email_with_info(self, title, description):
        print("Sending email")
        print("Email title: " + title) 
        print("Email description: " + description)
        
