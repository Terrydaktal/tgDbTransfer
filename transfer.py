import sqlite3
import sys
import os.path
import shutil

def extract (friendDatabase, chatID, startMessageID, endMessageID):
    with conn:
        conn = sqlite3.connect(friendDatabase)
        c = conn.cursor()
        c.execute('SELECT * FROM messages WHERE sourceID="{0}"'.format(chatID))
        rows = c.fetchall()
        rows = rows[startMessageID:endMessageID-1]
        conn.close()
    return rows
        
def retrieveBlanks(homeDatabase):
    conn = sqlite3.connect(homeDatabase)
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM messages WHERE message_type = "empty_message"')
        blanks = c.fetchall()
        blankIDPairs = []
        blankIDPairs.append([blanks[j][0] for j in range(len(blanks) - 1)])
        blankIDPairs.append([blanks[j][1] for j in range(len(blanks) - 1)])
        
    conn.close()
    return blankIDPairs
    
def insert (homeDatabase, rows):
    conn = sqlite3.connect(homeDatabase)
    with conn:
        c = conn.cursor()
        blankIDPairs = retrieveBlanks(homeDatabase)
        
      #  for i in range (len(rows) - 1):
      #      lst = list(rows[i])
      #      lst[0] = blankIDs[i]
      #      rows[i] = tuple(lst)
            
        for i in range (len(rows) - 1):
            c.execute('''REPLACE INTO messages('id', 'message_id', 'message_type',
                                  'source_type', 'source_id', 'sender_id', 'fwd_from_id', 'text', 'time', 'has_media', 'media_type',
                                  'media_file', 'media_size', 'media_json', 'markup_json', 'data', 'api_layer')
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',\
                                  (rows[i][0], rows[i][1], rows[i][2], rows[i][3], rows[i][4], rows[i][5], rows[i][6], rows[i][7], rows[i][8],
                                   rows[i][9], rows[i][10], rows[i][11], rows[i][12], rows[i][13], rows[i][14], rows[i][15], rows[i][16]))
            
       # fileIDs = [rows[j][11] for j in range(len(rows) - 1)]
       # for i in fileIDs:
       #     if not os.path.exists(homeFileDirectory + i):
       #         shutil.copy(friendFileDirectory+i, homeFileDirectory+i)      

    conn.commit()        
    conn.close()
        
if __name__ == '__main__':
    try: 
        homeDB, friendDB, chatID, startMessageID, endMessageID = [i for j in sys.argv[1:]]
    except Exception as e: print(e)
        
    homeDatabase = sqlite.connect(homeDB) #'<file>.sqlite'
    friendDatabase = sqlite.connect(friendDB)
    rows = extract(friendDatabase, chatID, startMessageID, endMessageID)
    insert(homeDatabase, rows)
