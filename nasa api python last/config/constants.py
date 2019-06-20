ROOT_URL = "http://www.neowsapp.com"
FEED_URL = ROOT_URL + "/rest/v1/feed"
SEARCH_ASTEROIDS = FEED_URL + "?start_date=2015-09-09&end_date=2015-09-09&detailed=false&api_key=DEMO_KEY"
REGEX = "https?://(?:[-\\w.]|(?:%%[\\da-fA-F]{2}))+"
ARGUMENTS = ["--headless", "--window-size=1920x1080"]
SPK_ID_SELECTOR = '//b[text()=\"SPK-ID:\"]/ancestor::font/following-sibling::font'
ABSOLUTE_SELECTOR = '//font[text()=\"absolute magnitude\"]/../../..//td[3]/font'
ECCENTRICITY_SELECTOR= "//a[text()=\"e\"]/ancestor::td/following-sibling::td[1]"
MAJOR_AXIS_SELECTOR =  "//a[text()=\"a\"]/ancestor::td/following-sibling::td[1]"
PERIHELION_DISTANCE_SELECTOR = "//a[text()=\"q\"]/ancestor::td/following-sibling::td[1]"
INCLINATION_SELECTOR = "//a[text()=\"i\"]/ancestor::td/following-sibling::td[1]"
