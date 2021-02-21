import sys
import os
sys.path.append('/home/pi/droneponics/droneAtlas/drone')
import datetime
import time
from google.api_core.exceptions import NotFound
from google.cloud import logging


TEST_LOGGER_NAME = "example_log_{}".format(uuid.uuid4().hex)


def example_log():
    client = logging.Client()
    logger = client.logger(TEST_LOGGER_NAME)
    text = "Hello, world."
    logger.log_text(text)
    return text
    
    
class DroneAlert:
  def __init__(self, __text, __payload):
    try:
      from google.cloud import error_reporting

      client = error_reporting.Client()
      client.report("An error has occurred.")
  
  __payload = {}
        drone.getBootPayload(__payload):
        __payload["displayText"] = __text 
    
    except:   
        print("Except DroneAlert")
        
        
class DroneError():

  def __init__(self, __text, __payload):
    from google.cloud import error_reporting 
    report_errors_api(self):
    client = error_reporting.Client()
    client.report("An error has occurred.")
  
  def manualError(self, __text):
    from google.cloud import error_reporting
    client = error_reporting.Client()
    
    try:
      client.report(__text)
    except:
      client.report_exception()

  def exceptionError(self):
    from google.cloud import error_reporting
    client = error_reporting.Client()
    
    try:
      client.report_exception()
    except:
      pass

  def apiError(self, __info):
    from google.cloud import error_reporting
    client = error_reporting.Client()
    
    try:
      _report_errors_api
      _use_grpc
      project
      _credentials
      _http
      _client_info
      _client_options
        
      client.report_errors_api()
    except:
      client.report_exception()
      
      
        
        
  def simulate_error():
    from google.cloud import error_reporting
    client = error_reporting.Client()
    try:
        # simulate calling a method that's not defined
        raise NameError
    except Exception:
        client.report_exception()
        
        
/*

    def report_errors_api(self):
        """Helper for logging-related API calls.
        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/entries
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.logs
        :rtype:
            :class:`_gapic._ErrorReportingGapicApi`
            or
            :class:`._logging._ErrorReportingLoggingAPI`
        :returns: A class that implements the report errors API.
        """
        if self._report_errors_api is None:
            if self._use_grpc:
                self._report_errors_api = make_report_error_api(self)
            else:
                self._report_errors_api = _ErrorReportingLoggingAPI(
                    self.project,
                    self._credentials,
                    self._http,
                    self._client_info,
                    self._client_options,
                )
        return self._report_errors_api
        
*/
