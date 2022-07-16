import requests
import re
from html import unescape
import json
from datetime import datetime
from pycookie import chromecookie

try:
    ID = input("\n Enter [ Number in URL ] ID : ")

    if ID:
        url = (f"https://nhentai.net/g/{ID}/")
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        }
        webdata = requests.get(url, cookies=chromecookie('nhentai.net').cookies(), headers=headers).text
        if '404 - Not Found' in webdata:
            print("\n Seems to be an INVALID ID Number Check Again!")
        else:
            raws = re.search(r'JSON.parse.{2}({.+})', webdata).group(1)
            JsonData = json.loads(raws.encode('utf-8').decode('unicode-escape'))
            with open('%s.json' % ID, 'w') as file:file.write(json.dumps(JsonData, indent=4))
            title = re.search(r'class="before">(?P<artist>.*)</span>[^=]+="pretty">(?P<title>.+)</span><span class="after">(?P<misc>.*)</span></h1>', webdata)
            language = re.findall(r'<a href="/language/([^/]+)', webdata)
            raw_strings = re.findall(r'data-src="(https?)://[A-z]+([0-9]+).{25,35}/(?:[0-9]+[A-z]+).([^"]+)', webdata)
            print("\n -------------------------------------")
            print(f" : Manga Name : {unescape(title.group('title'))}")
            print(" -------------------------------------")
            print(f" : Artist     : {title.group('artist')}")
            print(" -------------------------------------")
            print(f" : Manga Info :{title.group('misc')}")
            print(" -------------------------------------")
            print(f" : Language   : {[x.upper() for x in language]}")
            print(" -------------------------------------")
            print(f" : Uploaded   : {datetime.fromtimestamp(JsonData['upload_date'])}")
            print(" -------------------------------------")
            print(f" : Pages      : {JsonData['num_pages']}")
            print(" -------------------------------------")

            links, star = [], 1
            for x in raw_strings:
                link = "%s://i%s.nhentai.net/galleries/%s/%s.%s" % (x[0], x[1], JsonData['media_id'], star, x[2])
                links.append(link)
                star+=1
            print(f" : Images     : {len(links)}")
            print(" -------------------------------------")
            m = open(f"Links [{ID}].txt", "w")
            for a in links:
                m.write(a+"\n")
            m.close()
            print(" : All Links to Images Saved Locally!")
            print(" -------------------------------------")

    else:
        print("\n Enter Following [ https://nhentai.net/g/{ID}! ] :)")

except NameError as error:
    print(f"\n Oops! This Happened : {error}")

