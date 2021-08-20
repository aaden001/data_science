# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 19:14:41 2021

@author: adeni
"""
#!/usr/bin/python3
import sys  # access command line aruguements
from bs4 import BeautifulSoup # html/xml parser
import requests #requests
from requests.exceptions import HTTPError # for error handling
from urllib.parse import urljoin #construct full url path

listOfargv = sys.argv
def contentTypeRequest(value):
    try:
        req = requests.get(value)
        if req:
            # check link content type
            if( req.headers['Content-Type'] == "application/pdf"): 
                print("This is a pdf file \n")
                print("URI: {} \nFinal URL: {} \nContent Length: {}bytes \n\n" .format(value, req.url,req.headers['content-length']))
            else:
                print("Is Not a pdf File \n" )
        else:
            #displays status code error
            print("Request Failed Status code {}\nPlease Enter a valid webpage link \n" .format(req.status_code))
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
        
def prettyPrint(dictionary):
    i = 1
    for x in dictionary.keys():
        
        print("{}: {} ".format(i,x))
        contentTypeRequest(x)
        i = i+1
    
def getLinksFromWebsite(base_URL):

    try:
        # Get the request of the site
        response = requests.get(base_URL)
        blank_dict ={}
        if response:
            # removes bs4 warning
            soup = BeautifulSoup(response.text, "html.parser" )
            print("\nSite: {}" .format(base_URL) )
            # gets all a tags that has href values
            href_tags = soup.find_all('a',href=True)
            #indirect way to extract href
            for link in href_tags: 
                if (blank_dict.get(urljoin(base_URL, link.get('href')))) != None:
                    # avoid duplicates
                    pass 
                else:
                    #Store link 
                    blank_dict[urljoin(base_URL, link.get('href'))] =1
            #print dictionary
            prettyPrint(blank_dict)

        else:
            #displays status code error
            print("Request Failed Status code {}\nPlease Enter a valid webpage" .format(response.status_code)) 
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

if len(listOfargv) > 1:    
    for x in range(1,len(listOfargv)):  # Run multiple times
        getLinksFromWebsite(listOfargv[x])
        print("\n")
else:
    print("Pass in a link")