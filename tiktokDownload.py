import os
import time

while True:
	cmd = 'tiktok-scraper trend -n 0 --filepath /Users/sturzarmoravian.edu/DataWrangling/TikTok-Wrangling/TikToks -t json --session sid_tt=039fd5cd01d78ff9fa9e162871d951c3'
	os.system(cmd)
	time.sleep(600)

