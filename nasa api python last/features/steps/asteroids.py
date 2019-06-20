
from behave import *
import requests
import json
import re
import jsonpath_rw_ext as jp
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from config.constants import *
from common import *


# TODO: replace the next variables with an object of custom class
_url = ""
_method = ""
_result = None
_asteroids= []

@given(u'the api service is: "{endpoint}"')
def step_impl(context, endpoint):
  global _url

  if endpoint == "asteroids": 
    _url = SEARCH_ASTEROIDS
  else:
    assert False, "endpoint url is not provided"

@when(u'the service method is "{method}"')
def step_impl(context, method):
  global _method
  if method == "": assert False, "endpoint method is not provided"
  _method = method

@then(u'the response code should be "{status}"')
def step_impl(context,status):
  response = requests.request(_method, _url)
  global _result
  _result =  response.json()
  archiveResponse.saveJson(str(_result))
  global _asteroids
  _asteroids = jp.match("$.near_earth_objects.*.[*]", _result)

  assert response.status_code is int(status)

@then(u'"{field}" should match the total result')
def step_impl(context, field):
  totalNumber = len(_asteroids)

  assert totalNumber == _result.get(field)

@then(u'verify required fields')
def step_impl(context):
	errors = []
	counter = 1
	for asteroid in _asteroids:
		err = []

		if type(asteroid['id']) is None:
			err.append('asteroid in index ' + str(counter) + ' dose not have id')

		if type(asteroid['name']) is None:
			err.append('asteroid in index ' + str(counter) + ' dose not have name')

		if re.match(REGEX, asteroid["links"]["self"]) is False:
			err.append('asteroid in index ' + str(counter) + ' dose not have url')

		if type(asteroid["absolute_magnitude_h"]) != float:
			err.append('asteroid in index ' + str(counter) + ' dose not have absolute_magnitude_h')
		minDiameterInkilometers = asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_min"] 
		maxDiameterInkilometers = asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_max"]
		if minDiameterInkilometers > maxDiameterInkilometers :
			err.append(' asteroid in index ' + str(counter) + ' dose not have uncorect diameter')

		diameterFromKMetarsToMeters = round(asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_min"]*1000, 5)
		diameterInMeters = round(asteroid["estimated_diameter"]["meters"]["estimated_diameter_min"], 5)

		if  diameterFromKMetarsToMeters != diameterInMeters:
			err.append('asteroid in index ' + str(counter) + ' dose not have the same distance in m and km')

		if type(asteroid["is_potentially_hazardous_asteroid"]) != bool:
			err.append('asteroid in index ' + str(counter) + ' dose not have "is_potentially_hazardous_asteroid" proparty')

		counter += 1
		if err != []:
			errors.append(err)
	if errors != []:
		assert False, errors

@given(u'we have the data from the api')
def step_impl(context):
    assert _asteroids is not None

@then(u'the UI should have the same data as the api')
def step_impl(context):
	errors = []
	counter = 1
	for asteroid in _asteroids:
		asteroidFullData = requests.request("GET", asteroid["links"]["self"])
		asteroidFullData = asteroidFullData.json()
		err = []
		browser = Common.chrome()
		browser.get(asteroid["nasa_jpl_url"].replace("http://", "https://"))

		absolute_magnitude_h = browser.find_element(
			By.XPATH, ABSOLUTE_SELECTOR).text
		if (str(asteroid["absolute_magnitude_h"]) != str(absolute_magnitude_h)):
			err.append(['asteroid in the index of  ' + str(counter) +
									"  in the api array dose not have the same absolute_magnitude_h in UI", str(absolute_magnitude_h), str(asteroid["absolute_magnitude_h"])])

		SpkId = browser.find_element(By.XPATH, SPK_ID_SELECTOR).text
		if str(SpkId) != str(asteroid["id"]):
			err.append(['asteroid in the index of  ' + str(counter) +
									"  in the api array dose not have the same id in UI", SpkId, str(asteroid["id"])])

		eccentricity = browser.find_element(
			By.XPATH, ECCENTRICITY_SELECTOR).text
		if str(eccentricity) != str(asteroidFullData["orbital_data"]["eccentricity"]):
			err.append(['asteroid in the index of  ' + str(counter) +
									"  in the api array dose not have the same eccentricity in UI", str(eccentricity), str(asteroidFullData["orbital_data"]["eccentricity"])])

		semiMajorAxis = browser.find_element(
			By.XPATH, MAJOR_AXIS_SELECTOR).text
		if str(semiMajorAxis) != str(asteroidFullData["orbital_data"]["semi_major_axis"]):
			err.append(['asteroid in the index of  ' + str(counter) +
									"  in the api array dose not have the same semi_major_axis in UI", str(semiMajorAxis), str(asteroidFullData["orbital_data"]["semi_major_axis"])])

		perihelionDistance = browser.find_element(
			By.XPATH, PERIHELION_DISTANCE_SELECTOR).text
		if str(perihelionDistance) != str(asteroidFullData["orbital_data"]["perihelion_distance"]):
			err.append(['asteroid in the index of  ' + str(counter) +
									"  in the api array dose not have the same perihelion_distance in UI", str(perihelionDistance), str(asteroidFullData["orbital_data"]["perihelion_distance"])])

		inclination = browser.find_element(
			By.XPATH, INCLINATION_SELECTOR).text
		if str(inclination) != str(asteroidFullData["orbital_data"]["inclination"]):
			err.append(['asteroid in the index of  ' + str(counter) +
									"  in the api array dose not have the same inclination in UI", str(inclination), str(asteroidFullData["orbital_data"]["inclination"])])

		browser.quit()
		if err != []:
			errors.append(err)
		counter += 1

	if errors != []:
		assert False, errors
