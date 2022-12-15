import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇

html = BeautifulSoup(requests.get(URL).text, 'html.parser')
movies_list = [movie.getText()+'\n' for movie in html.find_all(name="h3", class_="title")][::-1]

print(movies_list)

with open("top_100_movies/top_100_movies.txt", "a") as file:
    for movie in movies_list:
        if 'â\x80\x93' in movie:
            file.write(movie.replace('â\x80\x93', '-'))
        else:
            file.write(movie)
