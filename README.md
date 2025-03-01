## Tokopedia Product Scraper

This Python script automates the scraping of product data from Tokopedia search results. It utilizes Selenium for browser automation and BeautifulSoup for HTML parsing, and pandas for data handling.

### Overview

The script navigates to Tokopedia, searches for "mesin antrian" (queue machine), and extracts product details like names, prices, sold counts, and store names from the first 10 pages of search results. The data is then saved to a CSV file.

### Key Features

* **Automated Browser Interaction:** Uses Selenium to control a Chrome browser, handling dynamic content loading and pagination.
* **Robust Element Location:** Employs multiple CSS selectors to identify crucial elements, enhancing resilience to website layout changes.
* **Lazy Loading Handling:** Implements scrolling to load all lazy-loaded product data.
* **Data Extraction:** Extracts product information using BeautifulSoup, targeting specific HTML classes.
* **CSV Output:** Stores scraped data in a structured CSV format using pandas.
* **Pagination Support:** Navigates through multiple search result pages.
* **Error Handling:** Includes basic error handling for timeouts and missing elements.

### How It Works

1.  **Initialization:**
    * Sets up a Chrome WebDriver instance with maximized window and logging disabled.
    * **Important:** The `executable_path` for `chromedriver.exe` needs to be updated to your local path.

2.  **Navigation and Search:**
    * Opens the Tokopedia homepage.
    * Waits for the page to fully load.
    * Locates the search input field using multiple CSS selectors.
    * Enters "mesin antrian" and submits the search.
    * Waits for search results to load.

3.  **Data Scraping Loop:**
    * Iterates through the first 10 search result pages.
    * Waits for the search results container to load.
    * Scrolls down to load all product items that load via lazy loading.
    * Parses the page's HTML using BeautifulSoup.
    * Extracts product details (name, price, sold, store name) from each product container.
    * Stores the data in a list of dictionaries.
    * Appends the data to a CSV file (`data_mesin_antrian.csv`).
    * Clicks the "Next Page" button.

4.  **Data Storage:**
    * Uses pandas to create a DataFrame from the scraped data.
    * Appends the DataFrame to the CSV file, creating headers if the file is new.

5.  **Termination:**
    * Closes the browser after scraping all pages.

### Usage

1.  **Prerequisites:**
    * Python 3.x
    * Chrome browser
    * ChromeDriver (download and place in a known directory)

2.  **Installation:**
    * Install required libraries: `pip install selenium beautifulsoup4 pandas`
    * Update the `executable_path` variable in the code to point to your ChromeDriver location.

3.  **Running the Script:**
    * Save the script as a `.py` file.
    * Run it from the command line: `python your_script_name.py`
    * The scraped data will be saved to `data_mesin_antrian.csv`.

### Important Considerations

* **ChromeDriver Path:** Ensure the `executable_path` is correct.
* **Website Changes:** Tokopedia's website structure may change, requiring updates to CSS selectors.
* **Rate Limiting:** Be mindful of Tokopedia's terms of service to avoid IP blocking. Add delays or use proxies if needed for larger scraping tasks.
* **Error Handling:** Expand error handling for production use.
* **Selector Stability:** Website html structures can change, so selector changes will be needed over time.
* **Pagination count:** The script is set to scrape 10 pages, this can be modified by changing the range in the for loop.
