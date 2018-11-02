import urllib
from bs4 import BeautifulSoup
import csv
url = "http://gwern.net/"
f = urllib.urlopen(url) 
soup = BeautifulSoup(f)
links_from_homepage=[]
link_texts=[]
for link in soup.find_all('a'):
    linkhref=link.get('href')
    linktext=link.contents[0]
    fulllink=url+linkhref
    links_from_homepage.append(fulllink)
    link_texts.append(linktext.encode('utf-8'))
print("Done with scraping homepage!")
importances=list(links_from_homepage)
for a in importances:
    a = "X"
i=0
while i < len(links_from_homepage):
    try:
        f=urllib.urlopen(links_from_homepage[i])
        soup=BeautifulSoup(f)
        text=soup.get_text()
        result=text.find('importance')+12
        if text[result] == u'1':
            if text[result+1] == u'0':
                importances[i]='10'
            else:
                importances[i]=text[result].encode('utf-8')
        else:
            importances[i]=text[result].encode('utf-8')
    except Exception:
        pass
    i +=1

list_of_acceptable_importances=['0','1','2','3','4','5','6','7','8','9','10']
with open('gwern_importances.csv', mode='w') as output_file:
    filewriter = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for index,importance in enumerate(importances):
        if importance in list_of_acceptable_importances:
             filewriter.writerow([link_texts[index],links_from_homepage[index],importance])
