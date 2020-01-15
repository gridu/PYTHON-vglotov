from web_driver_init import driver
from page_steps import home_page_steps, filter_page_steps


# on Home page
driver.get("https://blog.griddynamics.com")
home_page_steps.Actions.close_subscription_footer()
home_page_steps.Actions.click_filter_link()

# on Filters page
filter_page_steps.Actions.expand_by_year_dropdown()
filter_page_steps.Actions.click_by_2017()
displayed_articles = filter_page_steps.Filter_page_elements.displayed_articles()
assert (displayed_articles.__sizeof__() > 1)
article_name_to_check = displayed_articles[0].text
filter_page_steps.Actions.reset_filters()

# on Home page
displayed_articles = home_page_steps.Home_page_elements.displayed_articles()
assert (displayed_articles.__sizeof__() > 1)
article_name_to_check2 = displayed_articles[0].text
assert (article_name_to_check != article_name_to_check2)

driver.close()


