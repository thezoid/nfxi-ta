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
     if type.upper() == "ERROR" and loggingLevel >= 1:
          print(tcolors.FAIL,f"!!![{datetime.datetime.today().strftime('%Y%B%d@%H:%M:%S')}] {message}",tcolors.ENDC)
          if writeTofile:
               _scriptdir = os.path.dirname(os.path.realpath(__file__))
               with open(os.path.join(_scriptdir,f"logs/{datetime.datetime.today().strftime('%Y%B%d')}scraper.log"),"a",encoding="utf-8") as logFile:
                    logFile.write(f"!!![{datetime.datetime.today().strftime('%Y%B%d@%H:%M:%S')}] {message}\n")
     elif type.upper() == "WARNING" and loggingLevel >= 2:
               print(tcolors.WARNING,f"![{datetime.datetime.today().strftime('%Y%B%d@%H:%M:%S')}] {message}",tcolors.ENDC)
               if writeTofile:
                    _scriptdir = os.path.dirname(os.path.realpath(__file__))
                    with open(os.path.join(_scriptdir,f"logs/{datetime.datetime.today().strftime('%Y%B%d')}scraper.log"),"a",encoding="utf-8") as logFile:
                         logFile.write(f"![{datetime.datetime.today().strftime('%Y%B%d@%H:%M:%S')}] {message}\n")
     elif type.upper() == "INFO" and loggingLevel >= 3:
          print(tcolors.WHITE,f"*[{datetime.datetime.today().strftime('%Y%B%d@%H:%M:%S')}] {message}",tcolors.ENDC)
          if writeTofile:
               _scriptdir = os.path.dirname(os.path.realpath(__file__))
               with open(os.path.join(_scriptdir,f"logs/{datetime.datetime.today().strftime('%Y%B%d')}scraper.log"),"a",encoding="utf-8") as logFile:
                    logFile.write(f"*[{datetime.datetime.today().strftime('%Y%B%d@%H:%M:%S')}] {message}\n")

def main():
     #prep for nice console output
     os.system('color')
     #vars
     scriptdir = os.path.dirname(os.path.realpath(__file__))
     # read ./settings.json
     with open(scriptdir+"/settings.dev.json") as settingsFile: #!!!CHANGE THIS BACK TO DEFAULT TO settings.json!!!
          settings = json.load(settingsFile)
     # establish credentials and cache it locally to token.json
     # assume if it doesnt exist or we can't get a valid status, we need to refresh
     creds = None #initialize earlier to fix scope issues
     if os.path.exists(scriptdir+"/data/token.json"):
          creds = Credentials.from_authorized_user_file("token.json", settings["app"]["scopes"])
     if not creds or not creds.valid:
          if creds and creds.expired and creds.refresh_token:
               creds.refresh(Request())
          else:
               flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", settings["app"]["scopes"]
               )
               creds = flow.run_local_server(port=0)
          with open("token.json", "w") as token:
               token.write(creds.to_json())

     #if we get good credentials, lets integrate and start to evalute the source
     try:
          service = build("drive", "v3", credentials=creds)
          results = (
               service.files()
               .list(pageSize=10, fields="nextPageToken, files(id, name)")
               .execute()
          )
          items = results.get("files", [])

          if not items:
               print("No files found.")
          print("Files:")
          for item in items:
               print(f"{item['name']} ({item['id']})")
     except HttpError as error:
          match error:
               case default:
                    print(f"An error occurred: {error}")

     #1 - count files and folders in root of src
     writeLog("starting to count files in source root","info",True,settings["app"]["loggingLevel"])
     count = 0
     writeLog(f"there are {count} files in the source root","info",True,settings["app"]["loggingLevel"])
     #2 - count files and folders in src recursively
     writeLog("starting to count files in source recursively","info",True,settings["app"]["loggingLevel"])
     count = 0
     writeLog(f"there are {count} files in the source recursively","info",True,settings["app"]["loggingLevel"])
     #3 - copy all the content from src to dest
     writeLog("starting to copy all files from source to destination","info",True,settings["app"]["loggingLevel"])

#main
if __name__ == "__main__":
     main()

