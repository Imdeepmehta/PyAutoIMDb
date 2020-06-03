from django.shortcuts import render, redirect
from django.http import JsonResponse
from requests_html import HTMLSession
import json


def searchMovieIMDb(movieSearchName):
	session = HTMLSession()
	searchUrl = 'https://www.imdb.com/find?q='+movieSearchName
	data = session.get(searchUrl)
	totalMovie = data.html.find("table[class='findList']",first=True).absolute_links
	# print(totalMovie)

	movieDict = {}
	indexMovie = []
	indexMovieImgUrl = []
	for i,movi in enumerate(totalMovie):
		# print(movi)
		try:
			indexMovie.append(movi[27:36])
			img = data.html.find("table[class='findList']",first=True).find('img')[i].html[10:-3]
			name = data.html.find("table[class='findList']")[0].text.split('\n')[i]
		# print(img)
			indexMovieImgUrl.append(img)
			movieDict[movi[27:36]] = img,name
		except:
			print("hah")
	return movieDict



def movieDetail(request,moviID):

	finalMovieData = retriveMovieData(moviID)
	context = {
		'movieData' : finalMovieData
	}

	return render(request, 'movie.html', context=context)

def retriveMovieData(moviID): 
	movieStack = {}
	print("movidID:", moviID)
	finalUrl = 'https://www.imdb.com/title/'+moviID
	print('Final Url:', finalUrl)

	session = HTMLSession()
	movieData = session.get(finalUrl)
	print(movieData.status_code)

	jsonRaw = movieData.html.find("script[type='application/ld+json']",first=True)
	jsonResponse = json.loads(jsonRaw.text)

	actor_List = []
	for i in range(len(jsonResponse['actor'])):
	    actor_List.append(jsonResponse['actor'][i]['name'])
	creator_List = []
	for j in range(len(jsonResponse['creator'])):
	    try:
	        creator_List.append(jsonResponse['creator'][j]['name'])
	    except KeyError:
	        print('haha')
	creator_List = list(set(creator_List))
	videoType = jsonResponse['@type']
	videoDirector = jsonResponse['director']['name']
	videoName = jsonResponse['name']
	videoGenre = jsonResponse['genre']
	videoActor = actor_List
	videDescription = jsonResponse['description']
	# videoDatePublished = jsonResponse['datePublished']
	videRating = jsonResponse['aggregateRating']['ratingValue']

	summary = movieData.html.find("div[class='summary_text']",first=True).text
	taglines = movieData.html.find("div[class='txt-block']", first=True).text[10:]
	runtime = movieData.html.find("div[class='txt-block']",)[-4].text[9:]
	budget = movieData.html.find("div[class='txt-block']",)[-7].text[8:]
	StoryLine = movieData.html.find("div[class='inline canwrap']",first=True).text


	# print("\n StoryLine:", StoryLine)
	# print("\n Summary:", summary)
	# print("\n Tagline:", taglines)
	# print("\n Movie Director : ", videoDirector)
	# print("\n Movie Writer : ", creator_List)
	# print("\n Actors:", videoActor)
	# print("\n Video Format:", videoType)
	# print("\n Video Name :", videoName)
	# print("\n video Genre:", videoGenre)
	# print("\n video Description:", videDescription)
	# print("\n video Data Published:", videoDatePublished)
	# print("\n video Rating:", videRating)
	# print("\n runtime:", runtime)
	# print("\n budget:", budget)

	movieStack['Rating'] = videRating
	movieStack['Genre'] = ','.join(videoGenre)
	movieStack['movie Director'] = videoDirector
	movieStack['Movie Actor'] = ','.join(videoActor)
	movieStack['Budget'] = budget
	movieStack['Runtime'] = runtime

	movieStack['StoryLine'] = StoryLine
	movieStack['summary'] = summary
	movieStack['taglines'] = taglines
	movieStack['Movie Writer'] = ','.join(creator_List)
	movieStack['movie Type'] = videoType
	movieStack['Name'] = videoName
	movieStack['Description'] = videDescription
	# movieStack['Published Date'] = videoDatePublished

	return movieStack

def querySearch(request, q):
	# allMovieDataUrl, allMovieDataImgUrl = searchMovieIMDb('3 idiot ')
	allMovieData= searchMovieIMDb(q)

	context = {
	'allMovieData' : allMovieData
	# 'totalMovieFound' : len(allMovieDataUrl),
	# 'moviesUrl' : allMovieDataUrl,
	# 'moviesImgUrl' : allMovieDataImgUrl, 
	}
	return(render(request, 'query.html', context=context))

def home(request):
	if request.method == 'POST':
		print(request.POST)
		userQuery = request.POST.get('query')
		print(userQuery)
		return redirect("/search/"+userQuery)
	else:
		return(render(request, 'index.html',))




