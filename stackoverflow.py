from bs4 import BeautifulSoup
import requests
from os import mkdir, path
from matplotlib.pyplot import savefig
import matplotlib.pyplot as plt

'''
# To get tag list of particular question by its url.
def get_tag_list(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    res = soup.find('div', {'class': 'post-taglist'}).find_all('a')
    tag_list=[]
    for anch in res:
        s = anch['href'].split('/')
        tag_list.append(s[-1])
    return tag_list
'''

URL = "http://stackoverflow.com/questions?pagesize=50&sort=newest&page="
lang_freq = {}
tech_freq = {}
LANGUAGE_LIST = ['javascript', 'java', 'c#', 'php', 'android', 'python', 'html', 'c++', 'ios', 'sql', 'css', '.net',
                 'objective-c', 'c', 'ruby', 'vb.net', 'perl', 'scala', 'haskell', 'shell', 'go', 'swift', 'matlab', 'flash']
TECH_LIST = ['ruby-on-rails', 'angularjs', 'json', 'ajax', 'django', 'node.js', 'wordpress', 'mongodb', 'hibernate', 'hadoop', 'opencv',
             '.htaccess', 'apache-spark', 'coffeescript', 'git']

for lang in LANGUAGE_LIST:
    lang_freq[lang] = 0
for tech in TECH_LIST:
    tech_freq[tech] = 0


def page_tag_list(url):
    # Updates tag list of questions present on given url page.
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    res = soup.find_all('a', {'class': 'post-tag'})
    for _ in res:
        tag = _.string
        if tag in LANGUAGE_LIST:
            lang_freq[tag] += 1
        if tag in TECH_LIST:
            tech_freq[tag] += 1


def tag_pages(n):
    # Updates the total of tags present on first 'n' pages at given time.
    for i in range(n):
        print("getting page %d"%(i+1))
        url = URL + str(i+1)
        page_tag_list(url)

n = int(input("Enter number of pages to scrap(50 posts per page): "))
tag_pages(n)

file_path = "stackoverflow_analysis"
if not path.exists(file_path):
    mkdir(file_path)

lang_file = open(file_path+"/languages.txt", 'w')
tech_file = open(file_path+"/technologies.txt", 'w')

for lang in lang_freq:
    line = str(lang) + " " + str(lang_freq[lang]) + "\n"
    lang_file.write(line)
for tech in tech_freq:
    line = str(tech) + " " + str(tech_freq[tech]) + "\n"
    tech_file.write(line)

lang_file.close()
tech_file.close()

plt.figure(figsize=(12,14))
plotx = [i+1 for i in range(len(lang_freq.keys()))]
plt.bar(plotx, lang_freq.values())
plt.xticks(plotx, lang_freq.keys(), rotation='vertical')
for a,b in zip(plotx, lang_freq.values()):
    plt.text(a, b, str(b), ha='center', va='bottom')
plt.xlabel("Language")
plt.ylabel("Occurence")
plt.title("Language stats")
savefig(file_path+'/language_stats.png')
plt.clf()

plotx = [j+1 for j in range(len(tech_freq.keys()))]
plt.bar(plotx, tech_freq.values())
plt.xticks(plotx, tech_freq.keys(), rotation='vertical')
plt.xlabel("Technologies")
plt.ylabel("Occurence")
plt.title("Tech stats")
for a,b in zip(plotx, tech_freq.values()):
    plt.text(a, b, str(b), ha='center', va='bottom')
savefig(file_path+'/tech_stats.png')
plt.clf()

print("Done!")
s = input("Data and graphs saved in " + file_path + " directory.")