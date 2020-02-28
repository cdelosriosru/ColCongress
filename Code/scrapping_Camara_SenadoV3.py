### Web Scrapping Vataciones Congreso 2014-2018

# Install and load needed libraries
#pip install selenium

import time
from bs4 import BeautifulSoup
from selenium import webdriver
import re 
import pandas as pd

# I'll use the chrome driver

browser = webdriver.Chrome(executable_path=r"C:\Users\David\OneDrive\Documentos\chromedriver.exe")

#--------------------- Code start ------------------#

# --- Get all links to each votation --- #

### base URL to go trough pages
base_url = 'https://congresovisible.uniandes.edu.co/votaciones/#q=cuatrienio--2014-2018&page='

### how many pages are there? Let's check

url1 = base_url + '1'

browser.get(url1)
html = browser.page_source
time.sleep(2)
html1 = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
soup = BeautifulSoup(html1, "html.parser")

## Finding and extracting info from pages bar
pages_bar = re.search('<span class="paginas-disponibles">(.+)</span></p>', html1).group()

page = re.findall('<a>([0-9]+)</a>', pages_bar)

page = list(map(int, page))

last_page = max(page)

## A blank dataframe to fill with the bill's links
blank = {"Page": [], "page_link": [], "vote_link": []}
df = pd.DataFrame(blank)

## Visit al pages and extract bill's links
for i in range(1, last_page + 1):
#for i in range(1, 201):    
    
    # Print the page in console to keep track
    print("page", i)
    
    # define page to visit (base page + page number)
    url_p = base_url + str(i)
    
    # Extract html script from page
    browser.get(url_p)
    html = browser.page_source
    time.sleep(1)
    html_p = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(html1, "html.parser")
    
    # Extract table with Listado de Votaciones
    html_table = re.findall('<div class="container-double-list">(.+)</ul></div>', html_p)
    
    # Get links for each poll (addtional text to add)
    raw_links = re.findall('<a class=".+?" href="(.+?)"><span>', str(html_table))
    
    # Add text to get full links
    links = list(map(lambda orig_string: 'https://congresovisible.uniandes.edu.co' + orig_string, raw_links))
    
    page = i
    page_url = url_p
    
    # save on dataframe
    data0 = {"Page": page, "page_link": page_url , "vote_link": links}
    
    df0 = pd.DataFrame(data0)
    df = df.append(df0)
    

### --- extract results --- ###

# list of links (for loop)
link_list = list(df['vote_link'])

#--- DataFrames to fill ---#

# Overall info on project
blank1 = {"vote_link":[], "Nombre:": [], "Status":[], "Date": [], "Tipo" :[], "Camara":[], "Comision":[], "Votos": [],"Absenciones": [], "click":[]}
df1 = pd.DataFrame(blank1)

# Vote
blank2 = {"vote_link":[], "Congresista":[], "Partido:": [], "voto": [] }
df2 = pd.DataFrame(blank2)

# Abstentions
blank3 = {"vote_link":[], "Congresista":[], "Partido:": [], "voto": [] }
df3 = pd.DataFrame(blank3)

# Bill description
blank4 = {"vote_link":[], "bill_link" :[], "Bill_description":[], 'Autor' : [], 'party_autor': [], 'tags': []}
df4 = pd.DataFrame(blank4)

# ---- Extract info ---- #

# a counter to keep track
counter = 0

for i in link_list:

    counter = counter + 1
    print(counter)

    url = i
    browser.get(url)
    
    ## Open detail info
    ## Funny enough sometime if one has to try twice
    try:
        try:
            browser.find_element_by_xpath('//*[@id="container"]/div/div/div/div/div[3]/div/div/div[2]/div[1]/div[2]/div/a').click()
            clicker = 'OK'
        ## funny enough sometime one has to try twice 
        except:
            browser.find_element_by_xpath('//*[@id="container"]/div/div/div/div/div[3]/div/div/div[2]/div[1]/div[2]/div/a').click()    
            clicker = 'OK'
    except:
        print(url + "No clickable")
        clicker = 'NO'
        
    # extract inner HTML
    time.sleep(1)
    html = browser.page_source
    time.sleep(2)
    html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(html, "html.parser")
    
    # --------- let's fill the data sets -------- 
    
    
    # ----------------------- Overall Info ---------------------------
    ### Name 
    name = re.findall('<span class="name">(.+?)[\n]*[.|\S]*</span>', str(html))
    name = str(name).replace('&nbsp;', " ")
    
    if name == []:
        name = re.findall('<span class="name">([.+?[[\r\n]|\r\n]*.+?]+?)[\n]*[.|\S]*</span>', str(html))
        if name == []:
            new_html = str(html).rstrip('\r\n')
            name = re.findall('<span class="name">(.+?)*+</span>', str(new_html))

    ### total votes and abstentions
    t_votes = re.findall('\s+([0-9]+)\s+[^\n]\s+<span>Número de votos</span>', str(html))
    if t_votes == []:
        t_votes = [0]
    t_abstentions = re.findall('\s+([0-9]+)\s+[^\n]\s+<span>Abstenciones</span>', str(html))
    if t_abstentions == []:
        t_abstentions = [0]
    
    ### type of bill
    camera = re.findall('<li><h3>Cámara</h3>(.+?)</li>', str(html))
    camera = str(camera).replace('</p><p>',"-")
    camera = str(camera).replace('<p>',"")
    camera = str(camera).replace('</p>',"")
    camera = str(camera)
    
    ### Comsion 
    comision = re.findall('<li><h3>Comisión</h3>(.+?)</li>', str(html))
    comision = str(comision).replace('</p><p>',"-")
    comision = str(comision).replace('<p>',"")
    comision = str(comision).replace('</p>',"")
    comision = str(comision)
    
    ### Type of bill
    type_bill = re.findall('<li><h3>Tipo</h3>(.+?)</p><a.+</a></li>', str(html))
    type_bill = str(type_bill).replace('</p><p>',"-")
    type_bill = str(type_bill).replace('<p>',"")
    type_bill = str(type_bill).replace('</p>',"")
    type_bill = str(type_bill)
    
    ### Date
    date = re.findall('<li><h3>Fecha de Votación </h3>(.+?)</li>', str(html))
    date = str(date).replace('<p>',"")
    date = str(date).replace('</p>',"")
    date = str(date)
    
    ### Status
    status = re.findall('<div class="ico-(.+?)">', str(html))
    if status == []:
        status = re.findall('<div class=.ico-(.+?).>', str(html))
        if status == []:
            status = ['Unkown']
    
    # Ovell info on project
    data1 = {"vote_link": url, "Nombre:": name, "Status": status, "Date": date  ,"Tipo" : type_bill, "Camara": camera, "Comision": comision, "Votos": t_votes,"Absenciones": t_abstentions, "click": clicker}
    df01 = pd.DataFrame(data1)
    df1 = df1.append(df01)
    
    # ----------------------- Votes ---------------------------
    
    table_votos = re.findall('<table class="table4 table4-2" id="tabla-reporte-detallado">(.+?)</table>', str(html))
    line_table = re.findall('<tr.+?>(.+?)</tr>', str(table_votos))
    

    for i in range(1, len(line_table)):
        soup_vote = BeautifulSoup(str(line_table[i]))
        cols_vote = soup_vote.find_all('td')
        
        #### Extract names
        congressperson =  re.findall('<td>.+?>(.+?)</a></td>', str(cols_vote[0]))
        
        #### Extract party
        party =  re.findall('<td.+? href=.+?>(.+?)</a></td>', str(cols_vote[1]))
        
        #### Extract vote
        vote =  re.findall('<td>.*<a .+?>(.+?)</a>', str(cols_vote[2]))
        if vote == []:
            vote =  re.findall('<td>.+?<a .+?>(.+?)</a>', str(cols_vote[2]))
        
        data_vote0 = {"vote_link": url, "Nombre:": name, "Congresista": congressperson, "Partido:": party, "voto": vote }
        df02 = pd.DataFrame(data_vote0)
        df2 = df2.append(df02)
        
    
    # ----------------------- Abstention ---------------------------
    
    table_abs = re.findall('<table class="table4 table4-2" id="tabla-reporte-abstenciones">(.+?)</table>', str(html))
    line_abs = re.findall('<tr.+?>(.+?)</tr>', str(table_abs))
    

    for i in range(1, len(line_abs)):
        soup_abs = BeautifulSoup(str(line_abs[i]))
        cols_abs = soup_abs.find_all('td')
        
        #### Extract names
        congressperson =  re.findall('<td>.+?>(.+?)</a></td>', str(cols_abs[0]))
        
        #### Extract party
        party =  re.findall('<td.+? href=.+?>(.+?)</a></td>', str(cols_abs[1]))
        
        #### Extract vote
        vote =  str('Abstencion')
        
        data_abs0 = {"vote_link": url, "Nombre:": name, "Congresista": congressperson, "Partido:": party, "voto": vote }
        df03 = pd.DataFrame(data_abs0)
        df3 = df3.append(df03)
        
    # -------- Bill description --------#
    ## This is in a different page ##
    
    ### Get the link to the page w/ the description
    ### Bill description URL
    raw_link_bill = re.findall('<li><h3>Tipo</h3><p>.+?</p><a href=.(.+).>.+</a></li>', str(html))
    
    ### Add text to get full links
    link_bill = list(map(lambda orig_string: 'https://congresovisible.uniandes.edu.co' + orig_string, raw_link_bill))
    
    if link_bill == []:
        print('NO Description')
        bill_desc = ['NO Description']
        link_bill = ['Not availible']
        authors = ['NO Description']
        Party_author = ['NO Description']
        tags = ['NO Description']
    else:
        ### Go and extract Bill URL inner HTML
        url_bill = link_bill[0]
        browser.get(url_bill)
        html_bill = browser.page_source
        time.sleep(1)
        html_bill = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        soup_bill = BeautifulSoup(html, "html.parser")
        
        ### Get bill description
        bill_desc = re.findall('<h1 class="titular.">“(.+?)”</h1>', str(html_bill))
        if bill_desc == []:
            bill_desc = ['NO Description']
            
        ### get the Authors
        Authors_table = re.findall('<ul class="lista5">(.+?)</ul>', str(html_bill))
        authors = re.findall('<h3><a href=".*?">(.+?)</a></h3>', str(Authors_table))
        for i in range(1, len(authors) + 1 ):
            if 'Nombre del congresista' in str(authors):
                authors.remove('Nombre del congresista')
        if authors == []:
            authors = 'No reported'
        
        ## Get party
        Party_author = re.findall('<a href=./partidos.+?>(.+?)</a></p>', str(Authors_table))
        if Party_author == []:
            Party_author = 'NO party'
        
        ## Tags 
        tag_table = re.findall('<li><h3>Tags </h3>(.+?)</li>',str(html_bill))
        tags = re.findall('<a href=.+?>(.+?)</a>', str(tag_table))
        if tags == []:
            tags = 'No tags'
    
    ### Save on the dataframe 
    data_bill0 = {"vote_link": url, "bill_link" :  link_bill, "Bill_description": bill_desc, 'Autor' : [authors], 'party_autor': [Party_author], 'tags': [tags]}
    df04 = pd.DataFrame(data_bill0)
    df4 = df4.append(df04)    
    
### Export data set on Raw folder
df.to_csv(r'C:\Users\David\Dropbox\Votaciones_Parlamentarias\raw\Link_list.csv', encoding="utf-8-sig")
df1.to_csv(r'C:\Users\David\Dropbox\Votaciones_Parlamentarias\raw\Overall_info.csv', encoding="utf-8-sig")
df2.to_csv(r'C:\Users\David\Dropbox\Votaciones_Parlamentarias\raw\Votes.csv', encoding="utf-8-sig")
df3.to_csv(r'C:\Users\David\Dropbox\Votaciones_Parlamentarias\raw\Abstentions.csv', encoding="utf-8-sig")
df4.to_csv(r'C:\Users\David\Dropbox\Votaciones_Parlamentarias\raw\Description.csv', encoding="utf-8-sig")