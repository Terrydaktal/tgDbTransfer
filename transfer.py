import sqlite3

def extract (aymanDatabase):
    with conn:
        conn = create_connection(aymanDatabase)
        c = conn.cursor()
        c.execute('SELECT * FROM messages WHERE sourceID="<our chat>"')
        rows = c.fetchall()
        rows = rows[:137000]
        conn.close()
    return rows
        
        
def insert (lewisDatabase, rows):
    with conn:
        conn = create_connection(lewisDatabase)
        c = conn.cursor()
        c.execute('SELECT * FROM messages WHERE text=null')
        blanks = c.fetchall()
        blankIDs = [blanks[j][0] for j in blanks if blanks[j][<message row number>] == null]
        for i in range (rows.length()-1):
            lst = list(rows[i])
            lst[0] = blankIDs[i]
            rows[i] = tuple(lst)
            
        for i in range (rows.length()-1): c.executemany("INSERT INTO messages('id', 'message_id', 'message_type',\
                  'source_type', 'source_id', 'sender_id', 'fwd_from_id', 'text', 'time', 'has_media', 'media_type',\
                  'media_file', 'media_size', 'media_json', 'marlup_json', 'data', 'api_layer') VALUES({0}, {1}, {2},\
                  {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}".format(rows[i][0],
                    rows[i][1], rows[i][2], rows[i][3], rows[i][4], rows[i][5], rows[i][6], rows[i][7], rows[i][8]
                    rows[i][9], rows[i][10], rows[i][11], rows[i][12], rows[i][13], rows[i][14], rows[i][15], rows[i][16]))
        conn.commit()
        conn.close()
        
if __name__ == '__main__':
    messages = aymans_messages - my_messages
    lewisDatabase = sqlite.connect('<file>.sqlite')
    aymanDatabase = sqlite.connect('<file>.sqlite')
    rows = extract(aymanDatabase)
    insert(lewisDatabase, rows)
