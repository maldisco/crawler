from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# A custom wait for WebDriverWait
# Will wait until search has found something
# Docs: https://selenium-python.readthedocs.io/waits.html 
class element_finished_searching(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if(element.get_attribute("href") == ""):
            return False
        else:
            return element

# Returns rating [0,5] and number of reviews from tripadvisor
# @param search_term - place being searched
def get_rating_reviews_from(search_term):
    TRIPADVISOR_URL = "https://www.tripadvisor.com.br"

    custom_options = webdriver.ChromeOptions()
    custom_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=custom_options)
    driver.get(TRIPADVISOR_URL)
    wait = WebDriverWait(driver, 10)

    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/div[1]/button'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="lithium-root"]/main/div[3]/div/div'))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="lithium-root"]/main/div[3]/div/div/div[2]/form/input[1]'))).send_keys(search_term)
    wait.until(element_finished_searching((By.XPATH, '//*[@id="typeahead_results"]/a[1]'))).click()
    rating = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="tab-data-qa-reviews-0"]/div/div[3]/span/div/div[1]/div[1]'))).text
    number_of_reviews = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="tab-data-qa-reviews-0"]/div/div[3]/span/div/div[1]/div[2]/span'))).text
    driver.quit()

    return rating, number_of_reviews

if __name__ == "__main__":
    rating, number_of_reviews = get_rating_reviews_from("Congresso Nacional - Brasília")
    print(f'''
    ## Resultado da coleta de dados ##
    Avaliação do local: {rating} de {number_of_reviews} avaliações.
    ''')