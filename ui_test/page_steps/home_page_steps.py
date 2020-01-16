from ui_test.web_driver_init import driver


class Home_page_elements:

    def close_footer_icon():
        return driver.find_element_by_xpath("//a[@id='closefoot']")

    def filter_link():
        return driver.find_element_by_xpath(".//a[contains(text(),'Filter')]")

    def displayed_articles():
        return driver.find_elements_by_xpath("//div[@class='explor ' and @style='display: block;']//h4/a")


class Actions:

    def close_subscription_footer():
        Home_page_elements.close_footer_icon().click()

    def click_filter_link():
        Home_page_elements.filter_link().click()
