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

def sendMessage(contact,msg):
	#print contact
	#x_arg = '//span[contains(@title,' + contact + ')]'
	#print x_arg
	
	#group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))

	#print ("Wait for few seconds")
	#group_title.click()
	
	x_search = '//html/body/div[1]/div/div/div[3]/div/div[1]/div/label/input'
	
	caixa_de_pesquisa = driver.find_element_by_xpath(x_search)
	caixa_de_pesquisa.send_keys(contact.replace('"',""))
	time.sleep(2)
	# Seleciona o contato
	contato = driver.find_element_by_xpath("//span[@title = '{}']".format(contact.replace('"',"")))
	# Entra na conversa
	contato.click()
	

	#locate message form by_xpath
	message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
	time.sleep(3)


	# send_keys() to simulate key strokes
	message.send_keys(msg)

	sendbutton = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')[0]

	sendbutton.click()

ans = easygui.ynbox('O telefone foi conectado com sucesso?', 'Atenção', ('Sim', 'Não'))
if ans == True:
	time.sleep(10)
	
	while True:
		print "Buscando Mensagens"
		response = requests.get("http://vps4782.publiccloud.com.br/send/index.php")
		json_data = json.loads(response.text)
		for user in json_data:
			time.sleep(2)
			target = '"{}"'.format(user['contato'])
			string = user['mensagem']
			sendMessage(target,string)
			
		print "Aguardando 10 Segundos"
		time.sleep(10);

driver.close();
