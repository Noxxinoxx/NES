##
## This code will handle all the notifications
## That are comming in and catagorse them
## 3 diffrent catagoise 
## 1 : important will send a stress notification
## 2 : info will also send notification
## 3 : will be stored but no notification will be sent
## 

class Categorizer: 
    def __init__(self, config):
        self.config_path = config

    def categorize(self, notification_data):
        print(notification_data)    
    


    