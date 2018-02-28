import time
import glob
import os
from datetime import datetime
from transfer import insert, retrieveBlanks
firstline = True

def lineParser(line, message, state):
  space = 0
  comma = False
  global firstline

  if firstline:
    times.append(1431905243)
    firstline = False
    
  if state == "new":
    for char in line:

      if space >= 4:
          message += char

      else:
        if char.isspace(): space += 1
  
  else:
    for char in line: message += char
      
  return message

def configureDirectories():
  directories = ["Photos\\", "Videos\\", "Audios\\", "Documents\\"]
  allFiles = []
  for i in directories:
    tmpFiles = filter(os.path.isfile, glob.glob(i + "*"))
    files = [i for i in tmpFiles]
    files.sort(key=lambda x: os.path.getmtime(x))
    files = [i.split('\\')[1] for i in reversed(files)]
    allFiles.append(files)
                
  return allFiles
  
  #for i, j in enumerate(files):
  #  ext = re.search ("(?:\.)(.*)", j)
  #  os.rename(j, i+ext)

def checkMedia(line, voice, photo, video, document, allFiles, mediaFiles):  
  if "[[Photo" in line:
    line = line.replace("[[Photo]]", "")
    mediaFiles.append(allFiles[0][photo])
    photo+=1
  elif "[[Video" in line:
    mediaFiles.append(allFiles[1][video])
    video+=1
  elif "[[Voice Message" in line:
    mediaFiles.append(allFiles[2][voice])
    voice+=1
  elif "[[Document" in line:
    mediaFiles.append(allFiles[3][document])
    document+=1
  else:
    mediaFiles.append(None)
  return line, voice, photo, video, document, allFiles, mediaFiles
                 
if __name__ == '__main__':
  print("configuring...")
  messages, sendIDs, times, mediaFiles = [], [], [], []
  voice, photo, video = 0, 0, 0

  print("configuring directories...")
  allFiles = configureDirectories()
  
  print("extracting backup...")               
  with open('backup.txt', 'r', encoding="utf8") as backupFile:
    offset = 0
    lines = backupFile.readlines()
    for i in range(len(lines) - 1):
      finish = False

      try:
        if "Fedex Master" in lines[i+offset]:
          sendIDs.append(54129829)
        else: sendIDs.append(67106936)
      except Exception: break
     
      message = lineParser(lines[i+offset], "", "new")
      
      j=0
      
      if i + offset < len(lines) - 1:
        while not finish:
          j+=1
          try:
            lines[i+j+offset][0].isdigit()
            day, month, year = lines[i+j+offset][0:10].split(".")
            hours, mins, seconds = lines[i+j+offset][11:19].split(":")
            t = datetime(int(year),int(month),int(day),int(hours),int(mins),int(seconds))
            unixtime = time.mktime(t.timetuple())
            times.append(unixtime)
          except Exception:
            message+= " "
            message = lineParser(lines[i+j+offset], message, "continuation")
          else:
            message, voice, photo, video, allFiles, mediaFiles = checkMedia(message, voice, photo, video, allFiles, mediaFiles)
            finish = True
            messages.append(message)
      else:
        message, voice, photo, video, document, allFiles, mediaFiles = checkMedia(message, voice, photo, video, document, allFiles, mediaFiles)
        messages.append(message)

      offset += j - 1
      
  backupFile.close()

  print("building database...")   
  rows = []
  blankIDPairs = retrieveBlanks("database.sqlite")

  for i in range(len(times) - 1):
    if ".png" in str(mediaFiles[i]) or ".jpg" in str(mediaFiles[i]): media_type =  "photo"
    elif mediaFiles[i] != None: media_type = "document"
    else: media_type = None
    
    record = (blankIDPairs[0][i], i, "message", "dialog", "54129829", sendIDs[i], None, messages[i], 
              times[i], 1, media_type, mediaFiles[i], None, None, None, None, 53)
    rows.append(record)

    i+= 1
    
  print("commiting changes...")   
  insert("database.sqlite", rows)
  print("done!")

  #select * from messages where source_id = "54129829"
