from requests_html import HTMLSession
import json

session = HTMLSession()

url = "https://www.imdb.com/title/tt9680440/"
data = session.get(url)

jsonRaw = data.html.find("script[type='application/ld+json']",first=True)
StoryLine = data.html.find("div[class='inline canwrap']",first=True)
titleDetail = data.html.find("div[id='titleDetails']",first=True)

jsonResponse = json.loads(jsonRaw.text)

actor_List = []
for i in range(len(jsonResponse['actor'])):
	actor_List.append(jsonResponse['actor'][i]['name'])

videoType = jsonResponse['@type']
videoName = jsonResponse['name']
videoGenre = jsonResponse['genre']
videoActor = actor_List
videDescription = jsonResponse['description']
videoDatePublished = jsonResponse['datePublished']
videRating = jsonResponse['aggregateRating']['ratingValue']


print("Video videoType", videoType)
print('videoName',videoName)
print('videoGenre', videoGenre)
print('videoActor', videoActor)
print('videDescription', videDescription)
print('videoDatePublished', videoDatePublished)
print('videRating', videRating)
print('\n StoryLine', StoryLine.text)
print('\n\n\n Detail', titleDetail.text)
