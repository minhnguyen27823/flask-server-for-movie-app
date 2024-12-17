from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask import request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from bs4 import BeautifulSoup
import json
import getlink
import time
import timecompare as tc


def crawl(thresh_time):
    compare = tc.compare_with_current_time(thresh_time)
    if(compare == "Current time is before the given time"):
        movie_name="unkown"
        data={}
        driver = webdriver.Chrome()
        url = 'https://www.cgv.vn/home/'
        print("haha")
        driver.get(url)
        # credential = open('login.txt')
        # line = credential.readlines()
        # username = line[0]
        # password = line[1]
        sleep(2)
        search_field = driver.find_element(By.XPATH, '//*[@id="cboxClose"]')
        search_field.click()
        sleep(2)
        Clicknow = driver.find_element(By.XPATH, '//*[@id="top"]/body/div[3]/div/div[4]/div/div/div[1]/div/div/ul/li[2]/a')
        Clicknow.click()
        All_Movie = getlink.Getlink(driver)
        data=[]
        id = 0
        for movie in All_Movie:
            movie_data={}
            driver.get(movie)
            sleep(2)
            page_source = BeautifulSoup(driver.page_source, 'html.parser')
            movie_ten = page_source.find('div', class_='product-name').get_text(strip=True)
            movie_name = page_source.find('div', class_='movie-director movie-info').get_text(strip=True)
            movie_dienvien = page_source.find('div', class_='movie-actress movie-info').get_text(strip=True)
            movie_genra = page_source.find('div', class_='movie-genre movie-info').get_text(strip=True)
            movie_duration = page_source.find('div', class_='movie-release movie-info').get_text(strip=True)
            movie_time = page_source.find('div', class_='movie-actress movie-info').get_text(strip=True)
            movie_lang = page_source.find('div', class_='movie-language movie-info').get_text(strip=True)
            movie_rate = page_source.find('div', class_='movie-rating movie-rated-web').get_text(strip=True)
            movie_details = page_source.find_all('div', class_='movie-actress movie-info')
            movie_info_tags = page_source.find_all('div', class_='movie-actress movie-info')
            movie_review_page = page_source.find('div', class_='tab-content')
            movie_review = movie_review_page.find('div', class_='std').get_text(strip=True)
            for info in movie_info_tags:
                label = info.find('label').get_text(strip=True)
                content = info.find('div', class_='std').get_text(strip=True)

                if 'Đạo diễn:' in label:
                    movie_dienvien = content
                elif 'Thời lượng:' in label:
                    movie_time = f"{label} {content}"

            movie_image = page_source.find('div', class_='product-image-gallery')
            image_tags = movie_image.find_all('img')
            image_urls = []

            # Lặp qua tất cả các thẻ <img> và lấy giá trị của thuộc tính 'src'
            for img in image_tags:
                image_url = img['src']
                image_urls.append(image_url)
            # movie_data = (
            # "title":movie_ten, movie_name, movie_dienvien, movie_genra, movie_duration, movie_time, movie_lang, movie_rate,
            # movie_review,image_urls)
            movie_data["id"] = id
            movie_data["title"] = movie_ten
            movie_data["director"] = movie_name
            movie_data["dienvien"] = movie_dienvien
            movie_data["general"] = movie_genra
            movie_data["khoichieu"] = movie_duration
            movie_data["time"] = movie_time
            movie_data["languge"]= movie_lang
            movie_data["rate"] = movie_rate
            movie_data["review"]= movie_review
            movie_data["backdrop_path"] = image_urls[0]
            movie_data["poster_path"] = image_urls[1]
            data.append(movie_data)
            print(movie_ten)
            print(movie_name)
            print(movie_dienvien)
            print(movie_genra)
            print(movie_duration)
            print(movie_time)
            print(movie_lang)
            print(movie_rate)
            for idx, url in enumerate(image_urls):
                print(f"Image {idx + 1}: {url}")
            print(f"Review: {movie_review}")
            # print(movie_image)
            print('\n')
            id=id+1
        return jsonify(data), 200
    else:
        import json
        compare = tc.compare_with_current_time(thresh_time)
        print(compare)
        # Đường dẫn đến file JSON
        file_path = 'data.json'

        # Đọc file JSON
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # In dữ liệu đã đọc
        # print(data)

        # Truy cập các giá trị trong dữ liệu
        return jsonify(data), 200
    return jsonify(data), 200
