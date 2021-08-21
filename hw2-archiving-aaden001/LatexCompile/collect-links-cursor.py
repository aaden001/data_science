# collect-links-cursor.py
# MCW - 2/11/2021
import sys
import tweepy
import requests # for  requesting the url
from urllib.parse import urlparse # for requesting parse
import time #for time pauses to avoid max retries exceeded

def resovle_url(base_url,count):
    #print("\nProcess:    " +base_url +"\n")
    value =0
    url=""
    try:
        #request the link gotten set time out 2.5 seconds
        # This was actually useful to ensure that linked 
        #gotten would not take to much time during redirection
        request = requests.head(base_url,allow_redirects=True,timeout=2.5)
        
        #Ensure a 200 responds 
        if (request.status_code == 200):
            url  = request.url
            value =1
            #Gets the domain of the URI
            domain = urlparse(request.url).netloc
            #Ensures its not a twitter domain
            if domain.find("twitter.com") ==-1:
                url  = request.url
                value =1
                print("{} {}    :      {}".format( count,base_url,request.url))
                print("\n")
            else:
                #Reduce the counter because link wasnt resolved bc it a twitter domain
                count = count -1   
        else:
            #Reduce the counter because link wasnt resolved
            count = count -1
        request.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        pass
        #print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        #Reduce the counter because link wasnt resolved due to errors
        #from the link given
        count = count -1
        #print(f'Other error occurred: {err}')    
    return  count,value, url

# use coronavirus as default search term unless one provided
search_term = "coronavirus"
if len(sys.argv) > 1:
     search_term = str(sys.argv[1])

# number of links to collect
MAX_COUNT = 1000
count = 1
url =""
value =0
start = 1
blank_dict ={}

# OAuth2 procedure
consumer_key = "pnUItdX31QmYpHBFlVcYbocKQ"      # INSERT YOUR KEY HERE
consumer_secret = "gFNX2iztwhfL1tROFCX3UomwRbU8GjUJhHzLQat8DGxvBcyVmw"   # INSERT YOUR KEY HERE
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

try:
  for page in tweepy.Cursor(api.search, q=search_term, tweet_mode='extended', lang='en').pages():
    for tweet in page:
         for link in tweet.entities["urls"]:
             #resolve a the link gotten from twitter
             count,value, url = resovle_url(link['expanded_url'],count)
             if value != 0 :
                 if(blank_dict.get(url) != None):
                    #reduce count value if link could not be resolved
                    count = count - 1
                 else:
                    #print(count)
                    #print(url)
                    #store link and Ensures distinct url
                    blank_dict[url] = count
             count = count + 1 
             time.sleep(15)
    if count > MAX_COUNT:
        #print("\n\n") 
        #print(len(blank_dict))
        for x in range(0,len(blank_dict)-MAX_COUNT):
            #Remove excess link added only 1000 distinct links needed
            blank_dict.popitem()
        #used for debugging and print to console to see result values
        #[print(key,':',value) for key,value in blank_dict.items()]
        #print("\n\n")

        # swap values with keys
        blank_dict = {value:key for key, value in blank_dict.items()}
        
        #store result to a txt file called dict  in folder Q1       
        myfile = "Q1/dict.txt"
        with open(myfile, 'w') as f: 
            for key, value in blank_dict.items(): 
                f.write('%s\n' % (value)) 
        
        break
except tweepy.TweepError as e:
  print ("Tweepy Error: %s" % str(e))
