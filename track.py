from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time, sys

def time_format(time_sec):
	time = time_sec
	day = time // (24 * 3600)
	time = time % (24 * 3600)
	hour = time // 3600
	time %= 3600
	minutes = time // 60
	time %= 60
	seconds = time
	print("Online for : ", day, " days ", hour, " hours ", minutes, " minutes ", int(seconds), " seconds ")
	return 0
	
if __name__ == "__main__":
	try:
		driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
		driver.get("https://web.whatsapp.com/")
		wait = WebDriverWait(driver, 600)

	except:
		print("Could Not Open Whatsapp Web")

	else:
		target = input("Chat Name ?? ")
		if (ord(list(target)[0]) == 27):
			exit(0)

		target = '"' + target + '"'
		key = 2
		time_online = 0
		group_title = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(@title,' + target + ')]' )))
		group_title.click()

		while(1):
			try: 
				time.sleep(2)

			except KeyboardInterrupt:
				print("\nEnd of Tracking") 
				exit(0)

			else:
				try: 
					# description = driver.find_element_by_class_name('O90ur')	# Previously used Whatsapp Class Name
					description = driver.find_element_by_class_name('_315-i')
					online = description.text

					if(online == "online"):
						if(key):
							print("\nOnline at : " + time.asctime( time.localtime(time.time()) ))
							#print("Online")
							time_online =  time.time()
							key = 0

					elif(online.find('last seen') != -1):
						if(abs(1 - key) > 0):
							print("Offline at : " + time.asctime( time.localtime(time.time()) )) 
							if(key == 0):
								time_format(time.time() - time_online)
							print("...........")
							key = 1

				except NoSuchElementException as exception:
					if(key == 0):
						print("Offline at : " + time.asctime( time.localtime(time.time()) )) 
						#print("No such Element")
						time_format(time.time() - time_online)
						print("...........")							
						key = 1
						pass

				except:
					print("Error!")
		
