from __future__ import unicode_literals
import random
import time
import os
import re
import shutil
import youtube_dl
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from sys import argv

# Download data and config

download_options = {
	'format': 'bestaudio/best',
	'outtmpl': '%(title)s.%(ext)s',
	'nocheckcertificate': True,
	'postprocessors': [{
		'key': 'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
		'preferredquality': '192',
	}],
}


chrome_options = Options()
chrome_options.add_argument("--start-maximized");

driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get('https://www.shazam.com/fr/myshazam')

mail='your email'
mdp='your password'


#LOG IN (with facebook)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "/login/app/myshazam")))
driver.find_element_by_xpath('//*[@id="/login/app/myshazam"]/a[1]').click()

for handle in driver.window_handles:
 driver.switch_to.window(handle)


time.sleep(1)
driver.find_element_by_xpath('//*[@id="email"]').send_keys(email)
time.sleep(1)
driver.find_element_by_xpath('//*[@id="pass"]').send_keys(mdp)
time.sleep(1)
driver.find_element_by_xpath('//*[@id="u_0_0"]').click()
time.sleep(5)
driver.switch_to.window("")

time.sleep(5)

#NB SHAZAM
driver.execute_script("window.scrollBy(0, 2500);")
time.sleep(3)
links = driver.find_elements_by_xpath('//*[@id="/myshazam/shazams"]/ul/li')
len(links)


time.sleep(3)
#TITRE
titres = []
for c in range(1,len(links)+1):
 titreComplet = driver.find_element_by_xpath('//*[@id="/myshazam/shazams"]/ul/li['+ str(c) +']').text
 title = titreComplet.split('\n')[1]
 artiste = titreComplet.split('\n')[2]
 titreQOk = artiste + ' - ' + title
 titreOk=titreQOk.replace('&',' ')
 print(titreOk)
 titres.append(titreOk)
 

# Song Directory
if not os.path.exists('Songs'):
	os.mkdir('Songs')
else:
	os.chdir('Songs')

 
for titre in titres:
 driver.get('https://www.youtube.com/results?search_query='+ str(titre))
 lien = driver.find_element_by_xpath('//*[@id="contents"]/ytd-video-renderer[1]').find_element_by_id("video-title").get_attribute("href")
 print(lien)
 # Download Songs
 with youtube_dl.YoutubeDL(download_options) as dl:
  dl.download([str(lien)])


#DEPLACEMENT DES SONS

source =r'C:\Users\AppData\Local\Programs\Python\Songs'
dest1 = r'path you want your songs to be'

files = os.listdir(source)

for f in files:
 shutil.move(source+'\\'+f, dest1)
 
driver.close()