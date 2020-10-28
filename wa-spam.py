from splinter import Browser
from time import sleep
import argparse
from selenium.webdriver.common.keys import Keys

parser = argparse.ArgumentParser(description="Spam your friends or enemies on whatsapp!")
parser.add_argument('chat_name', type=str, help="Name of the chat you want to spam")
parser.add_argument('--msg', type=str, help="Message to be sent")
parser.add_argument('count', type=int, help="Number of messages to be sent")
parser.add_argument('-n', action='store_true', help="Explicitly set the network proxy type to: no proxy")
parser.add_argument('--waittime', type=int, default=10, help="Change the time that the application waits for you to login. Default: 10 seconds")
parser.add_argument('--file', type=str, help="Send text from a file")

args = parser.parse_args()

if(args.file == None and args.msg == None):
	print("Please enter either a message or file with the message")
	exit(0)

print("You will have 10 secs to scan the QR code.")
input("Press enter when you are ready with the whatsapp scanner on your phone!")

browser = Browser()

if(args.n):

	browser.visit("about:config")
	script = """
	var prefs = Components.classes["@mozilla.org/preferences-service;1"]
	.getService(Components.interfaces.nsIPrefBranch);

	prefs.setIntPref("network.proxy.type", 0);
	"""
	browser.execute_script(script.format("ProxyIP", "PORT"))


url = "https://web.whatsapp.com/"
browser.visit(url)

# time to login to whatsapp using QR code
sleep(args.waittime)

# find the chat
chat_search = browser.find_by_xpath("/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]").first
chat_search.type(args.chat_name)

# press the chat
browser.find_by_xpath('//*[contains(@title, "'+args.chat_name+'")]').click()

confirmation = input("is this the chat you want to send the messages to?\nEnter yes or no:")
if(confirmation == 'yes'):

	# send message
	if(args.file != None):
		f = open(args.file, "r")
		line = f.readline()

		active_web_element = browser.driver.switch_to_active_element()
		for i in range(args.count):
			f = open(args.file, "r")
			line = f.readline()
			while line:
				chatbox = browser.find_by_xpath("/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]").first
				line = line.strip('\n')
				chatbox.type(line)
				active_web_element.send_keys(Keys.CONTROL + Keys.ENTER)
				line = f.readline()
			send_button = browser.find_by_xpath("/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[3]/button").first.click()
			f.seek(0, 0)

		f.close()

	else:
		msg = args.msg
		for i in range(args.count):
			chatbox = browser.find_by_xpath("/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]").first
			chatbox.type(msg)
			send_button = browser.find_by_xpath("/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[3]/button").first.click()


#logout from whatsapp
browser.find_by_xpath("/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[3]/div").first.click()
browser.find_by_xpath("/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[3]/span/div/ul/li[7]/div").first.click()

#close window
browser.quit()