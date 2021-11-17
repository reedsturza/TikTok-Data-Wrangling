import json
import datetime


# Converts the unix time from the createTime attribute
def unix_time_to_datetime(unix_time):
    # uses the datetime library to convert unix time to datetime standard, the splits the result
    # ex. 1634694923 -> ['2021-10-19', '21:55:23']
    return datetime.datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S').split(' ')


def extract_data_into_csv(input_filename, output_filename):
    # opens the csv file and writes the first line for the column names
    write_file = open(output_filename, 'w')
    write_file.write('id,text,date,time,authorId,authorName,verified,signature,fans,musicId,musicName,'
                     'musicAuthor,musicOriginal,musicAlbum,videoMetaDuration,diggCount,shareCount,playCount,'
                     'commentCount\n')
    # open the json file and extract the necessary values
    with open(input_filename) as f:
        data = json.load(f)
        for tiktok in data:
            # for id:7017249610901064965 there is no musicAuthor or musicAlbum attribute for some reason
            if "musicAuthor" not in tiktok['musicMeta'] and "musicAlbum" not in tiktok['musicMeta']:
                write_file.write(str(tiktok['id']) + ',' + str(tiktok['text']) + ',' +
                    # calls the unix_time_to_datetime function to convert the createTime attribute to datetime and split the result
                    unix_time_to_datetime(tiktok['createTime'])[0] + ',' + unix_time_to_datetime(tiktok['createTime'])[1] + ',' +
                    str(tiktok['authorMeta']['id']) + ',' + tiktok['authorMeta']['name'] + ',' +
                    str(tiktok['authorMeta']['verified']) + ',' + tiktok['authorMeta']['signature'].replace('\n', ' ') + ',' +
                    str(tiktok['authorMeta']['fans']) + ',' + str(tiktok['musicMeta']['musicId']) + ',' +
                    tiktok['musicMeta']['musicName'] + ',' + ',' + # replaces the musicAuthor with an empty string
                    str(tiktok['musicMeta']['musicOriginal']) + ',' + ',' + # replaces the musicAlbum with an empty string
                    str(tiktok['videoMeta']['duration']) + ',' + str(tiktok['diggCount']) + ',' +
                    str(tiktok['shareCount']) + ', ' + str(tiktok['playCount']) + ',' + str(tiktok['commentCount']) + '\n')
            else:
                write_file.write(str(tiktok['id']) + ',' + str(tiktok['text']) + ',' +
                    # calls the unix_time_to_datetime function to convert the createTime attribute to datetime and split the result
                    unix_time_to_datetime(tiktok['createTime'])[0] + ',' + unix_time_to_datetime(tiktok['createTime'])[1] + ',' +
                    str(tiktok['authorMeta']['id']) + ',' + tiktok['authorMeta']['name'] + ',' +
                    str(tiktok['authorMeta']['verified']) + ',' + tiktok['authorMeta']['signature'].replace('\n', ' ') + ',' +
                    str(tiktok['authorMeta']['fans']) + ',' + str(tiktok['musicMeta']['musicId']) + ',' +
                    tiktok['musicMeta']['musicName'] + ',' + tiktok['musicMeta']['musicAuthor'] + ',' +
                    str(tiktok['musicMeta']['musicOriginal']) + ',' + tiktok['musicMeta']['musicAlbum'] + ',' +
                    str(tiktok['videoMeta']['duration']) + ',' + str(tiktok['diggCount']) + ',' +
                    str(tiktok['shareCount']) + ',' + str(tiktok['playCount']) + ',' + str(tiktok['commentCount']) + '\n')


def go():
    input_filename = 'tiktoks10000.json'
    output_filename = 'tiktoks.csv'

    extract_data_into_csv(input_filename, output_filename)


if __name__ == '__main__':
    go()