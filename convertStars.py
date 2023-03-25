import praw
import requests

credentials = open("natz_secret.txt", "r")

cid = credentials.readline().strip()
csc = credentials.readline().strip()
usn = credentials.readline().strip()
pwd = credentials.readline().strip()

reddit = praw.Reddit(
    client_id = cid, 
    client_secret = csc, 
    user_agent = "/r/TakeaPlantLeaveaPlant Dev bot by /u/themurrlover",
    username = usn,
    password = pwd,
    )

try:
    print("Authenticated as {}".format(reddit.user.me()))
except:
    print("Something went wrong during authentication")
    quit()

# Set the sub to TakeaPlantLeaveaPlant
sub = reddit.subreddit("TakeaPlantLeaveaPlant")
page = sub.wiki['userdirectory/b'].content_md
page_contents = page.split("\n")
page_contents = page_contents[5:]   #skip user directory stuff
# print(page_contents)

conversion = open("convertedB.md", "w")
num_yes = 0
num_no = 0
shipping_qual = 0

for line in page_contents:
    if '##' in line and '###' not in line:
        if num_yes > 0 or num_no > 0:
            conversion.write("|" + str(num_yes) + "|" + str(num_no) + "|" + str(shipping_qual) + "|\n\n")
        num_yes = 0
        num_no = 0
        shipping_qual = 0
        conversion.write("## " + line[2:] + "\n\n")
        continue

    if '###' in line or '|:-|:-|:-|' in line:
        continue

    if '|Rating|Type|Comments|' in line:
        conversion.write("|Trade Yes|Trade No|Shipping Quality|Comments|\n")
        conversion.write("|:-|:-|:-|:-|\n")
        continue
    
    rating = 0
    rating_split = line.split('|')

    if len(rating_split) == 1:
        continue
    else:
        rating = rating_split[1]
    
    if float(rating) > 2:
        num_yes += 1
    else:
        num_no += 1

    
    
conversion.close()
    
