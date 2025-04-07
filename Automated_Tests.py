from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

file_path = "C:/Dani/UNI/8ми Семестър/VVPS/Kursova Rabota/index.html"

driver = webdriver.Chrome()
driver.get(file_path)

def wait():
    time.sleep(0.3)

def search_keyword(keyword, use_enter=False):
    input_box = driver.find_element(By.ID, "searchInput")
    input_box.clear()
    input_box.send_keys(keyword)
    if use_enter:
        input_box.send_keys(Keys.ENTER)
    else:
        driver.find_element(By.ID, "searchBtn").click()
    wait()

def count_results():
    return len(driver.find_elements(By.CSS_SELECTOR, "#results .product"))

# 1. Empty input
search_keyword("")
message = driver.find_element(By.ID, "results").text
assert "Please enter a keyword." in message

# 2. Single match
search_keyword("Gimbal")
assert count_results() == 1

# 3. Case-insensitive search
search_keyword("gImBaL")
assert count_results() == 1

# 4. Multiple matches
search_keyword("wireless")
assert count_results() == 3

# 5. No match
search_keyword("nonexistent")
message = driver.find_element(By.ID, "results").text
assert "No products found" in message

# 6. Clear button
driver.find_element(By.ID, "clearBtn").click()
wait()
assert driver.find_element(By.ID, "searchInput").get_attribute("value") == ""
assert driver.find_element(By.ID, "results").text == ""

# 7. Highlighting
search_keyword("mouse")
html = driver.find_element(By.ID, "results").get_attribute("innerHTML")
assert '<span class="highlight">mouse</span>' in html.lower()

# 8. Press Enter to search
search_keyword("camera", use_enter=True)
assert count_results() >= 1

print("✅ All tests passed!")

driver.quit()
