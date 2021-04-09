import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

options = Options()
prefs = {'download.default_directory' : '/Volumes/Jose Songs'}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(executable_path="/Users/edwardcox/chromedriver/chromedriver",
                          options=options)
driver.minimize_window()
class SongScraper:
    def __init__(self):
        self.song_file = open("songTitles.txt",'r')
        self.wait = WebDriverWait(webdriver, 10)
        
    def save_song(self):
        while True:
            song = self.song_file.readline()
            print(song)
            if song is None: break
            try: 
                url = self.search_song(song)
                self.download_song(url)
            except:
                print("an exception occurred, skipping song: ",song)
    
    def search_song(self, song_name):
        query = song_name.replace(" ", "+")
        yt_query = "https://www.youtube.com/results?search_query=" + query
        driver.get(yt_query)
        time.sleep(3)
        
        thumbnail = driver.find_element_by_xpath("//a[@class='yt-simple-endpoint style-scope ytd-video-renderer']")
        thumbnail.click()
        time.sleep(3)
        yt_url = driver.current_url
        return yt_url
        
    def download_song(self, song_link):
        driver.get("https://ytmp3.cc/en13/")
        time.sleep(3)
        textinput = driver.find_element_by_xpath("//input[@name = 'video']")
        textinput.send_keys(song_link)
        submitBtn = driver.find_element_by_xpath("//input[@value = 'Convert']")
        submitBtn.click()
        time.sleep(25)
        downloadBtn = driver.find_element_by_xpath("/html/body/div[@id='content']/div[@id='converter_wrapper']/div[@id='converter']/div[@id='buttons']/a[1]")
        downloadBtn.click()
        time.sleep(5)
        
        
#if __name__ == "__main__":
#    ss = SongScraper()
#    ss.save_song()
