from web_driver_init import driver


class Filter_page_elements:

    def by_year_dropdown():
        return driver.find_element_by_xpath("//b[text()='By year']")

    def by_year_2017_dd_value():
        return driver.find_element_by_xpath("//span[@data-year='year2017']")

    def displayed_articles():
        return driver.find_elements_by_xpath("//div[@class='explor ' and @style='display: block;']//h4/a")

    def reset_filters_link():
        return driver.find_element_by_xpath("//div[@id='filter6']")


class Actions:

    def expand_by_year_dropdown():
        Filter_page_elements.by_year_dropdown().click()

    def click_by_2017():
        Filter_page_elements.by_year_2017_dd_value().click()

    def reset_filters():
        Filter_page_elements.reset_filters_link().click()