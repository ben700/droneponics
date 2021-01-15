# importing os module  
import os 
  
# Add a new environment variable  
os.environ['GOOGLE_CLOUD_PROJECT'] = 'droneponics-301222'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/pi/droneponics/config/Google/service_account.json'

# Get the value of 
# Added environment variable  
print("GOOGLE_CLOUD_PROJECT:", os.environ['GOOGLE_CLOUD_PROJECT'])
print("GOOGLE_APPLICATION_CREDENTIALS:", os.environ['GOOGLE_APPLICATION_CREDENTIALS']) 
