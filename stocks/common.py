from selenium.webdriver.chrome.options import Options
import os
from config.constants import ARGUMENTS
from selenium import webdriver

class Common:

  @classmethod
  def chrome(*args):
    chrome_options = Options()
    for arg in ARGUMENTS:
      chrome_options.add_argument(arg)
    browser = webdriver.Chrome(
      chrome_options=chrome_options)
    return browser

class archiveResponse :

  @classmethod
  def saveJson(context,json):
    try:
      if not os.path.exists("archive"):
        os.makedirs("archive")
      f= open("archive/stocks.py","w+")
    except:
      f= open("archive/stocks.py","w")
    f.write(json)
