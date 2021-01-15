# importing os module  
import os 
  
# Add a new environment variable  
os.environ['GCLOUD_PROJECT'] = 'droneponics-301222'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/pi/droneponics/config/Google/service_account.json'

# Get the value of 
# Added environment variable  
print("GCLOUD_PROJECT:", os.environ['GCLOUD_PROJECT'])
print('\n')
print("GOOGLE_APPLICATION_CREDENTIALS:", os.environ['GOOGLE_APPLICATION_CREDENTIALS']) 
