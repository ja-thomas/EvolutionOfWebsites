# -*- coding: utf-8 -*-
import requests
import re
import json
from pymongo import MongoClient
from bs4 import BeautifulSoup, Comment
from analysis import analysePage

client = MongoClient('localhost', 27017)
# or client = MongoClient('mongodb://localhost:27017/')

# you connect to the database you created with "use mydb"
db = client['EvoDATABASE']

# you connect to the collection you created with "db.testData.insert("something)"
pagesHTML_collection = db['youtube']

#Website to crawl
def Crawler(website):
    # website = "octoprint.org"
    url     = "url=" + website
    limit   = "limit=" + "20000"
    start_year = "2005"
    end_year = "2014"
    timezone = "from="+ start_year+  "&to=" + end_year
    # fields are "urlkey","timestamp","original","mimetype","statuscode","digest","length" &output=json &fl=timestamp,statuscode
    fields  = "fl="     + "timestamp,statuscode"
    timestamp   = 0
    statuscode  = 1
    custom_filter = "&filter=!statuscode:200"
    # &collapse=timestamp:10 Given 2 captures 20130226010000 and 20130226010800, since first 10 digits 2013022601 match, the 2nd capture will be filtered out.
    collapse = "&collapse=timestamp:" + "6"
    output  = "output=" + "json"

    # api call building
    api_call = "http://web.archive.org/cdx/search/cdx" + "?" + url + "&" + timezone + "&" + limit + "&" + fields + "&" + collapse + "&" + output
    print api_call
    r = requests.get(api_call)
    print r
    decoded = json.loads(r.text)
    print decoded
    # We build the links and store them (?)
    for entry in decoded[1:]:
        print entry
        if str(entry[1]) == "200":

            link =  "https://web.archive.org/web/"+ entry[timestamp] + "/http://" + website
            print link
            request_page = requests.get(link)
            # remove the wayback machine footer
            answer_clean_pass1 = request_page.text[:-297].encode('utf-8').strip()
            # print answer_clean_pass1

            regex = r"<!-- BEGIN WAYBACK TOOLBAR INSERT -->.*<!-- END WAYBACK TOOLBAR INSERT -->"
            regex2 = r"<!-- Start Wayback Rewrite JS Include -->.*<!-- End Wayback Rewrite JS Include -->"
            answer_clean_pass1 = re.sub("\n","", answer_clean_pass1)
            # print answer_clean_pass1
            #print re.findall(r"(/web/[0123456789]+.{2}_/)", answer_clean_pass1)
            answer_clean_pass1 = re.sub(r"(/web/[0123456789]+.{2}_/)", "", answer_clean_pass1)
            # print answer_clean_pass1
             # return json object with website that was crawled, the timestamp, the status, and the content of the website
            answer_clean_pass2 = re.sub(regex, "", answer_clean_pass1)
            answer_clean_pass2 = re.sub(regex2, "", answer_clean_pass2)
            # print answer_clean_pass2
            PageInfo = analysePage(answer_clean_pass2)
            #print PageInfo

            date = str(entry[timestamp][6:8]) + "." + str(entry[timestamp][4:6]) + "." + str(entry[timestamp][0:4])

            pageObjectMongo = {
                "date": date,
                "link": website,
                "timestamp": entry[timestamp],
                "content": answer_clean_pass2,
                "status": entry[statuscode],
                "comments": PageInfo["comments"],
                "numberOfImgs": PageInfo["numberOfImgs"],
                "frameworks": PageInfo["frameworks"],
                "numberOfRefLinks": PageInfo["numberOfRefLinks"],
                "h1": PageInfo["h1"],
                "h2": PageInfo["h2"],
                "h3": PageInfo["h3"],
                "h4": PageInfo["h4"],
                "h5": PageInfo["h5"]
              }
            pagesHTML_collection.insert(pageObjectMongo)
            print "saved Object " + str(entry)
        #print pageObject
        else:
            print "Bad response"


# Crawler("octoprint.org")

Crawler("www.youtube.com")
