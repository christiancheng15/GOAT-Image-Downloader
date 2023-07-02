# -------------------------#
# Goat Image Downloader    #
# Author: Christian Cheng  #
# GitHub: christiancheng15 #
# -------------------------#

import requests
from bs4 import BeautifulSoup
import json
from art import *
import re
import os

def menu():
    # Menu
    tprint("GOAT ID")
    print("Usage:")
    print("1. Input GOAT link e.g. https://www.goat.com/en-au/sneakers/dunk-low-black-white-dd1391-100")
    print("2. Press ENTER to generate GIF")
    print("Note: Not all products have HD images. It may take upwards of 30 seconds. Enter Q/q to quit.\n")

def download_images():
    # User enter GOAT link e.g. https://www.goat.com/en-au/sneakers/dunk-low-black-white-dd1391-100
    while True:
        url = input("GOAT Link: ")

        # Enter Q/q to quit 
        if url.lower() == "q":
            quit()

        # Validate StockX link format https://www.goat.com/en-au...
        # 1. Validate regex
        pattern = r"^https:\/\/www\.goat\.com\/[a-z]{2}-[a-z]{2}\/[a-z-]+\/[a-zA-Z0-9-]+$"
        if re.match(pattern, url):
            # 2. Validate url exists
            response = requests.get(url)
            if response.status_code < 400:
                break
        else:
            url = re.sub(r"^https:\/\/www\.goat\.com(?!\/[a-z]{2}-[a-z]{2})", "https://www.goat.com/en-au", url)
            response = requests.get(url)
            if response.status_code < 400:
                break
        print("Error. Please enter a valid GOAT link. https://www.goat.com/en-au...")

    # Get product name e.g. product_name_01.jpg
    product_name = url.split("/")[-1]
    
    # Create new folder directory /product_name/
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, product_name)
    os.makedirs(folder_path, exist_ok=True)

    # Parse HTML page and scrape images
    soup = BeautifulSoup(response.content, "html.parser")
    next_data = soup.find("script", id="__NEXT_DATA__", type="application/json").text
    next_data_json = json.loads(next_data)

    try:
        images = next_data_json["props"]["pageProps"]["productTemplate"]["productTemplateExternalPictures"]
        for image in range(0,len(images)):
            image_url = images[image]["mainPictureUrl"]

            # Format URL to HD photos + crop photos
            formatted_image_url = str(image_url).replace(".com/", ".com/transform/v1/").split("?")[0].replace("medium", "original") + "?action=crop&width=2000"
            response = requests.get(formatted_image_url)

            # Check if image exists. Yes - Download Image / No - Exit
            if response.status_code == 200:
                with open(f"{product_name}/{product_name}_{image+1:02d}.jpeg", "wb") as file:
                    file.write(response.content)
                print("Image downloaded successfully.")
            else:
                print("Failed to download the image.")
    except:
        image_url = next_data_json["props"]["pageProps"]["productTemplate"]["mainPictureUrl"]

        formatted_image_url = str(image_url).replace(".com/1000/", ".com/transform/v1/").split("?")[0] + "?action=crop&width=2000"
        response = requests.get(formatted_image_url)

        # Check if image exists. Yes - Download Image / No - Exit
        if response.status_code == 200:
            with open(f"{product_name}/{product_name}_01.png", "wb") as file:
                file.write(response.content)
            print("Image downloaded successfully.")
        else:
            print("Failed to download the image.")

menu()
while True:
    download_images()