# -*- coding: utf-8 -*-

from os import chdir, remove, urandom
from os.path import dirname, abspath
from sys import platform, exit
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from subprocess import call
from platform import machine
from binascii import hexlify
from PIL import Image


def fullpage_screenshot(driver, file):
	total_width = driver.execute_script("return document.body.offsetWidth")
	total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
	viewport_width = driver.execute_script("return document.body.clientWidth")
	viewport_height = driver.execute_script("return window.innerHeight")
	rectangles = []

	i = 0
	while i < total_height:
		ii = 0
		top_height = i + viewport_height

		if top_height > total_height:
			top_height = total_height

		while ii < total_width:
			top_width = ii + viewport_width

			if top_width > total_width:
				top_width = total_width

			rectangles.append((ii, i, top_width, top_height))

			ii = ii + viewport_width

		i = i + viewport_height

	stitched_image = Image.new('RGB', (total_width, total_height))
	previous = None
	part = 0

	for rectangle in rectangles:
		if previous is not None:
			driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
			sleep(0.2)

		file_name = "part_{0}.png".format(part)

		driver.get_screenshot_as_file(file_name)
		screenshot = Image.open(file_name)

		if rectangle[1] + viewport_height > total_height:
			offset = (rectangle[0], total_height - viewport_height)
		else:
			offset = (rectangle[0], rectangle[1])

		stitched_image.paste(screenshot, offset)

		del screenshot
		remove(file_name)
		part = part + 1
		previous = rectangle

	stitched_image.save(file)
	return True


def startup():
	try:
		if platform.startswith('win'):
			call('taskkill /F /IM chrome.exe', shell=True)

		elif platform.startswith('darwin'):
			call('pkill -a -i "Google Chrome"', shell=True)

		elif platform.startswith('linux'):
			call('kill -9 `ps -A |grep chrome| cut -d "?" -f1`', shell=True)

		else:
			print("Unknown system.")
			exit(0)

		opts = Options()
		opts.add_argument("user-data-dir=Chrome")

		if platform.startswith('win'):
			driver = webdriver.Chrome(executable_path="driver/win/chromedriver.exe", chrome_options=opts)

		elif platform.startswith('darwin'):
			driver = webdriver.Chrome(executable_path="driver/darwin/chromedriver", chrome_options=opts)

		elif platform.startswith('linux'):
			if machine().endswith('64'):
				driver = webdriver.Chrome(executable_path="driver/linux/x64/chromedriver", chrome_options=opts)

			else:
				driver = webdriver.Chrome(executable_path="driver/linux/x86/chromedriver", chrome_options=opts)

		else:
			print("Unknown system.")
			exit(0)

		driver.get('https://foxford.ru/user/registration/')
		driver.execute_script("return window.open('https://vk.com');")

		input("Login to foxford (or get homework URLs). When you are done, press Ctrl + C to continue.")

	except KeyboardInterrupt:
		main()


def main():
	while True:
		try:
			if platform.startswith('win'):
				call('taskkill /F /IM chrome.exe', shell=True)

			elif platform.startswith('darwin'):
				call('pkill -a -i "Google Chrome"', shell=True)

			elif platform.startswith('linux'):
				call('kill -9 `ps -A |grep chrome| cut -d "?" -f1`', shell=True)

			else:
				print("Unknown system.")
				exit(0)

			url = str(input("\nHomework url: "))
			opts = Options()
			opts.add_argument("user-data-dir=Chrome")

			if platform.startswith('win'):
				driver = webdriver.Chrome(executable_path="driver/win/chromedriver.exe", chrome_options=opts)

			elif platform.startswith('darwin'):
				driver = webdriver.Chrome(executable_path="driver/darwin/chromedriver", chrome_options=opts)

			elif platform.startswith('linux'):
				if machine().endswith('64'):
					driver = webdriver.Chrome(executable_path="driver/linux/x64/chromedriver", chrome_options=opts)

				else:
					driver = webdriver.Chrome(executable_path="driver/linux/x86/chromedriver", chrome_options=opts)

			else:
				print("Unknown system.")
				exit(0)

			driver.set_window_size(1920, 1080)

			driver.get(url)

			driver.execute_script("document.getElementById('headerComponent').setAttribute('style', 'display:none;');")

			string = str(hexlify(urandom(3))).strip('b').replace("'", "")

			fullpage_screenshot(driver, "homework_" + string + ".png")

			input("Homework saved as " + "'homework_" + string + ".png'." + " To capture another homework press Enter. To exit - Ctrl + C.")

		except KeyboardInterrupt:
			print("\n")
			exit(0)


if __name__ == "__main__":
	chdir(dirname(abspath(__file__)))

	startup()
