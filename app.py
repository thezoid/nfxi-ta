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

#funcs

#something fun to blow off steam - benign
def printLogo():
     art = '''                                
                         .:^~~!!!!~~^:.                         
                    :^!?J5PGGGGGGGGGGGP5Y?!:.                   
                .^7J55555555PGGGGGGGGGGGGGGGPJ!.                
              :7J5555555555555PGGGGGGGGGGBBBBBBPJ~              
            ^?Y5555555PP5555555YPGGBGGBBBBBGGGGGGG5!.           
          .7YYYYJ!~~!!7J5PP55YJJY5PGBBBG5?7~~!7YGGGGY^          
         !PP5YJJ:.:~!~~^~?7!~~!7?7!~!7?~:::^~^::5GPPPP7.        
        7GGGGGGY^~7PBP!^::::::::..   ...:^JGG?~^?BGPGGGJ.       
       !GGGGGGGG~~?G5!..::::::::.........:~YGJ~^PBGGGGGG?:.     
      :PGGGGPPGBP~::. .....:::::.....  .::::^^^YBG555PGGG!..    
      JGGGPP555PG^ ......:::::::... .^~^::::::^5GPYJJY5PG5^.    
     .PGP55555557......:~JYY!:::...^Y55J!^:::::!GPYJJJJJY5!:.   
     :YY5555555Y:....:^^^~?5~..  ..:J5J?77!^::^:YBP5JJJJY57^.   
     .JJJY55555~ .:^~~^^^^^:        ^777777?!^^:~GGPP5Y5557^.   
      ?YJJJYY5J.:^~~!7!~^^:..:~!!!^:^~7777??!~~~^7GP555555!^.   
      ~YJJJJJYJ~^^^^~7?7!^.. J####G^^^!??JJ!~~~~!?PP55555J~^.   
      .?YJYY55PGY7~^^~7777^..~5GGP?:^~?JJJ7~~~7YGGPPP5555!~:.   
       :J555555GGG5?~^!7777!~!7JYJ?7!?JJJ?~~?5GBBGPPPPP57~^.    
        ^YP5555PGGGGPY!77777!^^^!~~7JJ???7JPBBBBGPPPPGP?~^:.    
         :JP5555GGGGGGG5J?7777Y555JJJ?JYPGBBGGGGPPPPP57~^:.     
          .!YP55PGGGGGGGGPY?77JPP5??J5PBBBGGGGBGPPPPJ!~^:.      
            :!Y5PGGGGGGGGGGG5J7YPJY5GBBBGGGGGBBGP5J!~^:.        
              .~?5GGGGGGGGGGGGP55PGBBGGGGBBBBBGY?!~^:..         
                .:!J5PGGGGGGGGGPGBBBBBBBBBGPY?!~^^:..           
                   .:^!?JY5PPPPPGGGGPP5YJ?!~^^^:..              
                       ..:^^~~!!!!!!~~^^^:::..                  
                            .............                       
     '''
     print(tcolors.OKGREEN,art,tcolors.ENDC)

def printTitleCard():
     art = '''                           
                         .:^~~!!!!~~^:.                         
                    :^!?J5PGGGGGGGGGGGP5Y?!:.                   
                .^7J55555555PGGGGGGGGGGGGGGGPJ!.                
              :7J5555555555555PGGGGGGGGGGBBBBBBPJ~              
            ^?Y5555555PP5555555YPGGBGGBBBBBGGGGGGG5!.           
          .7YYYYJ!~~!!7J5PP55YJJY5PGBBBG5?7~~!7YGGGGY^          
         !PP5YJJ:.:~!~~^~?7!~~!7?7!~!7?~:::^~^::5GPPPP7.        
        7GGGGGGY^~7PBP!^::::::::..   ...:^JGG?~^?BGPGGGJ.       
       !GGGGGGGG~~?G5!..::::::::.........:~YGJ~^PBGGGGGG?:.     
      :PGGGGPPGBP~::. .....:::::.....  .::::^^^YBG555PGGG!..    
      JGGGPP555PG^ ......:::::::... .^~^::::::^5GPYJJY5PG5^.    
     .PGP55555557......:~JYY!:::...^Y55J!^:::::!GPYJJJJJY5!:.   
     :YY5555555Y:....:^^^~?5~..  ..:J5J?77!^::^:YBP5JJJJY57^.   
     .JJJY55555~ .:^~~^^^^^:        ^777777?!^^:~GGPP5Y5557^.   
      ?YJJJYY5J.:^~~!7!~^^:..:~!!!^:^~7777??!~~~^7GP555555!^.   
      ~YJJJJJYJ~^^^^~7?7!^.. J####G^^^!??JJ!~~~~!?PP55555J~^.   
      .?YJYY55PGY7~^^~7777^..~5GGP?:^~?JJJ7~~~7YGGPPP5555!~:.   
       :J555555GGG5?~^!7777!~!7JYJ?7!?JJJ?~~?5GBBGPPPPP57~^.    
        ^YP5555PGGGGPY!77777!^^^!~~7JJ???7JPBBBBGPPPPGP?~^:.    
         :JP5555GGGGGGG5J?7777Y555JJJ?JYPGBBGGGGPPPPP57~^:.     
          .!YP55PGGGGGGGGPY?77JPP5??J5PBBBGGGGBGPPPPJ!~^:.      
            :!Y5PGGGGGGGGGGG5J7YPJY5GBBBGGGGGBBGP5J!~^:.        
              .~?5GGGGGGGGGGGGP55PGBBGGGGBBBBBGY?!~^:..         
                .:!J5PGGGGGGGGGPGBBBBBBBBBGPY?!~^^:..           
                   .:^!?JY5PPPPPGGGGPP5YJ?!~^^^:..              
                       ..:^^~~!!!!!!~~^^^:::..                  
                            .............                       
    '''

     title = "Google Drive Integration Practice"
     author = "Author: Zoid"
     socialUrls = "GitHub: github.com/thezoid | Twitter: @zoid__"
     description = (
          "1: Report the total number of files and folders in the root of a given source Drive folder (by ID)\n"
          "2: Report the number of child objects (recurisvely) for each top-level folder in the source Drive folder\n"
          "3: Copy the content of the source Drive folder to a destination Drive folder, preserving the folder structure\n"
     )

     #split the ASCII art into lines and determine the width
     artLines = art.splitlines()
     artWidth = max(len(line) for line in artLines)

     #get the section line buffers
     sectionBuffer = max(len(line) for line in [title, author, socialUrls])
     #define the text lines
     textLines = [
          "",
          title,
          "-" * sectionBuffer, #len(title),
          author,
          "-" * sectionBuffer,#len(author),
          socialUrls,
          "-" * sectionBuffer,#len(socialUrls),
          description.split("\n")[0], #TODO: do this dynamically, not hardcoded
          description.split("\n")[1],
          description.split("\n")[2],
          ""
     ]

    # Ensure `textLines` has the same number of lines as `artLines`
     while len(textLines) < len(artLines):
          textLines.append("")

     # Calculate the max text width
     textWidth = max(len(line) for line in textLines)

     # Calculate total width for borders, considering the art width and text width
     totalWidth = artWidth + textWidth + 8  # 4 spaces padding on each side

     # Create the top and bottom borders
     border = "=" * totalWidth

     # Prepare each text line to be evenly spaced from the art
     spacedTextLines = []
     for i, line in enumerate(textLines):
          if i < len(artLines):
               padding = " " * (artWidth - len(artLines[i]) + 4)  # 4 spaces gap
               spacedTextLines.append(padding + line.ljust(textWidth))
          else:
               spacedTextLines.append(" " * (artWidth + 4) + line.ljust(textWidth))

     # Merge the art and the text lines
     finalOutput = "\n".join(
          [artLines[i] + spacedTextLines[i] for i in range(len(artLines))]
     )

     # Print the final title card with borders
     print(tcolors.OKGREEN,f"\n{border}")
     print(finalOutput)
     print(f"{border}\n",tcolors.ENDC)

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
          case default:
               writeLog(f"An error occured but is missing a specific case: {error}", "error", True, loggingLevel)

#do a basic lookup of files in the specified folder
def listFilesInFolder(service, folderID, page_size=10,loggingLevel=2):
     #build the query to search for files in the specified folder
     query = f"'{folderID}' in parents"
     #execute the query
     results = (
          service.files()
          .list(
               q=query, 
               pageSize=page_size, 
               fields="nextPageToken, files(id, name,mimeType,parents)"
          )
          .execute()
     )
     #get the list of files
     items = results.get("files", [])
     if items is None or len(items) == 0:
          writeLog(f"no items found in folder with id {folderID}","warning",True,loggingLevel)
          return None
     else:
          return items
    
#extend the normal look up function to work recursively to all depths of the folder
#service is the google api client object
#folder_id is the google drive folder id to search
#page_size is the number of results to return, helps with rate limiting
#loggingLevel is the level of logging to use to pass through to writelog - allows for controlling the verbosity deeper in the code
def listFilesInFolderRecursive(service, folderID, pageSize=10, loggingLevel=2):
     #build the query to search for files in the specified folder
     query = f"'{folderID}' in parents"
     #execute the query
     results = (
          service.files()
          .list(q=query, pageSize=pageSize, fields="nextPageToken, files(id, name, mimeType,parents)")
          .execute()
     )

     #get the list of files
     items = results.get("files", [])
     returnItems = []
     if items is None or len(items) == 0:
          writeLog(f"no items found in folder with id {folderID}","warning",True,loggingLevel)
          return None
     else:
          writeLog(f"{folderID} had: ","debug",True,loggingLevel)
          writeLog((items),"debug",True,loggingLevel)
          for item in items:
               writeLog("evaluating for deeper recurse","debug",True,loggingLevel)
               writeLog(item,"debug",True,loggingLevel)
               if item["mimeType"] == "application/vnd.google-apps.folder":
                    returnItems.append(listFilesInFolderRecursive(service, item["id"],pageSize,loggingLevel))
               else:
                    returnItems.append(item)
          writeLog("returning: ","debug",True,loggingLevel)
          writeLog(returnItems,"debug",True,loggingLevel)
          return returnItems

#recursively unwrap the results from the recursive lookup, faltten the output for easy size caluclations
#results is expeted to be the unflattened list from the recursive lookup
def unwrapRecurseLookupResults(results, loggingLevel=1):
     returnItems = []
     for item in results:
          if item:
               if isinstance(item, dict):
                    returnItems.append(item)
               elif isinstance(item, list):
                    returnItems.extend(unwrapRecurseLookupResults(item)) #extend so we dont nest lists, not append
               else:
                    print("unprocessed type", type(item))
     return returnItems

#copy a file from one folder to another; helper function for copyFolder (or for user elsewhere)
def copyFile(service, fileID, destFolderID, loggingLevel=2):
    copiedFileProperties = {'parents': [destFolderID]}
    writeLog(f"copying file {fileID} to folder {destFolderID} with properties {copiedFileProperties}","info",True,loggingLevel)
    service.files().copy(
          fileId=fileID, 
          body=copiedFileProperties
     ).execute()

#copy a folder from the source to the destionatiion id
#if it detects any folders as it is copying, it will recurse to ensure that all contents are copied over
def copyFolder(service, sourceFolderId, destFolderId, loggingLevel=2):
     filesCopied = 0
     files = listFilesInFolder(service, sourceFolderId,loggingLevel=loggingLevel)
     if files:
          writeLog(f"copying {len(files)} files from {sourceFolderId} to {destFolderId}","info",True,loggingLevel)
          for file in files:
               if file['mimeType'] == 'application/vnd.google-apps.folder':
                    writeLog(f"found nested folder!! creating folder {file['name']} in {destFolderId} and starting a copy","info",True,loggingLevel)
                    newFolder = service.files().create(
                         body={
                              'name': file['name'],
                              'mimeType': 'application/vnd.google-apps.folder',
                              'parents': [destFolderId]
                         }
                    ).execute()
                    filesCopied += copyFolder(service, file['id'], newFolder['id'],loggingLevel)
               else:
                    writeLog(f"copying file {file['name']} to {destFolderId}","info",True,loggingLevel)
                    copyFile(service, file['id'], destFolderId,loggingLevel)
                    filesCopied += 1
     return filesCopied

#help us get a clean state when the debug flag clearDestOnRun is set to true
# TODO: add some verification in here that clearDestOnRun is indeed set to true incase something happens in main() where it is called
def clearFolder(service, folderID, loggingLevel=2):
     files = listFilesInFolder(service, folderID,loggingLevel=loggingLevel)
     if files is not None:  # Check if files is not None
          writeLog(f"deleting {len(files)} files in folder {folderID}","warning",True,loggingLevel)
          for file in files:
               try:
                    writeLog(f"deleting file {file['name']}","info",True,loggingLevel)
                    service.files().delete(fileId=file["id"]).execute()
               except HttpError as error:
                    httpErrorHandler(error,loggingLevel)
          writeLog(f"finished deleting {len(files)} files in folder {folderID}","success",True,loggingLevel)

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

#generate the final report of the  script run
#uses basic formatting to generate a nice looking report, with dynamic alignment 
def finalReporting(fileCounts, bufferSize=50):
     totalFiles = 0
     separatorLine = "=" * bufferSize
     reportString = f"\n{separatorLine}\n"
     reportString += f"{'FINAL REPORT'.center(bufferSize)}\n"
     reportString += f"{separatorLine}\n"

     # Calculate the maximum length of keys for alignment
     maxKeyLength = max(len(key) for key in fileCounts.keys())

     # TODO: don't hard code this, let's dunamically make it the first after a sort
     key = "Source Root"
     reportString += f"[{key.ljust(maxKeyLength)}] contained [{fileCounts[key][0]:>2}] items\n"
     for key in sorted(fileCounts.keys()):
          if key != "Source Root":
               reportString += f"[{key.ljust(maxKeyLength)}] contained [{fileCounts[key][0]:>2}] items\n"
               totalFiles+=fileCounts[key][0]

     reportString += f"{separatorLine}\n"
     reportString += f"Total root files: {fileCounts['Source Root'][0]}"+"\n"#.center(bufferSize) + "\n"
     reportString += f"Total nested files: {totalFiles}"+"\n"#.center(bufferSize) + "\n"
     reportString += f"Total files: {totalFiles+fileCounts['Source Root'][0]}"+"\n"#.center(bufferSize) + "\n"
     reportString += f"{separatorLine}\n"

     return reportString

def main():
     #prep for nice console output
     os.system('color')
     #dynamic path caching
     scriptdir = os.path.dirname(os.path.realpath(__file__))
     tokenPath = os.path.join(scriptdir,"data","token.json")
     clientSecertsPath = os.path.join(scriptdir,"local","credentials.json")
     finalOutputPath = os.path.join(scriptdir,"data",f"{datetime.datetime.today().strftime('%Y%B%d@%H_%M_%S')}-report.txt")
     finalJSONPath = os.path.join(scriptdir,"data",f"{datetime.datetime.today().strftime('%Y%B%d@%H_%M_%S')}-report.json")
     finalDATAPath = os.path.join(scriptdir,"data",f"{datetime.datetime.today().strftime('%Y%B%d@%H_%M_%S')}-reportdata.json")
     #dict to store file counts for final reporting
     fileCounts = {}
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
          rootFiles = listFilesInFolder(service, settings["app"]["sourceFolderID"],loggingLevel=settings["app"]["loggingLevel"])
          if rootFiles != None:
               writeLog("found the following data at the root of src","debug",True,settings["app"]["loggingLevel"])
               writeLog(rootFiles,"debug",True,settings["app"]["loggingLevel"])
               writeLog(f"there are {len(rootFiles)} files in the source root","success",True,settings["app"]["loggingLevel"])
               fileCounts.setdefault(f"Source Root", []).append(len(rootFiles))
               #2 - count files and folders in src recursively
               writeLog("starting to count files in source recursively","info",True,settings["app"]["loggingLevel"])
               recurseFiles = []
               #loop through each of these top level folders and recurse so we dont pull them again
               for item in rootFiles:
                    results = listFilesInFolderRecursive(service, item["id"],loggingLevel=settings["app"]["loggingLevel"]) 
                    recurseFiles.append(results)
                    if results != None:
                         unwrappedrecurseFiles = unwrapRecurseLookupResults(results)
                         unwrappedrecurseFilesCount = len(unwrappedrecurseFiles)
                    else:
                         unwrappedrecurseFilesCount = 0 #just itself, the empty folder
                    writeLog(f"there are {len(unwrappedrecurseFiles)} files in the folder {item['name']} [{item['id']}]","success",True,settings["app"]["loggingLevel"])
                    fileCounts.setdefault((item["name"]+":"+item["id"]), []).append(unwrappedrecurseFilesCount)
               writeLog("found the following data recursing through the subfolders","debug",True,settings["app"]["loggingLevel"])
               writeLog(recurseFiles,"debug",True,settings["app"]["loggingLevel"])
               unwrappedrecurseFiles = unwrapRecurseLookupResults(recurseFiles)
               writeLog("found the following data unwrapping the recursive lookup data","debug",True,settings["app"]["loggingLevel"])
               writeLog(unwrappedrecurseFiles,"debug",True,settings["app"]["loggingLevel"])
               writeLog(f"there are {len(unwrappedrecurseFiles)+len(rootFiles)} files in the source root recursively","success",True,settings["app"]["loggingLevel"])
               #3 - copy all the content from src to dest
               writeLog("starting to copy all files from source to destination","info",True,settings["app"]["loggingLevel"])
               if settings["app"]["clearDestOnRun"]:
                    writeLog("clearing destination folder - set [clearDestOnRun] to [false] in settings.json to prevent this","warning",True,settings["app"]["loggingLevel"])
                    clearFolder(service, settings["app"]["destinationFolderID"],settings["app"]["loggingLevel"])
               numCopied = copyFolder(service, settings["app"]["sourceFolderID"], settings["app"]["destinationFolderID"],settings["app"]["loggingLevel"])
               writeLog(f"finished copying all [{numCopied}] files from source to destination","info",True,settings["app"]["loggingLevel"])
               #Final - reporting
               finalReport = finalReporting(fileCounts,bufferSize=100)
               writeLog("\n"+finalReport,"always",True,settings["app"]["loggingLevel"])
               #write the textual report for email/sending in some way for human consumption
               with open(finalOutputPath,"w") as reportFile:
                    reportFile.write(finalReport)
               uploadFile(service,settings["app"]["destinationFolderID"],finalOutputPath,f"{datetime.datetime.today().strftime('%Y%B%d@%H_%M_%S')}-report.txt",settings["app"]["loggingLevel"])
               #write the counts to a json for further parsing in what would be an assumed consumer of this application
               with open(finalJSONPath,"w") as reportFile:
                    reportFile.write(json.dumps(fileCounts))
               uploadFile(service,settings["app"]["destinationFolderID"],finalJSONPath,f"{datetime.datetime.today().strftime('%Y%B%d@%H_%M_%S')}-report.json",settings["app"]["loggingLevel"])
               #write the counts to a json for further parsing in what would be an assumed consumer of this application
               with open(finalDATAPath,"w") as reportFile:
                    reportFile.write(json.dumps(unwrappedrecurseFiles))
               uploadFile(service,settings["app"]["destinationFolderID"],finalJSONPath,f"{datetime.datetime.today().strftime('%Y%B%d@%H_%M_%S')}-reportdata.json",settings["app"]["loggingLevel"])
          else:
               writeLog(f"failed to get files in source","warning",True,settings["app"]["loggingLevel"])
     except HttpError as error:
          httpErrorHandler(error,settings["app"]["loggingLevel"])
 
#now that we have all the components workng in main(), let's regear to focus on a menu for individual runs by the assessor

def main2():
     #prep for nice console output
     os.system('color')
     #dynamic path caching
     scriptdir = os.path.dirname(os.path.realpath(__file__))
     tokenPath = os.path.join(scriptdir,"data","token.json")
     clientSecertsPath = os.path.join(scriptdir,"local","credentials.json")
     finalOutputPath = os.path.join(scriptdir,"data",f"{datetime.datetime.today().strftime('%Y%B%d@%H_%M_%S')}-report.txt")
     finalJSONPath = os.path.join(scriptdir,"data",f"{datetime.datetime.today().strftime('%Y%B%d@%H_%M_%S')}-report.json")
     finalDATAPath = os.path.join(scriptdir,"data",f"{datetime.datetime.today().strftime('%Y%B%d@%H_%M_%S')}-reportdata.json")
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
     try:
          service = build("drive", "v3", credentials=creds)
     except HttpError as error:
          httpErrorHandler(error,settings["app"]["loggingLevel"])

     menu = "1.  generate a report that shows the number of files and folders in total at the root of the source folder\n2. Generate a report that shows the number of child objects (recursively)\n3. Copy the content (nested files/folders) of the source folder to the destination folder\n4. Run the full assessment\n0. Quit\n\nPlease select an option to run"
     userInput = -1
     while userInput != "0":
          userInput = input(menu)
          match userInput:
               case "1":
                    #1 - count files and folders in root of src
                    fileCounts = {}
                    writeLog("starting to count files in source root","info",True,settings["app"]["loggingLevel"])
                    rootFiles = listFilesInFolder(service, settings["app"]["sourceFolderID"],loggingLevel=settings["app"]["loggingLevel"])
                    if rootFiles != None:
                         writeLog("found the following data at the root of src","debug",True,settings["app"]["loggingLevel"])
                         writeLog(rootFiles,"debug",True,settings["app"]["loggingLevel"])
                         writeLog(f"there are {len(rootFiles)} files in the source root","success",True,settings["app"]["loggingLevel"])
                         fileCounts.setdefault("Source Root", []).append(len(rootFiles))
                         #Final - reporting
                         finalReport = finalReporting(fileCounts,bufferSize=100)
                         printTitleCard()
                         writeLog("\n"+finalReport,"always",True,settings["app"]["loggingLevel"])
                         #write the textual report for email/sending in some way for human consumption
                         with open(finalOutputPath,"w") as reportFile:
                              reportFile.write(finalReport)
                         uploadFile(service,settings["app"]["destinationFolderID"],finalOutputPath,f"{datetime.datetime.today().strftime('%Y%B%d@%H_%M_%S')}-rootReport.txt",settings["app"]["loggingLevel"])
                         #write the counts to a json for further parsing in what would be an assumed consumer of this application
                         with open(finalJSONPath,"w") as reportFile:
                              reportFile.write(json.dumps(fileCounts))
                         uploadFile(service,settings["app"]["destinationFolderID"],finalJSONPath,f"{datetime.datetime.today().strftime('%Y%B%d@%H_%M_%S')}-report.json",settings["app"]["loggingLevel"])
                    else:
                         writeLog(f"failed to get files in source","warning",True,settings["app"]["loggingLevel"])
               case "2":
                    fileCounts = {}
                    rootFiles = listFilesInFolder(service, settings["app"]["sourceFolderID"],loggingLevel=settings["app"]["loggingLevel"])
                    if rootFiles != None:
                         writeLog("found the following data at the root of src","debug",True,settings["app"]["loggingLevel"])
                         writeLog(rootFiles,"debug",True,settings["app"]["loggingLevel"])
                         writeLog(f"there are {len(rootFiles)} files in the source root","success",True,settings["app"]["loggingLevel"])
                         fileCounts.setdefault("Source Root", []).append(len(rootFiles))
                         #2 - count files and folders in src recursively
                         writeLog("starting to count files in source recursively","info",True,settings["app"]["loggingLevel"])
                         recurseFiles = []
                         #loop through each of these top level folders and recurse so we dont pull them again
                         for item in rootFiles:
                              results = listFilesInFolderRecursive(service, item["id"],loggingLevel=settings["app"]["loggingLevel"]) 
                              recurseFiles.append(results)
                              if results != None:
                                   unwrappedrecurseFiles = unwrapRecurseLookupResults(results)
                                   unwrappedrecurseFilesCount = len(unwrappedrecurseFiles)
                              else:
                                   unwrappedrecurseFilesCount = 0 #just itself, the empty folder
                              writeLog(f"there are {len(unwrappedrecurseFiles)} files in the folder {item['name']} [{item['id']}]","success",True,settings["app"]["loggingLevel"])
                              fileCounts.setdefault(item["name"], []).append(unwrappedrecurseFilesCount)
                         writeLog("found the following data recursing through the subfolders","debug",True,settings["app"]["loggingLevel"])
                         writeLog(recurseFiles,"debug",True,settings["app"]["loggingLevel"])
                         unwrappedrecurseFiles = unwrapRecurseLookupResults(recurseFiles)
                         writeLog("found the following data unwrapping the recursive lookup data","debug",True,settings["app"]["loggingLevel"])
                         writeLog(unwrappedrecurseFiles,"debug",True,settings["app"]["loggingLevel"])
                         writeLog(f"there are {len(unwrappedrecurseFiles)+len(rootFiles)} files in the source root recursively","success",True,settings["app"]["loggingLevel"])
                         #Final - reporting
                         finalReport = finalReporting(fileCounts)
                         printTitleCard()
                         writeLog("\n"+finalReport,"always",True,settings["app"]["loggingLevel"])
                         #write the textual report for email/sending in some way for human consumption
                         with open(finalOutputPath,"w") as reportFile:
                              reportFile.write(finalReport)
                         uploadFile(service,settings["app"]["destinationFolderID"],finalOutputPath,f"{datetime.datetime.today().strftime('%Y%B%d@%H_%M_%S')}-recursiveReport.txt",settings["app"]["loggingLevel"])
                         #write the counts to a json for further parsing in what would be an assumed consumer of this application
                         with open(finalJSONPath,"w") as reportFile:
                              reportFile.write(json.dumps(fileCounts))
                         uploadFile(service,settings["app"]["destinationFolderID"],finalJSONPath,f"{datetime.datetime.today().strftime('%Y%B%d@%H_%M_%S')}-report.json",settings["app"]["loggingLevel"])
                         #write the counts to a json for further parsing in what would be an assumed consumer of this application
                         with open(finalDATAPath,"w") as reportFile:
                              reportFile.write(json.dumps(unwrappedrecurseFiles))
                         uploadFile(service,settings["app"]["destinationFolderID"],finalJSONPath,f"{datetime.datetime.today().strftime('%Y%B%d@%H_%M_%S')}-reportdata.json",settings["app"]["loggingLevel"])
                    else:
                         writeLog(f"failed to get files in source","warning",True,settings["app"]["loggingLevel"])
               case "3":
                    #3 - copy all the content from src to dest
                    writeLog("starting to copy all files from source to destination","info",True,settings["app"]["loggingLevel"])
                    if settings["app"]["clearDestOnRun"]:
                         writeLog("clearing destination folder - set [clearDestOnRun] to [false] in settings.json to prevent this","warning",True,settings["app"]["loggingLevel"])
                         clearFolder(service, settings["app"]["destinationFolderID"],settings["app"]["loggingLevel"])
                    copyFolder(service, settings["app"]["sourceFolderID"], settings["app"]["destinationFolderID"],settings["app"]["loggingLevel"])
                    writeLog("finished copying all files from source to destination","info",True,settings["app"]["loggingLevel"])
               case "4":
                    main()
               case "0":
                    writeLog("quitting","info",True,settings["app"]["loggingLevel"])
               case _:
                    writeLog("invalid selection, please try again","warning",True,settings["app"]["loggingLevel"])          

if __name__ == "__main__":
     main()
     #main2()