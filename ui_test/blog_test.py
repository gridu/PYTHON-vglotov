from selenium import webdriver


driver = webdriver.Chrome()

# on Home page
driver.get("https://blog.griddynamics.com")
driver.find_element_by_xpath("//a[@id='closefoot']").click()
driver.find_element_by_xpath(".//a[contains(text(),'Filter')]").click()

# on Filters page
driver.find_element_by_xpath("//b[text()='By year']").click()
driver.find_element_by_xpath("//span[@data-year='year2017']").click()
displayed_articles = driver.find_elements_by_xpath("//div[@class='explor ' and @style='display: block;']//h4/a")
assert (displayed_articles.__sizeof__() > 1)
article_name_to_check = displayed_articles[0].text
driver.find_element_by_xpath("//div[@id='filter6']").click()

# # on Home page
displayed_articles = driver.find_elements_by_xpath("//div[@class='explor ' and @style='display: block;']//h4/a")
assert (displayed_articles.__sizeof__() > 1)
article_name_to_check2 = displayed_articles[0].text
assert (article_name_to_check != article_name_to_check2)

driver.close()


