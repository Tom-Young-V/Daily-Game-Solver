from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep

def getGrid(tags):
	if len(tags) == 21:
		size = "daily"
	else:
		size = "deluxe"

	testGrid = []
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
				row.append([" ", 3])

			if x in [4, 7, 12, 15, 20]:
				testGrid.append(row.copy())
				row = []
		else:
			if x in [7, 8, 9, 18, 19, 20, 29, 30, 31]:
				row.append([" ", 3])
			if x in [6, 10, 17, 21, 28, 32, 39]:
				testGrid.append(row.copy())
				row = []

	print(testGrid)
	return testGrid

# Set up the Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)

# Set up the ChromeDriver with the specified options
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the archive page
url = "https://wafflegame.net/archive"
driver.get(url)

if False:
	deluxe_button = WebDriverWait(driver, 10).until(
		EC.element_to_be_clickable((By.CSS_SELECTOR, '.tab.tab--deluxe'))
	)
	deluxe_button.click()

	ad_button = WebDriverWait(driver, 10).until(
		EC.element_to_be_clickable((By.CSS_SELECTOR, '.button.button--watch-ad'))
	)
	ad_button.click()
	sleep(20)

# Wait for the waffle elements to be present


waffle_elements = WebDriverWait(driver, 10).until(
	EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.item'))
)



# Iterate through each waffle
for waffle_element in waffle_elements:
	# Click on the waffle to trigger the HTML update

	waffle_element = WebDriverWait(driver, 10).until(
		EC.element_to_be_clickable((waffle_element))
	)

	waffle_element.click()

	# Wait for the updated HTML to load (you may need to adjust the time based on your website's loading time)
	driver.implicitly_wait(10)

	# Get the updated page source after JavaScript has run
	html_source = driver.page_source

	# Parse the HTML source using BeautifulSoup
	soup = BeautifulSoup(html_source, 'html.parser')

	# Find and extract the data from the updated HTML
	target_tags = soup.find_all('div', class_=lambda value: value and 'tile draggable' in value)

	# Process or print the found tags as needed
	getGrid(target_tags)

	# Click on the back arrow to return to the archive
	back_arrow_button = WebDriverWait(driver, 10).until(
		EC.element_to_be_clickable((By.CSS_SELECTOR, '.button--back'))
	)
	back_arrow_button.click()

# Close the browser
driver.quit()




