# -*- coding: utf-8 -*-
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import easygui
import json
import requests

driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 1000)

def selectContact(contact):
	#print contact
	#x_arg = '//span[contains(@title,' + contact + ')]'
	#print x_arg
	#group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
	#print ("Wait for few seconds")
	#group_title.click()
	
	x_search = '//html/body/div[1]/div/div/div[3]/div/div[1]/div/label/input'
	
	caixa_de_pesquisa = driver.find_element_by_xpath(x_search)
	caixa_de_pesquisa.clear()
	caixa_de_pesquisa.send_keys(contact.replace('"',""))
	time.sleep(3)
	# Seleciona o contato
	contato = driver.find_element_by_xpath("//span[@title = '{}']".format(contact.replace('"',"")))
	# Entra na conversa
	contato.click()
	time.sleep(3)

def sendMessage(contact,msg):
	selectContact(contact)
	
	#locate message form by_xpath
	message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
	time.sleep(3)


	# send_keys() to simulate key strokes
	message.send_keys(msg)

	sendbutton = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')[0]

	sendbutton.click()
	
def sendImage(contact):
	file_path = "/Users/jonasmendesferreira/Documents/imagens/photo5775001477490780700.jpg"
	selectContact(contact)
	driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span').click()
	element = driver.find_element_by_xpath('//html/body/div[1]/div/div/div[4]/div/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button/input')
	element.send_keys(file_path)
	time.sleep(1)
	driver.find_element_by_xpath('//html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div').click()
	
	time.sleep(3)

def readMessages():
	contacts = driver.find_elements_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div/div')
	#contacts = element.find_elements_by_css_selector("")
	##pane-side > div:nth-child(1) > div > div > div:nth-child(3) > div > div > div._2WP9Q > div.KgevS > div._3H4MS > span > span
	#"div > div > div._2WP9Q > div.KgevS > div._3H4MS > span > span"
	#print len(contacts)
	list_contacts = []
	for ct in contacts:
		name = ct.find_element_by_css_selector("div > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span > span")
		cont = '"{}"'.format(name.text)
		list_contacts.append(cont)
		
	for cont in list_contacts:
		selectContact(cont)
		try:
			messageArea = driver.find_element_by_css_selector(".copyable-area")
			messages = messageArea.find_elements_by_css_selector("div.message-in, div.message-out")
			print "{} contem {} mensagens".format(cont,len(messages))
		except Exception as e:
			print e
		
	driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[1]/div/button').click()

ans = easygui.ynbox('O QR Code foi scanneado', 'Atenção', ('Sim', 'Não'))
if ans == True:
	time.sleep(10)
	
	while True:
		try:
			print "Buscando Mensagens"
			response = requests.get("http://vps4782.publiccloud.com.br/send/index.php")
			json_data = json.loads(response.text)
			for user in json_data:
				time.sleep(2)
				target = '"{}"'.format(user['contato'])
				string = user['mensagem']
				sendMessage(target,string)
				sendImage(target)
				requests.get("http://vps4782.publiccloud.com.br/send/index.php?action=saveStatus&id={}&status=2".format(user['id']))
			readMessages()
			print "Aguardando 10 Segundos"
			time.sleep(10);
		except (KeyboardInterrupt, EOFError) as err: 
			print "Finalizando Programa"
			exit(0);
			break;
		except Exception as e:
			if len(json_data):
				requests.get("http://vps4782.publiccloud.com.br/send/index.php?action=saveStatus&id={}&status=3".format(user['id']))
				
			print "Houve um erro não esperado"
			print e
			print "Aguardando 10 Segundos"
			time.sleep(10);	
			

driver.close();
