import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class PlacesScraper:
    def __init__(
        self,
        headless=True,
        load_images=False,
        chromedriver_path="/usr/local/bin/chromedriver",
        window_size=(700, 900),
    ):
        options = webdriver.ChromeOptions()

        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")

        if not load_images:
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(
            executable_path=chromedriver_path, options=options
        )
        self.driver.set_window_size(*window_size)

    def get_nearby_places(
        self,
        query,
        latitude,
        longitude,
        timeout=10,
        max_results=100,
    ):
        assert max_results <= 120, "max_results should be <= 120"

        self.driver.get(
            f"https://www.google.com/maps/search/{query}/@{latitude},{longitude},17z"
        )
        time.sleep(1)

        places_card = []
        st = time.time()

        # scroll to bottom
        while True:
            if time.time() - st > timeout:
                break
            elif len(places_card) >= max_results:
                break

            places_card = self.driver.find_elements(By.CLASS_NAME, "bfdHYd")
            if len(places_card) > 0:
                for i in places_card[-1:]:
                    self.driver.execute_script("arguments[0].scrollIntoView();", i)
            else:
                time.sleep(1)

        # process the data
        if len(places_card) > 0:
            data = []
            for i in places_card:
                # find anchor tag in parent div using xpath
                place_url = i.find_element(By.XPATH, "..//a").get_property("href")
                text = i.find_element(By.XPATH, ".//div[4]").text

                # remove all the unicode characters and unwanted space
                text = re.sub(r"[^\x00-\x7f]", r"", text)
                text = re.sub(r" +", " ", text)

                # split text by new line and create a dictionary
                keys = ["name", "rating", "address", "timing"]
                item = dict(zip(keys, text.split("\n")))
                item.update({"url": place_url})
                data.append(item)
            return data

    def close(self):
        self.driver.close()

    def __del__(self):
        self.close()


if __name__ == "__main__":
    scraper = PlacesScraper(headless=True, load_images=False)
    latitude, longitude = (28.4914835, 77.3219736)
    data = scraper.get_nearby_places(latitude, longitude, search_query="cafe")
    print(data)
