from bs4 import BeautifulSoup
import requests

date = input("Which date do you want to travel to? Type the date in this format YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(URL)

bilboard_hot_100_web_page = response.text

soup = BeautifulSoup(bilboard_hot_100_web_page, "html.parser")

songs_list = soup.find_all(name="h3", class_='a-no-trucate')

songs = [song.getText().strip() for song in songs_list]

print(songs)
