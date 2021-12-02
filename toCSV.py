import json
import os
import datetime


# Converts the unix time from the createTime attribute
def unix_time_to_datetime(unix_time):
    # uses the datetime library to convert unix time to datetime standard
    # ex. 1634694923 -> '2021-10-19 21:55:23'
    return datetime.datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')


# extracts the tiktok data and inserts it into the csv cleanly
def extract_data_into_csv(input_filename, output_filename, ids):
    # opens the csv file in append mode
    write_file = open(output_filename, 'a')
    # open the json file and extract the necessary values
    with open(input_filename) as f:
        data = json.load(f)
        for tiktok in data:
            # checks to see if the tiktok is already in the ids set (i.e. the tiktok is already in the csv)
            if tiktok['id'] not in ids:
                # there is no musicAuthor or musicAlbum attribute so I call an exception for those with missing attributes
                try:
                    write_file.write(str(tiktok['id']) + ',' + str(tiktok['text']) + ',' +
                        # calls the unix_time_to_datetime function to convert the createTime attribute to datetime and split the result
                        unix_time_to_datetime(tiktok['createTime']) + ',' + str(tiktok['authorMeta']['id']) + ',' +
                        tiktok['authorMeta']['name'] + ',' + str(tiktok['authorMeta']['verified']) + ',' +
                        tiktok['authorMeta']['signature'].replace('\n', ' ') + ',' +
                        str(tiktok['authorMeta']['fans']) + ',' + str(tiktok['musicMeta']['musicId']) + ',' +
                        tiktok['musicMeta']['musicName'] + ',' + tiktok['musicMeta']['musicAuthor'] + ',' +
                        str(tiktok['musicMeta']['musicOriginal']) + ',' + tiktok['musicMeta']['musicAlbum'] + ',' +
                        str(tiktok['videoMeta']['duration']) + ',' + str(tiktok['diggCount']) + ',' +
                        str(tiktok['shareCount']) + ',' + str(tiktok['playCount']) + ',' + str(tiktok['commentCount']) + '\n')
                    ids.add(tiktok['id'])
                except:
                    pass
    f.close()
    write_file.close()


def go():
    # a set of all the ids in the csv so there's no duplicates
    ids = set()
    output_filename = 'tiktoks.csv'
    # opens the csv file in append mode
    write_file = open(output_filename, 'w')
    # establishes the first line in the csv as the column names (changes the createTime column to date and time)
    write_file.write('id,text,createTime,authorId,authorName,verified,signature,fans,musicId,musicName,'
                     'musicAuthor,musicOriginal,musicAlbum,videoMetaDuration,diggCount,shareCount,playCount,'
                     'commentCount\n')
    write_file.close()
    # walks through all the files in the TikToks directory and extracts all the data
    for root, dirs, files in os.walk('TikToks'):
        for name in files:
            extract_data_into_csv(os.path.join(root, name), output_filename, ids)


if __name__ == '__main__':
    go()