ROOT_URL = "https://api.iextrading.com"
FEED_URL = ROOT_URL + "/1.0/tops/last"
FULL_URL = FEED_URL + "?symbols="
YAHOO_URL = "https://finance.yahoo.com/lookup"
ARGUMENTS = [ "--headless", "--window-size=1920x1080"]
PRICE_locator = '//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]'
SEARCH_INPUT_locator = "#yfin-usr-qry"
SEARCH_BUTTON_locator="#search-button"

