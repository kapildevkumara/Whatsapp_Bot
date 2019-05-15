from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import threading

def encrypt_decrypt(key):
	key_list = list(key)
	encryp_decryp_key = ""
	for i in key_list:
		if(ord(i)>=65 and ord(i)<=90 ):
			i = chr(65+90-ord(i))
		elif(ord(i)>=97 and ord(i)<=122 ):
			i = chr(122+97-ord(i))		
		encryp_decryp_key = encryp_decryp_key + i 
	return encryp_decryp_key

def send(driver):
	while(1):
		try:
			tx_key = input()
			if (ord(list(tx_key)[0]) == 27):
				break

			message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
			encryp_key = encrypt_decrypt(tx_key)
			# encryp_key = tx_key	:	Uncomment this if you Don't Want To Use Personal Encryption
			message.send_keys(encryp_key)
			sendbutton = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')[0]
			sendbutton.click()

		except:
			print("Cannot Send Message. So exiting")
			break

def chat(driver):
	try:
		target_chat = input("Chat Name ??? ")
		if (ord(list(target_chat)[0]) == 27):
			driver.close()
			return

		target = '"' + target_chat + '"'
		group_title = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(@title,' + target + ')]' )))
		group_title.click()

	except:
		print("Could not Find the Chat")
		return

	else:
		value = 10;
		tx = threading.Thread(target=send, args=(driver,))
		tx.start()
		while(1):
			try:
				msg_old = driver.find_elements_by_xpath('//div[contains(@class,"copyable-text")]')
				inbox = driver.find_elements_by_xpath("//span[@class='selectable-text invisible-space copyable-text']")
				if (value>2):
					for i in range(len(inbox)):
						rx_key = inbox[i].text
						decryp_key = encrypt_decrypt(rx_key)
						# decryp_key = rx_key	:	Uncomment this if you Don't Want To Use Personal Encryption
						print("From : ", msg_old[i].get_attribute("data-pre-plain-text"), "in", target_chat, "is : ", decryp_key)

				elif(value==2):
					rx_key = inbox[len(inbox) - 1].text
					decryp_key = encrypt_decrypt(rx_key)
					print("From : ", msg_old[len(inbox) - 1].get_attribute("data-pre-plain-text"), "with", target, "is : ", decryp_key)

				sleep(1)
				msg_new =  driver.find_elements_by_xpath('//div[contains(@class,"copyable-text")]')

				if(msg_new != msg_old):
					value = 2
				else:
					value = 1

			except:
				print("Closing Chat")
				return 0

			if(not tx.isAlive()):
				print("Chat Quit")
				return 1
				break

if __name__ == "__main__":
	try:
		driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
		driver.get("https://web.whatsapp.com/")
		wait = WebDriverWait(driver, 600)
		status = 1

	except:
		print("Could Not Open Whatsapp Web")

	else:
		while(status):
			try:
				status = chat(driver)

			except:
				print("Closing Whatsapp")
				driver.close()
				break
