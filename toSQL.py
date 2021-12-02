import json
import datetime
import mysql.connector
import os
import re
import sys


# function creates the connection to mysql and returns the connection variable cnx
# and the cursor variable used access the database.
def connectToMySQL():
    cnx = mysql.connector.connect(password='project', user='project')
    cursor = cnx.cursor()
    return cursor, cnx


# function creates the menagerie database passed as the parameter DB_NAME
def createDatabase(cursor, DB_NAME):
    # Creates the database at cursor with the given name.
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


def createTables(cursor):
    # Reads the sql create tables statements and creates the tables
    with open('tables.sql', 'r') as f:
        for line in f:
            sql = line
            sql.strip()  # remove the \n
            cursor.execute(sql)


# Converts the unix time from the createTime attribute
def unix_time_to_datetime(unix_time):
    # uses the datetime library to convert unix time to datetime standard
    # ex. 1634694923 -> ['2021-10-19', '21:55:23']
    return datetime.datetime.fromtimestamp(unix_time).isoformat().split('T')


# https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b
def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


# checks if the musicID is empty, if it is then it returns 0 for the musicID
def musicIDNotEmpty(musicID):
    if musicID == '':
        return '0'
    else:
        return musicID


# converts the boolean values to either 1 or 0
def boolToBit(bool):
    if bool:
        return 'TRUE'
    else:
        return 'FALSE'


def insertData(cursor, input_file , ids):
    # sets the make sure there's no duplicate primary keys in the tables
    authors = set()
    sounds = set()
    # open the json and extract the data
    with open(input_file) as f:
        data = json.load(f)
        for tiktok in data:
            # checks to see if the tiktok is already in the ids set (i.e. the tiktok is already in the csv)
            if tiktok['id'] not in ids:
                # inserts the data into the TikTok table
                input = ''
                input += '"' + tiktok['id'] + '", "' + tiktok['authorMeta']['id'] + '", "' + \
                            musicIDNotEmpty(tiktok['musicMeta']['musicId']) + '", "' + str(unix_time_to_datetime(tiktok['createTime'])[0]) + \
                            '", "' + str(unix_time_to_datetime(tiktok['createTime'])[1]) + '", "' + \
                            remove_emoji(tiktok['text']).replace('\"', "'") + '", "' + str(tiktok['videoMeta']['duration']) + '"'
                sql = 'INSERT INTO TikTok VALUES (' + input + ');'
                cursor.execute(sql)

                # insert the data into the author table
                # uses the authors set to get rid of duplicate authors
                if tiktok['authorMeta']['id'] not in authors:
                    input = ''
                    input += '"' + tiktok['authorMeta']['id'] + '", "' + tiktok['authorMeta']['name'] + '", ' + \
                                str(tiktok['authorMeta']['verified']) + ', "' + \
                                remove_emoji(tiktok['authorMeta']['signature'].replace('\n', ' ')).replace('\"',"'") + \
                                '", "' + str(tiktok['authorMeta']['fans']) + '"'
                    sql = 'INSERT INTO Author VALUES (' + input + ');'
                    cursor.execute(sql)
                    authors.add(tiktok['authorMeta']['id'])

                # insert the data into the music table
                # some of the sounds don't have musicAlbum or musicAuthor
                try:
                    # uses the sounds set to get rid of duplicates
                    if tiktok['musicMeta']['musicId'] not in sounds:
                        input = ''
                        input += '"' + tiktok['musicMeta']['musicId'] + '", "' + \
                                 remove_emoji(tiktok['musicMeta']['musicName']).replace('\"',"'") + \
                                 '", "' + remove_emoji(tiktok['musicMeta']['musicAuthor']).replace('\"',"'") + \
                                 '", ' + str(tiktok['musicMeta']['musicOriginal']) + \
                                 ', "' + remove_emoji(tiktok['musicMeta']['musicAlbum']).replace('\"',"'") + '"'
                        sql = 'INSERT INTO Music VALUES (' + input + ');'
                        cursor.execute(sql)
                        sounds.add(tiktok['musicMeta']['musicId'])
                except KeyError:
                    pass

                # insert data into the tiktok stats data
                # the primary key is tiktokID so there's already duplication validation
                input = ''
                input += '"' + tiktok['id'] + '", "' + str(tiktok['diggCount']) + '", "' + \
                         str(tiktok['shareCount']) + '", "' + str(tiktok['playCount']) + '", "' + \
                         str(tiktok['commentCount']) + '"'
                sql = 'INSERT INTO Tiktok_Stats VALUES (' + input + ');'
                cursor.execute(sql)



            ids.add(tiktok['id'])



def go():
    DB_NAME = 'TikToks'
    cursor, connection = connectToMySQL()
    cursor.execute('DROP DATABASE IF EXISTS ' + DB_NAME + ';')  # drops the database before it is created
    createDatabase(cursor, DB_NAME)  # Creates the database
    cursor.execute("USE {}".format(DB_NAME))

    # set to make sure there's no duplicate ids
    ids = set()
    # # walks through all the files in the TikToks directory and extracts all the data
    # for root, dirs, files in os.walk('TikToks'):
    #     for name in files:
    #         insertData(cursor, os.path.join(root, name), ids)
    createTables(cursor)
    insertData(cursor, 'tiktoks10000.json', ids)

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == '__main__':
    go()