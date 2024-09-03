#fresh slate, v1 was getting messy

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
from googleapiclient.http import MediaFileUpload

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

#custom logging function that prints to console and writes to a file (optional)
#users colors to differentiat between log levels in the console
#uses tags to differentiate between log levels in the file
def writeLog(message, type, writeTofile=True,loggingLevel=2):
     if loggingLevel == 0:
          return
     _scriptdir = os.path.dirname(os.path.realpath(__file__))
     if type.upper() == "ALWAYS":
          print(tcolors.OKCYAN,f"[{datetime.datetime.today().strftime('%Y%B%d@%H:%M:%S')}] {message}",tcolors.ENDC)
          if writeTofile:
               _scriptdir = os.path.dirname(os.path.realpath(__file__))
               with open(os.path.join(_scriptdir,"logs",f"{datetime.datetime.today().strftime('%Y%B%d')}.log"),"a",encoding="utf-8") as logFile:
                    logFile.write(f"[{datetime.datetime.today().strftime('%Y%B%d@%H:%M:%S')}] {message}\n")
     elif type.upper() == "ERROR" and loggingLevel >= 1:
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
          case _:
               writeLog(f"An error occured but is missing a specific case: {error}", "error", True, loggingLevel)

#attempt to authenticate the user with the provided scopes
#errors when the app credentials json is missing or an interactive browser cannot be invoked (e.g. headless server)
def authenticate(scopes,loggingLevel=2):
     creds = None
     tokenPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data","token.json")
     clientSecertsPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"local","credentials.json")
     writeLog("attempting to authenticate", "info", True, loggingLevel)
     #if the token file exists, delete it to force a new token
     if os.path.exists(tokenPath):
          os.remove(tokenPath) #get around google not returning a refresh_token in our token.json - otherwise we'd use the existing token
          #creds = Credentials.from_authorized_user_file(tokenPath)
     
     #make sure a the app creds are present
     if not os.path.exists(clientSecertsPath):
          writeLog(f"credential file is missing! please generate a credential related to a Google project before continuing and place it at {clientSecertsPath}", "error", True, loggingLevel)
          return

     
     #if not creds or not creds.valid: #no longer needed - keeping in case we need to revert
     #writeLog("no valid credentials found, requesting new ones", "warning", True, loggingLevel)
     # if creds and creds.expired and creds.refresh_token: #no longer needed - keeping in case we need to revert
     #      creds.refresh(Request())
     # else:
     #writeLog("no refresh token found, requesting new ones", "warning", True, loggingLevel)
     #request
     writeLog("requesting new auth token", "info", True, loggingLevel)
     flow = InstalledAppFlow.from_client_secrets_file(clientSecertsPath, scopes=scopes)
     creds = flow.run_local_server(port=0)
     with open(tokenPath, 'w') as token:
          writeLog(f"writing new token to file [{tokenPath}]", "info", True, loggingLevel)
          token.write(creds.to_json())

     service = build('drive', 'v3', credentials=creds)
     return service

#v1 had issues digging deep into heavily nested folders, like King the Land
#lets make sure we loop to get all paginated data this time
def listFilesInFolder(service,folderID,loggingLevel=2):
     results = []
     pageT = None
     #keep collecting pages until we run out
     while True:
          writeLog(f"getting page {pageT} of folder {folderID}", "debug", True, loggingLevel)
          response = service.files().list(
               q=f"'{folderID}' in parents",
               spaces='drive',
               fields='nextPageToken, files(id, name, mimeType,parents)',
               pageToken=pageT
          ).execute()
          #add the files to the results (flat so we can process better down the line)
          results.extend(response.get('files', []))
          pageT = response.get('nextPageToken')
          #no more pages, break the loop
          if pageT is None:
               writeLog(f"no next page - done!", "debug", True, loggingLevel)
               break
     writeLog(f"found {len(results)} items in folder {folderID}", "info", True, loggingLevel)
     return results

#recursively count through the folders to find the number of child objects and nested folders
def countChildObjects(service,folderID,loggingLevel=2):
     childFiles = listFilesInFolder(service,folderID) #get all the files in the folder
     totalFiles = len(childFiles) #count the files in the folder
     nestedFolders = 0 #keep track of how many nested folders we encounter
     folderStructure = [] #map this as we go to throw in the report later
     for file in childFiles:
          if file['mimeType'] == "application/vnd.google-apps.folder":
               writeLog(f"found nested folder {file['name']} in folder {folderID} - recursing", "info", True, loggingLevel)
               nestedFolders += 1 #increment because we found another nested folder
               nestedCount, nestedFolderCount,nestedStructure = countChildObjects(service,file['id']) #recurse
               totalFiles += nestedCount #add the files in the nested folder to the total
               nestedFolders += nestedFolderCount #add the nested folders in the nested folder to the total
               writeLog(f"nested folder {file['name']} had {nestedCount} items, including {nestedFolderCount} nested folders", "debug", True, loggingLevel)
               folderStructure.append({
                    "name": file['name'],
                    "id": file['id'],
                    "mimeType": file['mimeType'],
                    "parents": file['parents'],
                    "children":nestedStructure
               })
          else: #probably not a folder, lets just mark it as an individual item
               writeLog(f"found file {file['name']} in folder {folderID}", "info", True, loggingLevel)
               folderStructure.append({
                    'name': file['name'],
                    'id': file['id'],
                    'mimeType': file['mimeType'],
                    "parents": file['parents'],
               })
     return totalFiles, nestedFolders, folderStructure

#prepare the final report for the recursive lookup of the nested folders and files
def finalReportRecurse(service,sourceFolderID,destinationFolderID,loggingLevel=2,bufferSize=80):
     separatorLine = "=" * bufferSize
     report = [
          f"\n{separatorLine}",
          f"{'FINAL REPORT - RECURSIVE LOOKUP'.center(bufferSize)}",
          f"{separatorLine}"
     ]
     totalNestedFolders=0
     #get the initial folders in the source folder
     topLevelFolders = listFilesInFolder(service,sourceFolderID)
     #folderStructure = []
     #go through each folder and kick of the recursive check from countChildObjects
     for folder in topLevelFolders:
          if folder['mimeType'] == "application/vnd.google-apps.folder":
               totalFiles,nestedFolders,structure = countChildObjects(service, folder['id'],loggingLevel)
               report.append(f"[{folder['name']}: {folder['id']}] had [{totalFiles}] items, including [{nestedFolders}] nested folders.")
               totalNestedFolders += nestedFolders
               # folderStructure.append({
               #      "name": folder['name'],
               #      "id": folder['id'],
               #      "mimeType": folder['mimeType'],
               #      "parents": folder['parents'],
               #      "children": structure
               # })
     totalFilesInRoot,_,rootStructure  = countChildObjects(service,sourceFolderID)
     #poke the source back at the start of the structure
     # folderStructure.insert(0, {
     #      'name': 'Source Root',
     #      'id': sourceFolderID,
     #      'mimeType': 'application/vnd.google-apps.folder',
     #      'children': rootStructure
     # })
     #wrap the file structure map into a source based signifier
     reportStructure = {
          'name': 'Source Root',
          'id': sourceFolderID,
          'mimeType': 'application/vnd.google-apps.folder',
          'children': rootStructure
     }
     report.append(f"{separatorLine}")
     report.append(f"Total nested folders in source folder: {totalNestedFolders}")
     report.append(f"Total files in source folder including all nested items: {totalFilesInRoot}")
     report.append(f"{separatorLine}")
     #write to a file and upload to the destination folder
     #structure json write and upload
     reportName = f"{datetime.datetime.today().strftime('%Y%B%d@%H_%M_%S')}-a#2-fileStructureReport.json"
     reportPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data",reportName)
     with open(reportPath, "w") as jsonFile:
          json.dump(reportStructure, jsonFile, indent=4)
     uploadFile(service,destinationFolderID,reportPath,reportName,loggingLevel)
     #human readable report write and upload
     #TODO: ship  JSON to next step of the process instead of writing to a file
     reportName = f"{datetime.datetime.today().strftime('%Y%B%d@%H_%M_%S')}-a#2-recurisveLookup.txt"
     reportPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data",reportName)
     with open(reportPath, "w") as file:
          file.write("\n".join(report))
     uploadFile(service,destinationFolderID,reportPath,reportName,loggingLevel)

     return "\n".join(report)

#for a#1 - we just need the root folders, not the recursion in the other functions
#lets reduce how we look at the source folder
def getRootFilesAndFolders(service, sourceFolderId,loggingLevel=2):
     #get the folders
     files = listFilesInFolder(service, sourceFolderId,loggingLevel)
     #get the file structure for reporting
     structure = []
     for file in files:
          structure.append({
               "name": file['name'],
               "id": file['id'],
               "mimeType": file['mimeType'],
               "parents": file['parents']
          })
     #wrap the file structure map into a source based signifier
     rootStructure = {
          'name': 'Source Root',
          'id': sourceFolderId,
          'mimeType': 'application/vnd.google-apps.folder',
          'children': structure
    }
     return rootStructure

#build a report for a#1 and upload it to the destination folder
def finalReportRoot(service,results,destinationFolderID,loggingLevel=2,bufferSize=80):
     separatorLine = "=" * bufferSize
     report = [
          f"\n{separatorLine}",
          f"{'FINAL REPORT - ROOT LOOKUP'.center(bufferSize)}",
          f"{separatorLine}"
     ]
     for i in range(len(results['children'])):
          item = results['children'][i]
          report.append(f"{i+1}. [{item['name']}: {item['id']}]")
     report.append(f"{separatorLine}")
     report.append(f"Total nested folders in source folder: {len(results['children'])}")
     report.append(f"{separatorLine}")

     #structure json write and upload
     reportName = f"{datetime.datetime.today().strftime('%Y%B%d@%H_%M_%S')}-a#1-fileStructureReport.json"
     reportPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data",reportName)
     with open(reportPath, "w") as jsonFile:
          json.dump(results, jsonFile, indent=4)
     uploadFile(service,destinationFolderID,reportPath,reportName,loggingLevel)
     #human readable report write and upload
     reportName = f"{datetime.datetime.today().strftime('%Y%B%d@%H_%M_%S')}-a#1-rootLookup.txt"
     reportPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data",reportName)
     with open(reportPath, "w") as file:
          file.write("\n".join(report))
     uploadFile(service,destinationFolderID,reportPath,reportName,loggingLevel)

     return "\n".join(report)

#a simple helper script to help upload files to the drive
def uploadFile(service,fileID,filePath,fileName,loggingLevel=2):
     fileMetadata = {
          'name': fileName,
          'parents': [fileID]
     }
     media = MediaFileUpload(filePath)
     file = service.files().create(
          body=fileMetadata, 
          media_body=media, 
          fields='id'
     ).execute()
     
     if file:
          return file.get('id')

#clears out the destination folder to be sure we're clean before starting another copy test
def clearDestinationFolder(service, destinationFolderId,loggingLevel=2):
     files = listFilesInFolder(service, destinationFolderId,loggingLevel)
     for file in files:
          try:
               writeLog(f"deleting {file['name']} from destination folder", "info", True, loggingLevel)
               service.files().delete(fileId=file['id']).execute()
               writeLog(f"deleted {file['name']} from destination folder", "success", True, loggingLevel)
          except HttpError as error:
               httpErrorHandler(error,loggingLevel)
     writeLog(f"destination folder {destinationFolderId} is now empty - {len(files)} items removed", "success", True, loggingLevel)

#a helper function to copy a file or folder from the source to the destination
#this function will recurse on folders, preserving file structure
def copyItem(service,file,destinationFolderID,loggingLevel=2):
     itemsCopied = 0
     fileProperties = {
          'name': file['name'],
          'parents': [destinationFolderID]
     }
     #folder found, make it in the correct are, preserving structure
     #recurse on the folder's contents to copy everything
     if file['mimeType'] == 'application/vnd.google-apps.folder':
          writeLog(f"creating folder {file['name']} in destination folder", "info", True, loggingLevel)
          newFolder = service.files().create(
               body={
                    'name': file['name'],
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [destinationFolderID]
               }
          ).execute()
          sourcefiles = listFilesInFolder(service, file['id'],loggingLevel)
          writeLog(f"copying {len(sourcefiles)} files to {destinationFolderID}","info",True,loggingLevel)
          itemsCopied += 1
          for file in sourcefiles:
               itemsCopied += copyItem(service,file,newFolder['id'],loggingLevel)
     else:
          writeLog(f"copying file {file['name']} to {destinationFolderID}","info",True,loggingLevel)
          service.files().copy(
               fileId=file['id'], 
               body=fileProperties
          ).execute()
          itemsCopied += 1
     return itemsCopied
          

def main():
     #prep for nice console output
     os.system('color')
     #dynamic path caching
     scriptdir = os.path.dirname(os.path.realpath(__file__))
     #load settings
     with open(os.path.join(scriptdir,"settings.json")) as settingsFile:
          settings = json.load(settingsFile)
     #make sure all the folders we need are present
     if not os.path.exists(os.path.join(scriptdir,"logs")):
          os.makedirs(os.path.join(scriptdir,"logs"))
          writeLog("logs folder wasn't detected and has been created", "warning", True, settings['app']['loggingLevel'])
     if not os.path.exists(os.path.join(scriptdir,"data")):
          os.makedirs(os.path.join(scriptdir,"data"))
          writeLog("data folder wasn't detected and has been created", "warning", True, settings['app']['loggingLevel'])
     if not os.path.exists(os.path.join(scriptdir,"local")):
          os.makedirs(os.path.join(scriptdir,"local"))
          writeLog("local folder wasn't detected and has been created - please place your credentials.json file in this folder before running again", "error", True, settings['app']['loggingLevel'])
          return
     #authenticate the user on google
     service = authenticate(settings['app']['scopes'],settings['app']['loggingLevel'])
     if service is None:
          writeLog("failed to authenticate, exiting", "error", True, settings['app']['loggingLevel'])
          return
     menu = [
          f"{tcolors.OKCYAN}",
          "\n"+"="*50,
          f"Current source: https://drive.google.com/drive/folders/{settings['app']['sourceFolderID']}",
          f"Current destination: https://drive.google.com/drive/folders/{settings['app']['destinationFolderID']}",
          f"Current logging level: (higher is more verbose): {settings['app']['loggingLevel']}"
          "\n"+"="*50,
          "1. Generate a report that shows the number of files and folders in total at the root of the source folder",
          "2. Generate a report that shows the number of child objects (recursively)",
          "3. Copy the content (nested files/folders) of the source folder to the destination folder",
          ""
          "0. Quit",
          "Please select an option to run:",
          f"{tcolors.ENDC}"
     ]
     userInput = -1
     while userInput != "0":
          #writeLog("\n".join(menu), "always", True, settings['app']['loggingLevel'])
          userInput = input("\n".join(menu))
          writeLog(f"selected option {userInput}", "info", True, settings['app']['loggingLevel'])
          match userInput:
               case "1":#1 - count files and folders in root of src
                    writeLog("generating report for root folder", "info", True, settings['app']['loggingLevel'])
                    folderStructure = getRootFilesAndFolders(service,settings['app']['sourceFolderID'],settings['app']['loggingLevel'])
                    report = finalReportRoot(service,folderStructure,settings['app']['destinationFolderID'],settings['app']['loggingLevel'])
                    #writeLog(report, "always", True, settings['app']['loggingLevel'])
                    print(tcolors.OKCYAN,report,tcolors.ENDC)
                    input(f"{tcolors.OKGREEN}Report generated, saved, and uploaded!\nPress enter to continue{tcolors.ENDC}")
               case "2":#2 - count files and folders in src recursively
                    writeLog("generating recursive report", "info", True, settings['app']['loggingLevel'])
                    report = finalReportRecurse(service,settings['app']['sourceFolderID'],settings['app']['destinationFolderID'],settings['app']['loggingLevel'])
                    #writeLog(report, "always", True, settings['app']['loggingLevel'])
                    print(tcolors.OKCYAN,report,tcolors.ENDC)
                    input(f"{tcolors.OKGREEN}Report generated, saved, and uploaded!\nPress enter to continue{tcolors.ENDC}")
               case "3":#3 - copy all the content from src to dest
                    writeLog("copying content from source to destination", "info", True, settings['app']['loggingLevel'])
                    #check if we flagged to clear the destination on the next copy run 
                    if settings["app"]["clearDestOnRun"]:
                         writeLog("clearing destination folder - set [clearDestOnRun] to [false] in settings.json to prevent this","warning",True,settings["app"]["loggingLevel"])
                         clearDestinationFolder(service,settings['app']['destinationFolderID'],settings['app']['loggingLevel'])
                    #get the basefiles in the source
                    files = listFilesInFolder(service, settings['app']['sourceFolderID'],settings['app']['loggingLevel'])
                    #go through all the root folders and files and copy them to the destination
                    copies = 0
                    for file in files:
                         copies = copyItem(service,file,settings['app']['destinationFolderID'],settings['app']['loggingLevel'])
                    writeLog(f"copied {copies} items from source [{settings['app']['sourceFolderID']}] to destination [{settings['app']['destinationFolderID']}]", "success", True, settings['app']['loggingLevel'])
                    input(f"{tcolors.OKGREEN}Files copied!\nPress enter to continue{tcolors.ENDC}")
               case "0":
                    writeLog("Quitting", "info", True, settings['app']['loggingLevel'])
               case _:
                    writeLog("Invalid input, please try again", "always", True, settings['app']['loggingLevel'])

if __name__ == "__main__":
     main()