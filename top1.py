import requests 
 				# Requests module, that we use to send all kind of HTTP requests.   
from bs4 import BeautifulSoup
   				# Beautiful Soup library for pulling data out of HTML and XML files.   
import pprint
  					# Uses of pprint for data pretty print
import os
  				# OS module they provide a way to dependent of operating system functionality.
import json
  				# Json pakages uses of data exchanges 
import random, time
  				# random module use for generate randomly data.
  				# time module return the second where time begins start.

# task1..............................................................................................................................
						# here scrape movies's name, positon, url, year, rating
def scrape_top_list():
	url = "https://www.imdb.com/india/top-rated-indian-movies/"
	a=requests.get(url)
	soup = BeautifulSoup(a.text,"html.parser")
	# print(soup)
	top_movies_list = []
	main_div = soup.find('div',class_="lister")
	# print(main_div)
	tbody = main_div.find('tbody',class_="lister-list")
	trs = tbody.find_all('tr')
	# print (trs)
	for tr in trs:
		movies_data = tr.find('td',class_="titleColumn")
		# print (movies_data)
		position = movies_data.get_text().strip().split(".")[0]
		# print(position)

		names = movies_data.find('a').get_text()
		year = movies_data.find('span').text.strip("()")
		
		movie_url = movies_data.find('a').get('href')
		imdb_url = 'https://www.imdb.com' + movie_url
		movie_rating = tr.find('td',class_="ratingColumn imdbRating").strong.get_text()
		top_movie_dic = {"names":"","year":"","position":"","url":"","rating":""}
		top_movie_dic['names']=names

		top_movie_dic['year']=int(year.strip("()"))
		top_movie_dic['position']=position
		top_movie_dic['rating']=float(movie_rating)
		# print(top_movie_dic['rating'])
		top_movie_dic['url']=imdb_url
		# print(top_movie_dic['url'])
		top_movies_list.append(top_movie_dic)
	return top_movies_list
# pprint.pprint (scrape_top_list())

top_movies=scrape_top_list()


# task2..............................................................................................................###
						# here analyse group by year
def group_by_year():
	top_movies=scrape_top_list()
	dic={}
	for movie in top_movies:
		dic[movie["year"]]=[]
		print (dic)
	for movie_key in dic:
		for key in top_movies:
			movie_year=key["year"]
			print(movie_year)
			if movie_key==movie_year:
				dic[movie_key].append(key)
	# pprint.pprint (dic)
	return(dic)		
# pprint.pprint(group_by_year())	
# dictionary=group_by_year(top_movies)


# ##task 3..............................................................................................................###

def group_by_decade(top_movies):
	movie_by_decade = {}
	for movie in top_movies:
		division = movie['year']//10
		decade = division * 10
		movie_by_decade[decade]=[]
		# print(movie_by_decade)
	for decade_key in movie_by_decade:
		for movie in top_movies:
			division = movie['year']//10
			decade = division * 10
			if decade_key==decade:
				movie_by_decade[decade_key].append(movie)
	# pprint.pprint(movie_by_decade)
				
	

		
group_by_decade(top_movies)

##task12...................................................................................................................##
									# Here we analyse their caste of movie in individually.
def scrape_movie_caste(movie_caste_url):
	s_l=movie_caste_url[:37]
	a_=s_l[27:]

	page=requests.get(movie_caste_url)
	soup=BeautifulSoup(page.text,"html.parser")
	f = soup.find_all("div",class_="see-more")
	for c_ in f:
		if "See full cast »" == c_.text.strip():
			# x_=c.find_all('a')
			create_=(c_.find('a').get('href'))
			ul_="https://www.imdb.com/title/"+a_+create_
			# print(ul_)
			get_=requests.get(ul_)
			soup_=BeautifulSoup(get_.text,"html.parser")
			# print(soup_)

			main_div=soup.find("table",class_="cast_list")
			tds=main_div.find_all("td",class_="")
			list = []
			for td in tds:
				dic={}
				p=td.find("a").get("href")[6:15]
				dic["imdb_id"]=p
				s=td.find("a").text.strip()
				dic["name"]=s
				# print (dic)
				list.append(dic)
			return(list)
# movie_caste=scrape_movie_caste(top_movies[0]['url'])
# pprint.pprint("rohit")
# pprint.pprint(movie_caste)



## task4......................................................................................................##


def scrape_movie_details(movie_url):

	##task 9
	random_time = random.randint(1,3)
	# print(random_url)

	#task 8
	ID_=''
	a=movie_url[:36]
	next_a=a[27:]
	if os.path.exists("details_data/"+next_a+'.json'):
		with open("details_data/"+next_a+'.json',"r") as show_file:
			show_data = json.load(show_file)
			return(show_data)
	else:
		c=[]
		time.sleep(random_time)
		page = requests.get(movie_url)
		soup = BeautifulSoup(page.text,"html.parser")
		# print(soup.title)
		name = soup.find('div', class_="title_wrapper").h1.get_text().split()
		name.pop()
		movie_name = ' '.join(name)
		movie_bio = soup.find('div',class_="summary_text")
		# print(movie_bio)
		movie_details = soup.find('div',class_="plot_summary")
		movie_bio = movie_details.find('div',class_="summary_text").get_text().strip()
		# print(movie_bio)
		movie_director = movie_details.find('div', class_="credit_summary_item")
		directors = movie_director.find_all('a')
		director_list = [director.get_text() for director in directors]
		# print(director_list)
		movie_poster_url = soup.find('div', class_="poster").a.img['src']
		# print(movie_poster_url)
		movies_data = soup.find("div", class_="title_wrapper")
		# print(movies_data)
		movie_genre = movies_data.find('div', class_='subtext')
		geners  = movie_genre.find_all('a')
		geners.pop()
		gener_list = [gener.get_text() for gener in geners]
		# print(gener_list)
		movie_runtime = movie_genre.find('time').get_text().split()
		minutes = 0
		for time_ in movie_runtime:
			if 'h' in time_:
				hours_to_min = int(time_.strip('h')) * 60
			elif 'min' in time_:
				minutes = int(time_.strip('min'))
		runtime = hours_to_min + minutes
		# print(runtime)
		txt_block = soup.find("div", attrs={'class':'article', 'id': 'titleDetails'})
		language_block = txt_block.find_all("div",class_="txt-block")
		# print(language_block)
		for i in language_block:
			h4 = i.find('h4')
			if h4:
				if h4.text == 'Language:':
					at = i.find_all('a')
					for b in at:
						c.append(b.text)
				elif h4.text == 'Country:':
					bt = i.find_all('a')
					# print(bt)
					for v in bt:
						d=(v.text)
						# print(d)
		movie_details_dict = {'name':'','bio':'','gener':'','movie_poster_url':'','Language':'','Country':'','director':'','runtime':''}
		movie_details_dict['name'] = movie_name
		movie_details_dict['bio'] = movie_bio
		movie_details_dict['gener'] = gener_list
		movie_details_dict['movie_poster_url'] = movie_poster_url
		movie_details_dict['Language'] = c
		movie_details_dict['Country'] = d
		movie_details_dict['director'] = director_list
		movie_details_dict['runtime'] = runtime
		# movie_details_dict['caste'] = scrape_movie_caste(movie_url)

		with open('details_data/'+next_a+'.json',"w") as show_file:
			json.dump(movie_details_dict,show_file)



		return (movie_details_dict)


movie_details = scrape_movie_details(top_movies[0]['url'])
pprint.pprint(movie_details)


## task5...........................................................................................##
								# In this task, we have to analyse to scrape movie detail.
def get_movie_details(movie_list):
	count = 0
	top_10_movies_list = []
	for movie in movie_list:
		count+=1
		movie_url = movie['url']
		movie_dict = scrape_movie_details(movie_url)
		top_10_movies_list.append(movie_dict)
		if count == 250:
			break
	return(top_10_movies_list)
	# pprint.pprint(top_10_movies_list)


top_10_movies = get_movie_details(top_movies)
# pprint.pprint(top_10_movies)
# pprint.pprint('rohit')

## task6..........................................................................................##
									# In this task, we have analyse of movie_languages.
def analyse_movie_language(movie_list):
	
	movies_by_language = {}
	for movie in movie_list:
		for language in movie['Language']:
			movies_by_language[language] = 0
	for lang in movies_by_language:
		for movie_ in movie_list:
			if lang in movie_['Language']:
				movies_by_language[lang] +=1
	return movies_by_language
			

		

film_language =analyse_movie_language(top_10_movies)
# pprint.pprint(film_language)

##task 7.............................................................................................##
										# In this task, analyses of movie director.					
def analyse_movie_director(movie_list):
	director_dict = []
	new_direct_dict = {}
	for direct_ in movie_list:
		# print(direct_['director'])
		for film_directors in direct_['director']:
			if film_directors not in director_dict:
				director_dict.append(film_directors)
	# print(director_dict)
	for director_ in director_dict:
		count=0
		for direct_ in movie_list:
			for All_directors in direct_['director']:
				if director_ == All_directors:
					count+=1
		new_direct_dict[director_]=count
	return(new_direct_dict)




film_director=analyse_movie_director(top_10_movies)
# pprint.pprint(film_director)
# pprint.pprint('rohit')

## task 10.............................................................................................................
											# Here we analyse language and director of movie.
def analyses_language_and_director(movie_list):
	dic_director={}
	for mov in movie_list:
		# return(mov)
		for director in mov['director']:
			dic_director[director] = {}
	# print(dic_director)
	for i in range(len(movie_list)):
		for director in dic_director:
			if director in movie_list[i]['director']:
				for language_ in movie_list[i]['Language']:
					dic_director[director][language_]=0
	# return(dic_director)

	for i in range(len(movie_list)):
		for director in dic_director:
			if director in movie_list[i]['director']:
				for language_ in movie_list[i]['Language']:
					dic_director[director][language_] +=1
	return(dic_director)


language_director=analyses_language_and_director(top_10_movies)
# pprint.pprint(language_director)

## task 11....................................................................................
									# Here we analyse the Genres of movie.
def analyses_movie_genre(movie_list):
	list_gener = []
	for list1 in movie_list:
		# return (list1)
		geners = list1['gener']
		# print(geners)
		for i in geners:
			if i not in list_gener:
				list_gener.append(i)
	# return(list_gener)
	gener_anallys = {gener_type:0 for gener_type in list_gener}
	for gener_type in list_gener:
		for list1 in movie_list:
			if gener_type in list1['gener']:
				gener_anallys[gener_type] +=1
	# return (gener_anallys)




gener_analysis=analyses_movie_genre(top_10_movies)
# print(gener_analysis)


## task15................................................................................................
									# Here analyse caste details of movie.
def analysis_caste_details(movie_list):
	dic1={}
	for movie in movie_list:
		cast=movie["caste"]
		# pprint.pprint(cast)
		for i in cast:
			# pprint.pprint(i)
			imdb_id=i["imdb_id"]
			# pprint.pprint(imdb_id)
			dic={"name":"","no_of_movies":0}

			for j in movie_list:
				cas=j["caste"]
				for n  in cas:
					if imdb_id==n["imdb_id"]:
						dic["name"]=i["name"]
						dic["no_of_movies"]+=1
						# pprint.pprint(dic)
			dic1[imdb_id]=dic	
	# pprint.pprint(dic1)				
# analysis_caste_details(top_10_movies)

