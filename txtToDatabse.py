import datetime
import glob
import os
from transfer import insert, retireveBlanks

def lineParser(line, message, state):
  space = 0
  comma = False
  if state == "new":
    for char in line:
      tempStr = "" 
      if not char == "," and not comma:
        tempStr += char
      else: comma = True

      if char.isspace():
        space += 1
      if space > 4:
        message += char
  
  else:
    for char in line: message += char
      
  return message

def configureDirectories():
  search_dir = "Photos/"
  files = filter(os.path.isfile, glob.glob(search_dir + "*"))
  files.sort(key=lambda x: os.path.getmtime(x))
  
  #for i, j in enumerate(files):
  #  ext = re.search ("(?:\.)(.*)", j)
  #  os.rename(j, i+ext)

def commitToDatabase(messages, sendIds, sourceIDs, times)

if __name__ == '__main__':
  messages, sendIds, times = ([],)*3
  
  configureDirectories()
  with open('backup.txt', 'r') as backupFile:
    for i, line in enumerate(backupFile):
      finish = false
      if "Fedex Master" in line:
        sendIDs.append(<id>)
      else: sendIDs.append(<other id>)
      
      checkMedia()
     
      message = lineParser(line, "", "new")

    if backupFile[i+1][0].isdigit()
      day,month,year = backupfile[i+1][0:10].split('.')
      while not finish:
        try:
          time = datetime(int(year),int(month),int(day).total_seconds() - datetime(1970,1,1)).total_seconds()
          times.append(time)
        except ValueError:
          message+=""
          lineParser(line, message, "continuation")
        else: 
          messages.append(message)
          finish = true
          
  backupFile.close()
  
  rows = []
  for i in range(times.length()-1):
    blankIDs = retrieveBlanks()
    record = (blankID[i], blankID[i], "message", "dialog", source_id, sendIDs[i], null, messages[i], 
              times[i], 1, media_type, media_file, media_size, null, null, null, 53)
    rows.append(record)
  
  imsert("database.sqlite", rows)
  
