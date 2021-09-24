import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time

driver = webdriver.Chrome('./chromedriver')
# https://chromedriver.chromium.org/downloads
# if there is driver issue go for the link form
# above and download the currect version and put in in the projects folder
driver.get(r"https://members.callloop.com/login")

file_path = r"C:"  # path to execle files
listName = "name"  # name of list
Password = 'pass'  # password to account
email = 'email@email.com'  # email of account
count_number_of_grope = 1  # what is the grope number you are
count_number_of_file = 1  # what is the upload file number you are
# you don't need to change number_of_files it is auto function
number_of_files = 0  # how many files in your folder
delay = 17  # normal wait for reload page
long_delay = 25  # longer wait time


# click button by its id
def click_button_id(id):
    try:
        button_element = driver.find_element_by_id(id)
        button_element.click()
    except TimeoutException:
        print("error didn't find the button")
        time.sleep(5)
        button_element = driver.find_element_by_id(id)
        button_element.click()


# click button by its name
def click_button_name(name):
    try:
        button_element = driver.find_element_by_name(name)
        button_element.click()
    except TimeoutException:
        print("error didn't find the button")
        time.sleep(5)
        button_element = driver.find_element_by_name(name)
        button_element.click()


# click button by its class name
def click_button_class(name):
    try:
        button_element = driver.find_element_by_class_name(name)
        button_element.click()
    except TimeoutException:
        print("error didn't find the button")
        time.sleep(5)
        button_element = driver.find_element_by_class_name(name)
        button_element.click()


# create new group of contacts
def create_new_group(grope_name):
    click_button_id("create_group")
    time.sleep(5)
    name_element = driver.find_element_by_id("Name")
    name_element.send_keys(grope_name)
    click_button_name("submit")


# upload a group of contacts
def upload_contacts(file_path):
    driver.get("https://members.callloop.com/subscribers/import/index")
    driver.find_element_by_id("fileupload").send_keys(file_path)
    driver.find_element_by_xpath(
        "//*[@id='forms']/table/tbody/tr[4]/td/span/div/div[2]/div").click()  # click on agree
    click_button_class("sm-button")
    click_button_class("sm-button")
    time.sleep(5)
    click_button_class("sm-button")


def wait_for_next_page(id_of_new_page_contnt, delay_of_refresh):
    try:
        from selenium.webdriver.support.wait import WebDriverWait

        WebDriverWait(driver, delay_of_refresh).until(
            lambda x: x.find_element_by_id(id_of_new_page_contnt))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")
        driver.refresh()
        time.sleep(15)
        driver.get("https://members.callloop.com")
        wait_for_next_page("create_group", delay)


path, dirs, files = next(os.walk(file_path))
number_of_files = len(files) + 2
print("number of file: " + str(number_of_files))
wait = WebDriverWait(driver, 600)
element = driver.find_element_by_id("email")
element.send_keys(email)
element = driver.find_element_by_id("password")
element.send_keys(Password)
click_button_id("submit")

# move to second page
wait_for_next_page("lists", delay)
el = driver.find_element_by_id('lists')
found_list = False
for option in el.find_elements_by_tag_name('option'):
    if option.text == (listName + str(count_number_of_grope)):  # (listName + str(count_number_of_grope)):
        option.click()
        found_list = True
        break
wait_for_next_page("lists_table", delay)
table_id = driver.find_element_by_id('lists_table')
rows = table_id.find_elements_by_tag_name("tr")  # get all of the rows in the table
word_len = rows[1].text[len(listName):].split(' ')[5]
if not found_list:
    create_new_group(listName + str(count_number_of_grope))
    word_len = 0
    print("new group")
count_number_of_grope += 1
wait_for_next_page("content", delay)
driver.get("https://members.callloop.com")
wait_for_next_page("create_group", delay)
for x in range((number_of_files - (count_number_of_file - 3))):
    print("the x is: " + str(x) + ", in: " + str((number_of_files - (count_number_of_file - 3))))
    print("number of people in the group: " + str(word_len))
    if int(word_len) > 16500:
        create_new_group(listName + str(count_number_of_grope))
        print("successfully created new group: " + listName + str(count_number_of_grope))
        count_number_of_grope += 1
        number_of_files += 1
    else:
        upload_contacts((
                file_path + r"\sheet" + str(count_number_of_file) + ".csv"))
        print("successfully upload contacts file number: " + str(count_number_of_file))
        count_number_of_file += 1
        wait_for_next_page("content", long_delay)
    driver.get("https://members.callloop.com")
    wait_for_next_page("lists_table", delay)
    table_id = driver.find_element_by_id('lists_table')
    rows = table_id.find_elements_by_tag_name("tr")  # get all of the rows in the table
    if (int(word_len) != 0) & (int(word_len) == int(rows[1].text[len(listName):].split(' ')[5])):
        print("error! no add contacts")
    word_len = rows[1].text[len(listName):].split(' ')[5]
