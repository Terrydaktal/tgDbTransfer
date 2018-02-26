import datetime

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
    
if __name__ == '__main__':
  messages, sendIds, sourceIDs, times = ([],)*4
  
  with open('backup.txt', 'r') as backupFile:
    for i, line in enumerate(backupFile):
      finish = false
      sourceIDs.append(<chat id>)
      if "Fedex Master" in line:
        sendIDs.append(<id>)
      else: sendIDs.append(<other id>)
     
      message = lineParser(line, "", "new")

    if backupFile[i+1][0].isdigit()
      day,month,year = backupfile[i+1][0:10].split('.')
      while not finish:
        try:
          datetime.datetime(int(year),int(month),int(day))
          time = datetime(int(year),int(month),int(day).total_seconds() - datetime(1970,1,1)).total_seconds()
          times.append(time)
        except ValueError:
          message+=""
          lineParser(line, message, "continuation")
        else: 
          messages.append(message)
          finish = true
          
  backupFile.close()
