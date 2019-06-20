from behave import *
import requests
import json
import re
import jsonpath_rw_ext as jp
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config.constants import *
from common import *
import math

_result = []
_url = ""
_method = ""

@given(u'the api service is for : "{endPoint}" stocks')
def step_impl(context, endPoint):
  global _url
  if endPoint == "SNAP,fb": 
    _url = FULL_URL + endPoint
  else:
    assert False, "endpoint url is not provided"

@when(u'the service method is "{method}"')
def step_impl(context,method):
  global _method
  if method == "": assert False, "endpoint method is not provided"
  _method = method

@then(u'the response code should be "{status}"')
def step_impl(context,status):
  response = requests.request(_method, _url)
  global _result
  _result =  response.json()
  archiveResponse.saveJson(str(_result))
  assert response.status_code is int(status)

@then(u'it should return the datafor "{num}" company')
def step_impl(context, num):
    totalNumber = len(_result)
    assert str(totalNumber) == str(num)

@then(u'verify required fields')
def step_impl(context):
    errors = []
    counter = 1
    for stock in _result:
        err = []
        if type(stock['symbol']) is None:
            err.append('stock in index ' + str(counter) +
                       ' dose not have symbol')
        if type(stock['price']) is None:
            err.append('stock in index ' + str(counter) +
                       ' dose not have price')
        counter += 1
        if err != []:
            errors.append(err)
    if errors != []:
        assert False, errors

@given(u'we have the data from the api')
def step_impl(context):
    assert _result is not None

@then(u'the UI should have the same data as the api')
def step_impl(context):
  errors = []
  counter = 1

  def floatDigits(f, n):
    return math.floor(f * 10 ** n) / 10 ** n

  for stock in _result:
    err = []
    browser = Common.chrome()
    browser.get(YAHOO_URL)
    browser.find_element(
      By.CSS_SELECTOR, SEARCH_INPUT_locator).send_keys(stock["symbol"])
    browser.find_element(By.CSS_SELECTOR, SEARCH_BUTTON_locator).click()
    WebDriverWait(browser, 10).until(
      EC.presence_of_element_located((By.XPATH, PRICE_locator)))
    arr = []
    for x in range(5):
      time.sleep(2)
      price = browser.find_element(By.XPATH, PRICE_locator).text
      arr.append(floatDigits(float(price), 2))
        
    if round(float(stock["price"]),2) not in arr:
      err.append(["The two prices is not equal for " + stock["symbol"],
        arr, round(float(stock["price"]),2)])

    browser.quit()
    if err != []:
      errors.append(err)
    counter += 1
  if errors != []:
    assert False, errors
