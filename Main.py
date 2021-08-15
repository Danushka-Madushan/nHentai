import requests
import msvcrt
import sys
import re

try:
    ID = input("\n Enter [ Number in URL ] ID : ")

    if ID:
        url = (f"https://nhentai.to/g/{ID}")
        webdata = requests.get(url).content.decode("utf-8")
        if re.search(r'<div class="code">\D+404[ ]*</div>', webdata):
            print("\n Seems to be an INVALID ID Number Check Again!")
            msvcrt.getch()
            sys.exit()
        else:

            title = re.search(r'<div id="info">\D+<h1>(.+?)</h1>', webdata).group(1)
            copyright = re.search(r'<div class="tag-container field-name ">\D+Parodies\D+<span class="tags">\D+class="tag tag-[0-9]* ">(.+?)</a>', webdata).group(1)
            up_time = re.search(r'<div>Uploaded <time datetime="([0-9-]*)', webdata).group(1)
            pages = re.search(r'<div>([0-9]*) pages</div>', webdata).group(1)
            language = re.search(r'<div class="tag-container field-name ">\D+Languages\D+<span class="tags">\D+class="tag tag-[0-9]* ">(.+?)</a>', webdata).group(1)
            raw_strings = re.findall(r'data-src="(https?://[A-z.]*/galleries/[0-9]*/[0-9]*)t(.[a-z]*)"', webdata)
            print("\n -------------------------------------")
            print(f" : Manga Name : {title}")
            print(" -------------------------------------")
            print(f" : Language   : {language.upper()}")
            print(" -------------------------------------")
            print(f" : Parodies   : {copyright.upper()}")
            print(" -------------------------------------")
            print(f" : Uploaded   : {up_time}")
            print(" -------------------------------------")
            print(f" : Pages      : {pages}")
            print(" -------------------------------------")

            links = []
            for x in raw_strings:
                links.append(x[0]+x[1])
            print(f" : Images     : {len(links)}")
            print(" -------------------------------------")
            m = open(f"Links [{ID}].txt", "w")
            for a in links:
                m.write(a+"\n")
            m.close()
            print(" : All Links to Images Saved Locally!")
            print(" -------------------------------------")
            msvcrt.getch()
            sys.exit()

    else:
        print("\n Enter Following [ https://nhentai.to/g/{ID}! ] :)")
        msvcrt.getch()
        sys.exit()

except Exception as error:
    print(f"\n Oops! This Happened : {error}")
    msvcrt.getch()
