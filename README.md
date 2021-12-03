# TikTok-Wrangling
Tiktok scraper used for this project
https://github.com/drawrowfly/tiktok-scraper/blob/master/README.md

Run the tiktokDownload.py file in a terminal to download tiktoks continuously


## Data Wrangled From the TikTok Scraper
<table>
    <tr>
        <th>Variable Name</th>
        <th>Description</th>
        <th>Type</th>
    </tr>
    <tr>
        <td>Id</td>
        <td>the video id</td>																					
        <td>int</td>   
    </tr>
    <tr>
        <td>text</td>
        <td>the text the author attached to the tiktok</td>																					
        <td>string</td>   
    </tr>
    <tr>
        <td>createTime</td>
        <td>the time the user published the tiktok (convert the create time to a normal standard)</td>																					
        <td>int</td>   
    </tr>
    <tr>
        <td>authorId</td>
        <td>the id for the author (user who posted) of the tiktok</td>																					
        <td>int</td>   
    </tr>
    <tr>
        <td>authorName</td>
        <td>the authors username</td>																					
        <td>String</td>   
    </tr>
    <tr>
        <td>verified</td>
        <td>boolean for if the author is verified</td>																					
        <td>boolean</td>   
    </tr>
    <tr>
        <td>signature</td>
        <td>the bio of the author’s account</td>																					
        <td>String</td>   
    </tr>
    <tr>
        <td>fans</td>
        <td>the number of followers the author has</td>																					
        <td>int</td>   
    </tr>
    <tr>
        <td>musicId</td>
        <td>id for the music on the tiktok</td>																					
        <td>int</td>   
    </tr>
    <tr>
        <td>musicName</td>
        <td>the name for the music the author pick for the tiktok, isn’t always a song name	</td>																					
        <td>String</td>   
    </tr>
    <tr>
        <td>musicAuthor</td>
        <td>the creator of the music, author’s create music so the musicAuthor could be the author</td>																					
        <td>String</td>   
    </tr>
    <tr>
        <td>musicOriginal</td>
        <td>true if the an author made the music, false if an actual artist made the music</td>																					
        <td>boolean</td>   
    </tr>
    <tr>
        <td>musicAlbum</td>
        <td>the album the music is from iff musicOriginal is false</td>																					
        <td>String</td>   
    </tr>
    <tr>
        <td>videoMetaDuration</td>
        <td>the length of each tiktok</td>																					
        <td>int</td>   
    </tr>
    <tr>
        <td>diggCount</td>
        <td>number of people who “hearted” the video</td>																					
        <td>int</td>   
    </tr>
    <tr>
        <td>shareCount</td>
        <td>the number of people who have shared the tiktok to someone else</td>																					
        <td>int</td>   
    </tr>
    <tr>
        <td>playCount</td>
        <td>the number of views the tiktok has</td>																					
        <td>int</td>   
    </tr>
    <tr>
        <td>commentCount</td>
        <td>the number of comments the tiktok has, author can disable comments so this number could be 0</td>																					
        <td>int</td>   
    </tr>
    <tr>
        <td>hashtagsId</td>
        <td>the id for one of the hashtags use in the post</td>																					
        <td>int</td>   
    </tr>
    <tr>
        <td>hashtagsName</td>
        <td>the actual hashtag without the hash (ex. fyp not #fyp)</td>																					
        <td>String</td>   
    </tr>
</table>

## CSV
Headers of the CSV file
>id,text,createTime,authorId,authorName,verified,signature,fans,musicId,musicName,musicAuthor,musicOriginal,musicAlbum,videoMetaDuration,diggCount,shareCount,playCount,commentCount


# SQL
<table>
<caption>SQL Tables and their Fields</caption>
    <tr>
        <th>TikTok Table</th>
        <th>Author Table</th>
        <th>Music Table</th>
        <th>TikTok_Stats Table</th>
        <th>Hash_Tags Table</th>
    </tr>
    <tr>
        <td><u>tiktokID: key</u></td>
        <td><u>authorID: key</u></td>
        <td><u>musicID: key</u></td>
        <td><u>tiktokID: key</u></td>
        <td>tiktokID</td>
    </tr>
    <tr>
        <td>authorID</td>
        <td>authorName</td>
        <td>musicName</td>
        <td>diggCount</td>
        <td>hashTagID</td>
    </tr>
    <tr>
        <td>musicID</td>
        <td>verified</td>
        <td>musicAuthor</td>
        <td>shareCount</td>
        <td>name</td>
    </tr>
    <tr>
        <td>createTime</td>
        <td>signature</td>
        <td>musicOriginal</td>
        <td>playCount</td>
    </tr>
    <tr>
        <td>text</td>
        <td>fans</td>
        <td>musicAlbum</td>
        <td>commentCount</td>
    </tr>
    <tr>
        <td>videoMetaDuration</td>
    </tr>
</table>