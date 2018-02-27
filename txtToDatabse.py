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
  directories = ["Photos\\", "Videos\\", "Audios\\"]
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

def checkMedia(line, voice, photo, video, allFiles, mediaFiles):  
  if "[[Photo" in line:
    line.replace("[[Photo]]", allFiles[0][photo])
    mediaFiles.append(allFiles[0][photo])
    photo+=1
  elif "[[Video" in line:
    line.replace("[[Video]]", allFiles[1][video])
    mediaFiles.append(allFiles[1][video])
    video+=1
  elif "[[Voice Message" in line:
    line.replace("[[Voice Message]]", allFiles[2][voice])
    mediaFiles.append(allFiles[2][voice])
    voice+=1
  else:
    mediaFiles.append(None)
  return line, voice, photo, video, allFiles, mediaFiles
                 
if __name__ == '__main__':
  print("configuring...")
  messages, sendIDs, times, mediaFiles = [], [], [], []
  voice, photo, video = 0, 0, 0

  print("configuring directories...")
  allFiles = configureDirectories()
  
  print("extracting backup...")               
  with open('backup.txt', 'r', encoding="utf8") as backupFile:
    lines = backupFile.readlines()
    for i, line in enumerate(lines):
      finish = False
      if "Fedex Master" in line:
        sendIDs.append(54129829)
      else: sendIDs.append(67106936)
      
      line, voice, photo, video, allFiles, mediaFiles = checkMedia(line, voice, photo, video, allFiles, mediaFiles)
     
      message = lineParser(line, "", "new")
      
      if i < len(lines) - 1:
        j=0
        while not finish:
          j+=1
          try:
            lines[i+j][0].isdigit()
            day, month, year = lines[i+j][0:10].split(".")
            hours, mins, seconds = lines[i+j][11:19].split(":")
            t = datetime(int(year),int(month),int(day),int(hours),int(mins),int(seconds))
            unixtime = time.mktime(t.timetuple())
            times.append(unixtime)
          except Exception:
            message+= " "
            message = lineParser(line, message, "continuation")
          else:
            messages.append(message)
            finish = True

        else: messages.append(message)
          
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
