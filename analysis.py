from bs4 import BeautifulSoup, Comment
import re

def analysePage(site):

    site = BeautifulSoup(site)
    results = {}

    #find comments
    filteredComments = []
    comments = site.findAll(text=lambda text:isinstance(text, Comment))

    for comment in comments:
        if "<" not in comment and "\\" not in comment and "machid" not in comment and len(comment) < 100:
            filteredComments.append(comment)
    results["comments"] = filteredComments

    #find frameworks
    frameworks = []

    for link in site.findAll("script"):
        if link.get("src"):
           for element in link.get("src").split("/"):
                if ".js" in element:
                    if "?" in element:
                        element = element.split("?")[0]
                    frameworks.append(element)
    results["frameworks"] = frameworks

    results["numberOfImgs"] = len(site.findAll("img"))

    results["numberOfRefLinks"] = 0
    for link in site.findAll("a"):
        # print link
        if "ref" in link or "affi" in link:
            results["numberOfRefLinks"] += 1



    for size in [1, 2, 3, 4, 5]:
        headline = "h"+str(size)
        results[headline] = []
        lines = site.findAll(headline)
        for line in lines:
            results[headline].append(line.text)



    return results
