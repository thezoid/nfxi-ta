#core libraries
import json
import os
import datetime

#google libraries
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#class for helpers
class tcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[1;37;40m'

#funcs
def writeLog(message, type, writeTofile=True,loggingLevel=2):
     if loggingLevel == 0:
          return
     _scriptdir = os.path.dirname(os.path.realpath(__file__))
     if type.upper() == "ERROR" and loggingLevel >= 1:
          print(tcolors.FAIL,f"[ERROR][{datetime.datetime.today().strftime('%Y%B%d@%H:%M:%S')}] {message}",tcolors.ENDC)
          if writeTofile:
               _scriptdir = os.path.dirname(os.path.realpath(__file__))
               with open(os.path.join(_scriptdir,"logs",f"{datetime.datetime.today().strftime('%Y%B%d')}.log"),"a",encoding="utf-8") as logFile:
                    logFile.write(f"[ERROR]][{datetime.datetime.today().strftime('%Y%B%d@%H:%M:%S')}] {message}\n")
     elif type.upper() == "WARNING" and loggingLevel >= 2:
               print(tcolors.WARNING,f"[WARNING][{datetime.datetime.today().strftime('%Y%B%d@%H:%M:%S')}] {message}",tcolors.ENDC)
               if writeTofile:
                    _scriptdir = os.path.dirname(os.path.realpath(__file__))
                    with open(os.path.join(_scriptdir,"logs",f"{datetime.datetime.today().strftime('%Y%B%d')}.log"),"a",encoding="utf-8") as logFile:
                         logFile.write(f"[WARNING][{datetime.datetime.today().strftime('%Y%B%d@%H:%M:%S')}] {message}\n")
     elif type.upper() == "SUCCESS" and loggingLevel >= 2:
          print(tcolors.OKGREEN,f"[SUCCESS][{datetime.datetime.today().strftime('%Y%B%d@%H:%M:%S')}] {message}",tcolors.ENDC)
          if writeTofile:
               _scriptdir = os.path.dirname(os.path.realpath(__file__))
               with open(os.path.join(_scriptdir,"logs",f"{datetime.datetime.today().strftime('%Y%B%d')}.log"),"a",encoding="utf-8") as logFile:
                    logFile.write(f"[SUCCESS][{datetime.datetime.today().strftime('%Y%B%d@%H:%M:%S')}] {message}\n")
     elif type.upper() == "INFO" and loggingLevel >= 3:
          print(tcolors.WHITE,f"[INFO][{datetime.datetime.today().strftime('%Y%B%d@%H:%M:%S')}] {message}",tcolors.ENDC)
          if writeTofile:
               _scriptdir = os.path.dirname(os.path.realpath(__file__))
               with open(os.path.join(_scriptdir,"logs",f"{datetime.datetime.today().strftime('%Y%B%d')}.log"),"a",encoding="utf-8") as logFile:
                    logFile.write(f"[INFO][{datetime.datetime.today().strftime('%Y%B%d@%H:%M:%S')}] {message}\n")
     elif type.upper() == "DEBUG" and loggingLevel >= 4:
          print(tcolors.OKBLUE,f"[DEBUG][{datetime.datetime.today().strftime('%Y%B%d@%H:%M:%S')}] {message}",tcolors.ENDC)
          if writeTofile:
               _scriptdir = os.path.dirname(os.path.realpath(__file__))
               with open(os.path.join(_scriptdir,"logs",f"{datetime.datetime.today().strftime('%Y%B%d')}.log"),"a",encoding="utf-8") as logFile:
                    logFile.write(f"[DEBUG][{datetime.datetime.today().strftime('%Y%B%d@%H:%M:%S')}] {message}\n")

#do a basic lookup of files in the specified folder
def list_files_in_folder(service, folder_id, page_size=10):
    #build the query to search for files in the specified folder
    query = f"'{folder_id}' in parents"
    #execute the query
    results = (
        service.files()
        .list(q=query, pageSize=page_size, fields="nextPageToken, files(id, name)")
        .execute()
    )
    
    #get the list of files
    items = results.get("files", [])

    if not items:
        return None
    else:
        return items
    
#extend the normal look up function to work recursively to all depths of the folder
#service is the google api client object
#folder_id is the google drive folder id to search
#page_size is the number of results to return, helps with rate limiting
#loggingLevel is the level of logging to use to pass through to writelog - allows for controlling the verbosity deeper in the code
def list_files_in_folder_recursive(service, folder_id, page_size=10, loggingLevel=2):
     #build the query to search for files in the specified folder
     query = f"'{folder_id}' in parents"
     #execute the query
     results = (
          service.files()
          .list(q=query, pageSize=page_size, fields="nextPageToken, files(id, name, mimeType)")
          .execute()
     )

     #get the list of files
     items = results.get("files", [])
     returnItems = []
     if not items:
          writeLog(f"no items found in folder {folder_id}; returning None","warning",True,loggingLevel)
          return None
     else:
          writeLog(f"{folder_id} had: ","debug",True,loggingLevel)
          writeLog((items),"debug",True,loggingLevel)
          for item in items:
               writeLog("evaluating for deeper recurse","debug",True,loggingLevel)
               writeLog(item,"debug",True,loggingLevel)
               if item["mimeType"] == "application/vnd.google-apps.folder":
                    returnItems.append(list_files_in_folder_recursive(service, item["id"]))
               else:
                    returnItems.append(item)
          writeLog("returning: ","debug",True,loggingLevel)
          writeLog(returnItems,"debug",True,loggingLevel)
          return returnItems

#recursively unwrap the results from the recursive lookup, faltten the output for easy size caluclations
#results is expeted to be the unflattened list from the recursive lookup
def unwrapRecurseLookupResults(results):
     returnItems = []
     for item in results:
          if item:
               # print(item)
               if isinstance(item, dict):
                    # print("dict")
                    returnItems.append(item)
               elif isinstance(item, list):
                    # print("list")
                    returnItems.extend(unwrapRecurseLookupResults(item)) #extend so we dont nest lists, not append
               #elif isinstance(item, str):
                    #print("str","we went too far unwrapping")
               else:
                    print("unprocessed type", type(item))
          # else:
          #      print("skip none type entry")
     return returnItems

#lets build one big block to handle http errors
#error is the full error object returned fromHttpError
def httpErrorHandler(error, loggingLevel=1):
     match error.status_code:
          case 400:
               writeLog(f"Received 400 Bad Request\n{error}\n", "error", True, loggingLevel)
          case 401:
               writeLog(f"Received 401 Unauthorized: {error}", "error", True, loggingLevel)
          case 403:
               writeLog(f"Received 403 Forbidden: {error}", "error", True, loggingLevel)
          case 404:
               writeLog(f"Received 404 Not Found: {error}", "error", True, loggingLevel)
          case 405:
               writeLog(f"Received 405 Method Not Allowed: {error}", "error", True, loggingLevel)
          case 406:
               writeLog(f"Received 406 Not Acceptable: {error}", "error", True, loggingLevel)
          case 408:
               writeLog(f"Received 408 Request Timeout: {error}", "error", True, loggingLevel)
          case 414:
               writeLog(f"Received 414 URI Too Long: {error}", "error", True, loggingLevel)
          case 429:
               writeLog(f"Received 429 Too Many Requests: {error}", "error", True, loggingLevel)
          case 431:
               writeLog(f"Received 431 Request Header Fields Too Large: {error}", "error", True, loggingLevel)
          case 500:
               writeLog(f"Received 500 Internal Server Error: {error}", "error", True, loggingLevel)
          case 501:
               writeLog(f"Received 501 Not Implemented: {error}", "error", True, loggingLevel)
          case 502:
               writeLog(f"Received 502 Bad Gateway: {error}", "error", True, loggingLevel)
          case 503:
               writeLog(f"Received 503 Service Unavailable: {error}", "error", True, loggingLevel)
          case 504:
               writeLog(f"Received 504 Gateway Timeout: {error}", "error", True, loggingLevel)
          case 505:
               writeLog(f"Received 505 HTTP Version Not Supported: {error}", "error", True, loggingLevel)
          case 511:
               writeLog(f"Received 511 Network Authentication Required: {error}", "error", True, loggingLevel)
          case default:
               writeLog(f"An error occured but is missing a specific case: {error}", "error", True, loggingLevel)

def main():
     #prep for nice console output
     os.system('color')
     #dynamic path caching
     scriptdir = os.path.dirname(os.path.realpath(__file__))
     tokenPath = os.path.join(scriptdir,"data","token.json")
     clientSecertsPath = os.path.join(scriptdir,"local","credentials.json")
     # read ./settings.json
     # !!! reset to read the default settings file instead of the development file !!!
     with open(os.path.join(scriptdir,"local","dev.settings.json")) as settingsFile:
          settings = json.load(settingsFile)
     # establish credentials and cache it locally to token.json
     # assume if it doesnt exist or we can't get a valid status, we need to refresh
     creds = None #initialize earlier to fix scope issues
     if os.path.exists(tokenPath):
          creds = Credentials.from_authorized_user_file(tokenPath, settings["app"]["scopes"])
     if not creds or not creds.valid:
          if creds and creds.expired and creds.refresh_token:
               creds.refresh(Request())
          else:
               flow = InstalledAppFlow.from_client_secrets_file(
                    clientSecertsPath,  settings["app"]["scopes"]
               )
               creds = flow.run_local_server(port=0)
          with open(tokenPath, "w") as token:
               token.write(creds.to_json())

     #if we get good credentials, lets integrate and start to evalute the source
     try:
          service = build("drive", "v3", credentials=creds)
          if settings["app"]["clearDestOnRun"]:
               writeLog("clearing destination folder","info",True,settings["app"]["loggingLevel"])
          #1 - count files and folders in root of src
          writeLog("starting to count files in source root","info",True,settings["app"]["loggingLevel"])
          rootFiles = list_files_in_folder(service, settings["app"]["sourceFolderID"])
          if rootFiles != None:
               writeLog("found the following data at the root of src","debug",True,settings["app"]["loggingLevel"])
               writeLog(rootFiles,"debug",True,settings["app"]["loggingLevel"])
               writeLog(f"there are {len(rootFiles)} files in the source root","success",True,settings["app"]["loggingLevel"])
               #2 - count files and folders in src recursively
               writeLog("starting to count files in source recursively","info",True,settings["app"]["loggingLevel"])
               recurseFiles = []
               fileTreeDict = {}
               #loop through each of these top level folders and recurse so we dont pull them again
               for item in rootFiles:
                    results = list_files_in_folder_recursive(service, item["id"],settings["app"]["loggingLevel"]) 
                    recurseFiles.append(results)
                    #intialize the key if it doesnt exist, then append the structured results (!!!don't flatten to preserve structure for file copying)
                    fileTreeDict.setdefault(item["id"], []).append(results)
               writeLog("found the following data recursing through the subfolders","debug",True,settings["app"]["loggingLevel"])
               writeLog(recurseFiles,"debug",True,settings["app"]["loggingLevel"])
               unwrappedrecurseFiles = unwrapRecurseLookupResults(recurseFiles)
               writeLog("found the following data unwrapping the recursive lookup data","debug",True,settings["app"]["loggingLevel"])
               writeLog(unwrappedrecurseFiles,"debug",True,settings["app"]["loggingLevel"])
               writeLog(f"there are {len(unwrappedrecurseFiles)+len(rootFiles)} files in the source recursively","success",True,settings["app"]["loggingLevel"])
               #3 - copy all the content from src to dest
               writeLog("starting to copy all files from source to destination","info",True,settings["app"]["loggingLevel"])
          else:
               writeLog(f"failed to get files in source","error",True,settings["app"]["loggingLevel"])
     except HttpError as error:
          httpErrorHandler(error,settings["app"]["loggingLevel"])
 
    

#main
if __name__ == "__main__":
     main()
