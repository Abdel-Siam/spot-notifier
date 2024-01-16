from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import re
from playsound import playsound
from colorama import init
from termcolor import colored
import time
import datetime

# Initialize colorama for colored CLI output
init()

# Lists to store course numbers and identifiers
total_coursenumb = []
total_coursenbr = []

# URL of the website to scrape
url = 'https://studentservices.uwo.ca/secure/timetables/mastertt/ttindex.cfm'

# Setting up Selenium webdriver options
options = webdriver.FirefoxOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument('--no-sandbox')

# Initialize the WebDriver
driver = webdriver.Firefox(executable_path="geckodriver.exe", options=options)

# Read courses from 'courses.txt' and 'courseslist.txt' files assuming both files located in the same directory as this script
with open('courses.txt', 'r') as courses_file:
    course_list = [line.strip() for line in courses_file.readlines()]

with open('courseslist.txt', 'r') as courses_file_2:
    courseslist = [line.strip() for line in courses_file_2.readlines()]

# Function to print courses list
def listing():
    for course in courseslist:
        print(course)

# Function to fetch and process course information from the website
def courseinf(index):
    global page_source
    driver.get(url)
    subject_dropdown = Select(driver.find_element_by_xpath('//*[@id="inputSubject"]'))
    submit_button = driver.find_element_by_xpath('//*[@id="searchform"]/fieldset/div[4]/div/button')
    
    subject_dropdown.select_by_value(course_list[int(total_coursenumb[index])-1])
    submit_button.click()
    page_source = driver.page_source

# Function to parse the HTML and extract course status
def souping(course_nbr):
    global cleanedcourses
    soup = BeautifulSoup(page_source, 'lxml')
    cleanedcourses = []
    
    table_rows = soup.find_all('table', {'class': 'table table-striped'})
    for tr in table_rows:
        td = tr.find_all('td')
        row_data = [cell.get_text().strip() for cell in td]
        chunked_data = list(chunks(row_data, 15)) # We are assuming each row should be divided into chunks of 15
        for chunk in chunked_data:
            cleanedcourses.append(chunk)

# Function to update the statuses of the courses continuously
def statsupdater():
    while True:
        for index, course_nbr in enumerate(total_coursenbr):
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(current_time)
            courseinf(index)
            souping(course_nbr)
            
            for sections in cleanedcourses:
                for section in sections:
                    if section[2] == str(course_nbr):
                        course_status = section[14]
                        message = f"{course_list[int(total_coursenumb[index])-1]} section {section[0]} is {course_status}"
                        if course_status == 'Full':
                            print(colored(message, 'red'))
                        elif course_status == 'Not Full':
                            print(colored(message, 'green'))
                            playsound('NotFull.mp3')
                        else:
                            print('An unexpected issue occurred.')
            time.sleep(15)
        print("_______________________________________________________________________")

# Helper function to break list into chunks
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

# Function to add additional courses
def morecourses(number):
    for _ in range(number):
        coursenumb = input('Input the number of the subject you want:      ')
        coursenbr = input('What is the course/tutorial/lab nbr?       ')
        total_coursenumb.append(coursenumb)
        total_coursenbr.append(coursenbr)

# Main execution starts here
if __name__ == "__main__":
    listing()
    print('Above are numbers that correspond to each subject')
    total_coursenumb.append(input('Input the number of the subject you want:       '))
    total_coursenbr.append(input('What is the course/tutorial/lab nbr?      '))
    
    if input('Do you want to add another course? y/n        ').lower() == 'y':
        number_of_courses = int(input('How many more do you want?      '))
        morecourses(number_of_courses)
    
    statsupdater()