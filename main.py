import time
import random
import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scroll_down(driver, times):
    if times <= 0:
        return
    driver.execute_script("window.scrollBy(0, 250)")
    time.sleep(2)
    scroll_down(driver, times - 1)


def click_random_visible_element_in_list(driver, class_name):
    list_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_name)))

    visible_elements = [element for element in list_elements if element.is_displayed()]

    if not visible_elements:
        print("No visible elements")
        return None

    random_visible_element = random.choice(visible_elements)

    random_visible_element.click()


def take_and_save_screenshot(screen_name, timeout, driver):
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    if not os.path.exists(desktop_path):
        os.makedirs(desktop_path)

    save_path = os.path.join(desktop_path, screen_name + '.png')

    time.sleep(timeout)
    screenshot = driver.get_screenshot_as_png()
    with open(save_path, 'wb') as file:
        file.write(screenshot)


@pytest.fixture(scope="module")
def setup():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('mobileEmulation', {'deviceName': 'iPhone X'})  # Change deviceName as needed
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_wap(setup):
    driver = setup
    wait = WebDriverWait(driver, 30)
    driver.get("https://www.twitch.tv/")
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, ".ScCoreButton-sc-ocjdkq-0.ScCoreButtonPrimary-sc-ocjdkq-1.lnaTdO.eQdnrM"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Search']"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ScInputBase-sc-vu7u7d-0.ScInput-sc-19xfhag-0.gDMCvN.hLfCn"
                                                            ".InjectLayout-sc-1i43xsx-0.fsdMgG.tw-input.tw-input--"
                                                            "large"))).send_keys("StarCraft")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'StarCraft II')]"))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".CoreText-sc-1txzju1-0.fdegKV")))

    scroll_down(driver, 2)

    click_random_visible_element_in_list(driver, "sc-f7ad2bad-0.kBEPNi")

    # wait for follow button to be clickable
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ScCoreButton-sc-ocjdkq-0.ScCoreButtonPrimary-sc-ocjdkq-1.lnaTdO.eQdnrM")))

    take_and_save_screenshot("example_001", 3, driver)
