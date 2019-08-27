from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import re
from playsound import playsound
from colorama import init
from termcolor import colored
import time
import datetime

init()
total_coursenumb = []
total_coursenbr = []

# site to work on
url = 'https://studentservices.uwo.ca/secure/timetables/mastertt/ttindex.cfm'

# opens chrome web drive in incognito (headless)
options = webdriver.FirefoxOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = webdriver.Firefox(executable_path="geckodriver.exe", options=options)


# importing courses from txt file (NOTE: SHOULD BE IN SAME DIRECTORY AS THE PY FILE)
courses_file = open('courses.txt', 'r')
courses_file_2 = open('courseslist.txt', 'r')
course_list = courses_file.readlines()
courseslist = courses_file_2.readlines()
list(courseslist)

# cleans the list from \n
for i in range(len(list(course_list))):
    course_list[i] = course_list[i].strip()
    courseslist[i] = courseslist[i].strip()

# main function
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]


def courseinf(i):
    global page_source
    driver.get(url)

    click_list = Select(driver.find_element_by_xpath('//*[@id="inputSubject"]'))
    submit = driver.find_element_by_xpath('//*[@id="searchform"]/fieldset/div[4]/div/button')

    click_list.select_by_value(course_list[int(total_coursenumb[i])-1])
    submit.click()

    page_source = driver.page_source


def listing():
    for i in range(len(courseslist)):
        print(courseslist[i])


def souping(nbr):
    global courses
    global cleanedcourses

    courses = []
    cleanedcourses = []
    soup = BeautifulSoup(page_source, 'lxml')

    table_rows = soup.find_all('table', {'class': 'table table-striped'})
    for tr in table_rows:
        td = tr.find_all('td')
        for i in range(len(td)):
            td[i] = td[i].get_text()
            td[i] = td[i].strip()
        to_change = ['\n', '\xa0', '\t']
        for char in range(len(to_change)):
            td[i] = re.sub(to_change[char], '', td[i])
        courses.append(td)
    for i in range(len(courses)):
        cleanedcourses.append(list(chunks(courses[i], 15)))


def statsupdater():
    while True:
        for t in range(len(total_coursenumb)):
            now = datetime.datetime.now()
            print(now.strftime("%Y-%m-%d %H:%M:%S"))
            courseinf(t)
            souping(total_coursenbr[t])
            for char in range(len(cleanedcourses)):
                for i in range(len(cleanedcourses[char])):
                    if cleanedcourses[char][i][2] == str(total_coursenbr[t]):
                        if cleanedcourses[char][i][14] == 'Full':
                            print(colored(str(course_list[int(total_coursenumb[t])-1])+ ' section '+ cleanedcourses[char][i][0]+ \
                                  ' is '+ cleanedcourses[char][i][14], 'red'))
                        elif cleanedcourses[char][i][14] == 'Not Full':
                            print(colored(str(course_list[int(total_coursenumb[t])-1])+ ' section '+ cleanedcourses[char][i][0]+ \
                                  ' is '+ cleanedcourses[char][i][14], 'green'))
                            playsound('NotFull.mp3')
                        else:
                            print('smth is wrong')
            time.sleep(15)
        print("_______________________________________________________________________")


def morecourses(number):
    for i in range(number):
        coursenumb = input('Input the number of the subject you want:     ')
        coursenbr = input('What is the course/tutorial/lab nbr?      ')
        total_coursenumb.append(coursenumb)
        total_coursenbr.append(coursenbr)


listing()
print('Above are numbers that correspond to each subject')
coursenumb = input('Input the number of the subject you want:       ')
coursenbr = input('What is the course/tutorial/lab nbr?     ')
total_coursenumb.append(coursenumb)
total_coursenbr.append(coursenbr)
more = input('Do you want to add another course? y/n        ')
if more == 'y':
    number = input('How many more do you want?      ')
    morecourses(int(number))
statsupdater()
