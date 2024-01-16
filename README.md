# Course Availability Notifier

## Introduction

The Course Availability Notifier is a Python tool designed to periodically check university course statuses and provide a notification if a course status changes from 'Full' to 'Not Full'. This README offers an explanation of the tool, usage guidelines, and details the accompanying files required for the script to operate.

## Project Structure

This project includes several key files:
- `notifier.py`: The main Python script that checks course availability and sends notifications.
- `courses.txt`: A text file containing one course code per line for the courses you wish to monitor.
- `courseslist.txt`: A text file containing numbered full names of each course, corresponding to the codes in `courses.txt`.
- `geckodriver.exe`: The Firefox WebDriver executable for use with Selenium.
- `NotFull.mp3`: An audio file that is played when a course's status updates to 'Not Full'.

## Prerequisites

To run the Course Availability Notifier, ensure you have the following installed:
- Python 3.x
- Selenium Python package (`pip install selenium`)
- BeautifulSoup Python package (`pip install beautifulsoup4`)
- playsound Python package (`pip install playsound`)
- colorama Python package (`pip install colorama`)
- termcolor Python package (`pip install termcolor`)
- Mozilla Firefox web browser

## Usage

1. Make sure all prerequisites are installed.
2. Update `courses.txt` with the course codes you are interested in monitoring.
3. Ensure `courseslist.txt` has a numbered list of full course names corresponding to `courses.txt`.
4. Place `geckodriver.exe` in the same directory as the `notifier.py` script.
5. Verify that `NotFull.mp3` is within the project directory if you wish to receive audio alerts.
6. Execute the notifier script using: ```python notifier.py```
7. Respond to the terminal prompts to select and add courses you wish to track.

## Customization

The script may require updates to XPath locations and CSS selectors if changes appear on the course scheduling website. Refer to the Selenium documentation for guidance on element identification.

## Additional Notes

- The script's default behavior includes a 15-second sleep interval between status checks. Modify the `statsupdater()` function in the script to change this interval.
- Though the script uses `geckodriver` for Firefox, it can be adapted to Chrome or other browsers by employing the appropriate WebDriver and adjusting the Selenium configuration code.
- The colorama and termcolor libraries are used to display terminal output in various colors for improved readability.

## Troubleshooting

- In case of issues with `geckodriver`, confirm its presence in the script's directory and ensure it has proper execution permissions.
- Check that all required Python packages from the prerequisites list are installed.
- Browser and Selenium compatibility can occasionally cause issues. Updating both Selenium and Firefox to their latest versions may resolve some problems.

## Contributions

 Feel free to fork the repository, implement your enhancements, and submit pull requests.
