# -*- coding: utf-8 -*-
import requests
import re
import json
from mongoConnect import SaveToDatabase

#Website to crawl
def Crawler(link):
    # website = "octoprint.org"
    website = link
    url     = "url=" + website
    limit   = "limit=" + "3"
    start_year = "2010"
    end_year = "2011"
    timezone = "from="+ start_year+  "&to=" + end_year
    # fields are "urlkey","timestamp","original","mimetype","statuscode","digest","length" &output=json &fl=timestamp,statuscode
    fields  = "fl="     + "timestamp,statuscode"
    timestamp   = 0
    statuscode  = 1
    custom_filter = "&filter=!statuscode:200"
    # &collapse=timestamp:10 Given 2 captures 20130226010000 and 20130226010800, since first 10 digits 2013022601 match, the 2nd capture will be filtered out.
    output  = "output=" + "json"

    # api call building
    api_call = "http://web.archive.org/cdx/search/cdx" + "?" + url + "&" + limit + "&" + fields + "&" + output

    r = requests.get(api_call)
    decoded = json.loads(r.text)
    # We build the links and store them (?)
    for entry in decoded[1:]:
        link =  "https://web.archive.org/web/"+ entry[timestamp] + "/http://" + website
        print link
        request_page = requests.get(link)
        # remove the wayback machine footer
        answer_clean_pass1 = request_page.text[:-297].encode('utf-8').strip()

        regex = r"<!-- BEGIN WAYBACK TOOLBAR INSERT -->.*<!-- END WAYBACK TOOLBAR INSERT -->"
        answer_clean_pass1 = re.sub("\n","", answer_clean_pass1)
        #print re.findall(r"(/web/[0123456789]+.{2}_/)", answer_clean_pass1)
        answer_clean_pass1 = re.sub(r"(/web/[0123456789]+.{2}_/)", "", answer_clean_pass1)
         # return json object with website that was crawled, the timestamp, the status, and the content of the website
        answer_clean_pass2 = re.sub(regex, "", answer_clean_pass1)
        pageObject = json.dumps(
          {
            "link": website,
            "timestamp": entry[timestamp],
            "content": answer_clean_pass2,
            "status": entry[statuscode]
          }
        )
        SaveToDatabase(json.loads(pageObject))
        return pageObject

        # print answer_clean_pass1

Crawler("octoprint.org")

print Crawler("www.octoprint.org")
