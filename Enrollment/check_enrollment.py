#!/usr/bin/env python3
"""Check enrollment of my class."""

import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class ElementValueIsNot:
    def __init__(self, locator, value):
        self.locator = locator
        self.value = value

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        return element.text != self.value


def get_available_seats() -> str:
    """Check enrollment."""
    selenium_url = os.getenv("SELENIUM_SERVER_URL", "http://localhost:4444/wd/hub")

    options = webdriver.FirefoxOptions()
    with webdriver.Remote(command_executor=selenium_url, options=options) as driver:
        driver.get("https://form.jotform.com/243407365523152")

        iframe_id = "customFieldFrame_15"

        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.ID, iframe_id)))
        driver.switch_to.frame(iframe_id)

        locator = (
            By.XPATH,
            "//li[label[@for='inperson-classroom']]/span[@class='items-left']"
        )

        try:
            wait.until(ElementValueIsNot(locator, "25 left"))
            return driver.find_element(*locator).text
        except TimeoutException:
            print("Text did not change within the timeout period.")
            raise

if __name__ == "__main__":
    result = get_available_seats()
    outpath = Path(__file__).parent / "output/result.txt"
    outpath.write_text(result, encoding="utf-8")
