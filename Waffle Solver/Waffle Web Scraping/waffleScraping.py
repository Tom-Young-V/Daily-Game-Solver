from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def getGrid(tags, size):
	grid = []
	row = []
	for x, tag in enumerate(tags):
		tag = str(tag)
		tag = tag.split("'")
		letterInfo = tag[0][33:].split('"')[0]

		if "green" in letterInfo:
			row.append((letterInfo[0], 2))
		elif "yellow" in letterInfo:
			row.append((letterInfo[0], 1))
		else:
			row.append((letterInfo[0], 0))

		if size == "daily":
			if x in [5, 6, 13, 14]:
				row.append((" ", 3))

			if x in [4, 7, 12, 15, 20]:
				grid.append(row)
				row = []

		if size == "deluxe":
			if x in [7, 8, 9, 18, 19, 20, 29, 30, 31]:
				row.append((" ", 3))

			if x in [6, 10, 17, 21, 28, 32, 39]:
				grid.append(row)
				row = []

	return grid

# AAAAAAA
# A A A A
# AAAAAAA
# A A A A
# AAAAAAA
# A A A A
# AAAAAAA

def getTagsFromWeb(url):
	# Set up the Chrome options
	chrome_options = Options()
	chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)

	# Set up the ChromeDriver with the specified options
	driver = webdriver.Chrome(options=chrome_options)

	# Navigate to the website
	driver.get(url)

	# Wait for the dynamic element with class "tile" to be present (adjust the time based on your website's loading time)
	try:
		dynamic_element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.CLASS_NAME, "tile.draggable"))
		)

		# Get the page source after JavaScript has run
		html_source = driver.page_source

	finally:
		# Close the browser
		driver.quit()

	# Parse the HTML source using BeautifulSoup
	soup = BeautifulSoup(html_source, 'html.parser')

	# Find tags with the specified class and data attributes
	target_tags = soup.find_all('div', class_=lambda value: value and 'tile draggable' in value)

	return target_tags


def getDaily(printGet = False):
	target_tags = getTagsFromWeb("https://wafflegame.net/daily")

	if printGet:
		if target_tags:
			print("Found tiles")
		else:
			print("Failed")
			return False

	return getGrid(target_tags, "daily")


def getDeluxe(printGet = False):
	target_tags = getTagsFromWeb("https://wafflegame.net/deluxe")

	if printGet:
		if target_tags:
			print("Found tiles")
		else:
			print("Failed")
			return False

	return getGrid(target_tags, "deluxe")


if __name__ == "__main__":
	print(getDaily())
	print(getDeluxe())














