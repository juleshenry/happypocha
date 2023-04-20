with open('food.html') as f:
	krn=[]
	for l in f.readlines():
		x = ''.join(c for c in l if ord(c)> 1000 and ord(c) < 70000 )
		if x:krn.append(x)


import requests
from bs4 import BeautifulSoup
import os

MAX_IMAGES = 1
SEARCH_ENGINE = 'NAVER'

def url_getter(search_engine):
	#default google
	match search_engine:
		case 'GOOGLE':
			return lambda q: 'https://www.google.com/search?q=' + q + '&source=lnms&tbm=isch'
		case 'NAVER':
			return lambda q: f"https://search.naver.com/search.naver?where=image&query={q}"
		case _:
			return lambda q:'https://www.google.com/search?q=' + q + '&source=lnms&tbm=isch'

# List of food items to search for
food_items = krn

get_url = url_getter(SEARCH_ENGINE)
# Define function to download images
def download_image(url, file_path):
    response = requests.get(url)
    with open(file_path, "wb") as f:
        f.write(response.content)

# Create directory to store images
if not os.path.exists('food_images'):
    os.mkdir('food_images')


# Loop through food items
for item in food_items[:2]:
    # Construct search URL
    search_url = get_url(item)
    print(search_url,"SERCHN")
    # Make request to URL
    response = requests.get(search_url)
    # Parse HTML response with Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all image tags
    images = soup.find_all('img')
    print(images)
    # Loop through images and download them
    i = 1
    for image in images[:MAX_IMAGES]:
        # Get image source URL
        image_url = image['src']
        # Construct file name for image
        try:
            file_name = f'food_images/{item}_{i}.jpg'
            download_image(image_url, file_name)
            i += 1
        except:
            pass
        # Download image

