import random
from time import sleep
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as soup

# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
driver = webdriver.Chrome('./chromedriver.exe')

# Voy a la pagina que requiero
driver.get('https://www.instagram.com/p/B166OkVBPJR/')


# Busco el boton para cargar mas informacion
boton = driver.find_element_by_xpath('//button[@class="dCJp8 afkep"]')
for i in range(3):
    try:
        boton.click()
        sleep(random.uniform(8.0,10.0))
        boton = driver.find_element_by_xpath('//button[@class="dCJp8 afkep"]')
    except:
        break

urlPost = driver.current_url

pageWebContent = soup(driver.page_source, "lxml")
caption = pageWebContent.findAll("div",{"class":"C4VMK"})

for i in caption :
    mensaje = i.findAll("span",{"class":""})
    MessageCaption = mensaje[0].get_text()
    break

listUsername = []
listfecha = []
listlikesComment = []
listIdFatherComment = []
listIdChildComment = []
listcaption = []
listPost = []
commentsO = driver.find_elements_by_xpath('//ul[@class="Mr508"]')
comments = pageWebContent.findAll("ul",{"class":"Mr508"})
for comment in comments:
    # Por cada comentario encuentro los demas datos
    User = comment.div.li.div.div.findAll("div",{"class":"C4VMK"})
    for u in User:
        Username = (u.findAll("a"))[0].get_text()
        listUsername.append(Username)
for comment1 in commentsO:
    fecha = comment1.find_element_by_xpath('.//time[@class="FH9sR Nzb55"]').text
    likesComment = comment1.find_element_by_xpath('.//button[@class="FH9sR"]').text  #respuesta: 1 like y Reply  debo filtrarlo
    IdFatherComment = comment1.find_element_by_xpath('.//span[@class]').text
    IdChildComment = comment1.find_element_by_xpath('.//span[@class]').text #no estoy secure
    
    listfecha.append(fecha)
    if not(likesComment == "Reply"):
        listlikesComment.append(likesComment)
    else:
       listlikesComment.append("0 like") 
    listIdFatherComment.append(IdFatherComment)
    listIdChildComment.append(IdChildComment)
    listcaption.append(MessageCaption)
    listPost.append(urlPost)
df = pd.DataFrame({'Post':listPost,
                    'Caption':listcaption,
                    'date':listfecha,
                    'likeComment':listlikesComment,
                    'IdFatherComment':listIdFatherComment,
                    'IdChildComment':listIdChildComment,
                    'Username':listUsername})
sleep(10)
df.to_csv('ScrapingInstagram.csv', index=False,header = True, sep='\t')