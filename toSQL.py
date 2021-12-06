import json
import datetime
import mysql.connector
import os
import re
import sys


# function creates the connection to mysql and returns the connection variable cnx
# and the cursor variable used access the database.
def connect_to_my_SQL():
    cnx = mysql.connector.connect(password='project', user='project')
    cursor = cnx.cursor()
    return cursor, cnx


# function creates the menagerie database passed as the parameter DB_NAME
def create_database(cursor, DB_NAME):
    # Creates the database at cursor with the given name.
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


def create_tables(cursor):
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
# removes all special character in the strings so that the data is formatted for sql
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
def music_id_not_empty(musicID):
    if musicID == '':
        return '0'
    else:
        return musicID


# for the all the string errors that could occur tiktok_str_replace fixes them
def tiktok_str_replace(str):
    # remove_emoji removes all the emojis and special characters
    # removes the \n so there is no new lines in the print statements
    # removes the double quotes and makes them single quotes so the SQL with have single quotes in the table
    # I used single quotes instead of double because ' can be used in other ways (ex. don't)
    # replaces the \\ which is printed as \ to \\\\ which will have a \\ in the sql statement (ex. ':/\' -> ':/\\')
    return remove_emoji(str.replace('\n', ' ').replace('\"', "'").replace('\\', '\\\\'))


# inserts the data into the TikTok table
def tiktok_table(tiktok, cursor):
    values = '"' + tiktok['id'] + '", "' + tiktok['authorMeta']['id'] + '", "' + \
             music_id_not_empty(tiktok['musicMeta']['musicId']) + '", "' + \
             str(unix_time_to_datetime(tiktok['createTime'])[0]) + \
             '", "' + str(unix_time_to_datetime(tiktok['createTime'])[1]) + '", "' + \
             tiktok_str_replace(tiktok['text']) + '", "' + str(tiktok['videoMeta']['duration']) + '", "' + \
             str(tiktok['videoUrl']) + '"'
    sql = 'INSERT INTO TikTok VALUES (' + values + ');'
    cursor.execute(sql)


# inserts the data into the author table
def author_table(tiktok, authors, cursor, f):
    if tiktok['authorMeta']['id'] not in authors:
        # replaces all the errors that could occur
        values = '"' + tiktok['authorMeta']['id'] + '", "' + remove_emoji(tiktok['authorMeta']['name']) + '", ' + \
                 str(tiktok['authorMeta']['verified']) + ', "' + \
                 tiktok_str_replace(tiktok['authorMeta']['signature']) + \
                 '", "' + str(tiktok['authorMeta']['fans']) + '"'
        sql = 'INSERT INTO Author VALUES (' + values + ');'
        cursor.execute(sql)
        authors.add(tiktok['authorMeta']['id'])


# inserts the data into the music table
def music_table(tiktok, sounds, cursor):
    # uses the sounds set to get rid of duplicates
    if tiktok['musicMeta']['musicId'] not in sounds:
        values = '"' + tiktok['musicMeta']['musicId'] + '", "' + \
                tiktok_str_replace(tiktok['musicMeta']['musicName']) + \
                '", "' + tiktok_str_replace(tiktok['musicMeta']['musicAuthor']) + \
                '", ' + str(tiktok['musicMeta']['musicOriginal']) + \
                ', "' + tiktok_str_replace(tiktok['musicMeta']['musicAlbum']) + '"'
        sql = 'INSERT INTO Music VALUES (' + values + ');'
        cursor.execute(sql)
        sounds.add(tiktok['musicMeta']['musicId'])


# inserts the data into the tiktok_stats table
def tiktok_stats_table(tiktok, cursor):
    values = '"' + tiktok['id'] + '", "' + str(tiktok['diggCount']) + '", "' + \
             str(tiktok['shareCount']) + '", "' + str(tiktok['playCount']) + '", "' + \
             str(tiktok['commentCount']) + '"'
    sql = 'INSERT INTO Tiktok_Stats VALUES (' + values + ');'
    cursor.execute(sql)


# insert the data into the Hash_Tags data
def hashtag_table(tiktok, cursor):
    x = 0
    while x < len(tiktok['hashtags']):
        values = '"' + tiktok['id'] + '", "' + tiktok['hashtags'][x]['id'] + '", "' + \
                remove_emoji(tiktok['hashtags'][x]['name']) + '"'
        sql = 'INSERT INTO Hash_Tags VALUES (' + values + ');'
        cursor.execute(sql)
        x += 1


# inserts the data into the individual tables
def insert_data(cursor, input_file, ids, authors, sounds):
    # open the json and extract the data
    with open(input_file) as f:
        data = json.load(f)
        for tiktok in data:
            # checks to see if the tiktok is already in the ids set (i.e. the tiktok is already in the csv)
            if tiktok['id'] not in ids:
                try:
                    # inserts the data into the TikTok table
                    tiktok_table(tiktok, cursor)

                    # insert the data into the author table
                    # uses the authors set to get rid of duplicate authors
                    author_table(tiktok, authors, cursor, f)

                    # insert the data into the music table
                    music_table(tiktok, sounds, cursor)

                    # insert data into the tiktok stats data
                    # the primary key is tiktokID so there's already duplication validation
                    tiktok_stats_table(tiktok, cursor)

                    # insert the data into the Hash_Tags data
                    hashtag_table(tiktok, cursor)
                # keyError is for when one of the fields doesn't exist for a tiktok in the json
                except KeyError:
                    pass

            ids.add(tiktok['id'])


def go():
    DB_NAME = 'TikToks'
    cursor, connection = connect_to_my_SQL()
    cursor.execute('DROP DATABASE IF EXISTS ' + DB_NAME + ';')  # drops the database before it is created
    create_database(cursor, DB_NAME)  # Creates the database
    cursor.execute("USE {}".format(DB_NAME))

    # sets the make sure there's no duplicate primary keys in the tables
    ids = set()
    authors = set()
    sounds = set()
    create_tables(cursor)
    # walks through all the files in the TikToks directory and extracts all the data
    for root, dirs, files in os.walk('TikToks'):
        for name in files:
            insert_data(cursor, os.path.join(root, name), ids, authors, sounds)

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == '__main__':
    go()