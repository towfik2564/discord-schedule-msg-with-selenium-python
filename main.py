
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from apscheduler.schedulers.background import BlockingScheduler
from time import sleep
import random

# collecting discord credentials from text file
with open('account.txt') as f:
    email = f.readline().strip()
    password = f.readline().strip()
    channel_link = f.readline().strip()
    message = f.readline().strip()
email = email
password = password

print(f'running script for discord id: {email}')

driver_options = Options()
arguments = [
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-blink-features=AutomationControlled'
]
experimental_options = {
    'excludeSwitches': ['enable-automation', 'enable-logging'],
    'prefs': {'profile.default_content_setting_values.notifications': 2}
}

for argument in arguments:
    driver_options.add_argument(argument)
for key, value in experimental_options.items():
    driver_options.add_experimental_option(key, value)

# initiating browser
driver = webdriver.Chrome(options=driver_options)

# loging into discord
driver.get('https://discord.com/login')
driver.find_element(By.NAME,'email').send_keys(email)
sleep(1)
driver.find_element(By.NAME,'password').send_keys(password)
sleep(1)
driver.find_element(By.CSS_SELECTOR,"[type=submit]").click()
sleep(10)
print('successfully logged in!')


# redirecting to specific channel after login
driver.get(channel_link)
print('redicting to channel...')
sleep(60)

# Creates a default Background Scheduler
sched = BlockingScheduler()
scheduled_time = 1

def send_msg():
    try:
        # finding chatbox and typing the message there
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME,'editor-H2NA06'))).send_keys(message, Keys.ENTER)
        scheduled_time = random.randrange(3, 5)
        print(f'[success] {scheduled_time}')
    except:
        driver.refresh()
        print("chatbox not found")     
send_msg()
sched.add_job(send_msg,'interval', minutes=scheduled_time)
sched.start()