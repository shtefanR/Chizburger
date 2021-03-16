from bs4 import BeautifulSoup
import requests, bs4, json, time
start_time = time.time()
headers = {
    "User-Agent" : "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 88.0.4324.111 YaBrowser / 21.2.1.107 Yowser / 2.5 Safari / 537.36"
}
f = open("file.json", "w", encoding = "utf-8")
def getComments(url, title, headers):
    soup = bs4.BeautifulSoup(requests.get(url, headers).text, "html.parser")
    [i.extract() for i in soup.find_all('br')]
    commentAuthors = soup.select('.comments__item__user__name span:first-child')
    commentContents = soup.select('.comments__item__text', recursive = True)
    eachComment = {"author": "", "text": ""}
    comments = []
    for i, j in zip(commentAuthors, commentContents):
        eachComment["author"] = i.find(text=True)
        eachComment["text"] = "".join(j.find_all(text=True))
        comments.append(eachComment)
        eachComment = {}
    post = {}
    post["url"] = url
    post["title"] = title
    post["comments"] = comments
    return(post)

soup = bs4.BeautifulSoup(requests.get("https://vc.ru/", headers).text, "html.parser")
urls = []
titles = []
allComments = []
for cycle in range (25):
    for i in soup.find_all(class_ = 'news_item__title t-link l-fs-16 l-lh-24 l-mr-8'):
        urls.append(i.get('href'))
        titles.append(i.get_text())
        lastPostID = int(''.join(filter(str.isdigit, i.get('href')))[:6])
    soup = bs4.BeautifulSoup(requests.get(f"https://vc.ru/news/more/{lastPostID}?mode=raw", headers).json()['data']['html'], "html.parser")

for url, title in zip(urls, titles):
    allComments.append(getComments(url, title, headers))

json.dump(allComments, f, ensure_ascii=False, indent=1)
f.close()
print(f"this code ran for {(time.time() - start_time)} seconds")