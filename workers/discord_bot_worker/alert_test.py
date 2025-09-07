from common.kafka_sender import Sender

test_data = {
  "service": "mongodb",        
  "level": "error",            
  "category": 1,               
  "message": "MongoDB connection failed",  
  "timestamp": "2025-09-07T15:34:12Z"    
}

sender = Sender()

sender.send_alert(test_data)

