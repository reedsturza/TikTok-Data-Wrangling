CREATE TABLE TikTok (tiktokID BIGINT PRIMARY KEY, authorID BIGINT, musicID BIGINT, createDate DATE, createTime TIME, text TEXT, videoDuration INT);
CREATE TABLE Author (authorID BIGINT PRIMARY KEY, authorName VARCHAR(100), verified BIT(1), signature VARCHAR(255), fans INT);
CREATE TABLE Music (musicID BIGINT PRIMARY KEY, musicName VARCHAR(100), musicAuthor VARCHAR(255), musicOriginal BIT(1), musicAlbum VARCHAR(255));
CREATE TABLE TikTok_Stats (tiktokID BIGINT PRIMARY KEY, diggCount INT, shareCount INT, playCount INT, commentCount INT);
CREATE TABLE HashTags (tiktokID BIGINT, hashTagID BIGINT,name VARCHAR(100));