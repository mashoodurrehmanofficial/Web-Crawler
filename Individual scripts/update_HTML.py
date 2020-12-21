import  requests,os,json
from concurrent.futures import ThreadPoolExecutor
from generate_sitemap import root_url
from bs4 import BeautifulSoup as bs4






from iteration_utilities import unique_everseen 
rawhtmlfile=[x for x in os.listdir(os.path.join(os.getcwd(),'HTML'))]
rawfiles=[x.replace('.html','') for x in os.listdir(os.path.join(os.getcwd(),'HTML'))]
 
    

 

def getfilteredhrefs():
    with open('filtered_hrefs.json','rb') as json_file:
        data = json.load(json_file)['all_links']
        return data

def getencodestaticfilesdata():
    with open('encoded_static_files_data.json','rb') as json_file:
        data = json.load(json_file)['allstaticdata']
        return data

 
def readHTML(filename):
    with open(os.path.join(os.getcwd(),'HTML',filename), 'rb') as target:
        data=" ".join([x.decode('utf8') for x in target.readlines()])
        return bs4(data,'lxml')
def writeHTML(filename,data):
    with open(os.path.join(os.getcwd(),'HTML',filename), 'wb') as target:
        target.write(str(data).encode('utf-8'))

repeat=0
def fetcher(alllinks):  
    try:
        for url in alllinks:
            soup=readHTML(url)
            csslinks=soup.find_all('link')      
            for x in csslinks:
                for y in getencodestaticfilesdata():
                    if x['href']==y['orignalurl']:
                        x['href']=y['newurl']  
            imglinks=soup.find_all('img')      
            for x in imglinks:
                for y in getencodestaticfilesdata():
                    if x['src']==y['orignalurl'] or  x['src'].startswith(y['orignalurl']) or x['src'].endswith(y['orignalurl']):
                        x['src']=y['newurl']  
            jslinks=soup.find_all('script')      
            for x in jslinks:
                for y in getencodestaticfilesdata():
                    try:
                        if x['src']==y['orignalurl'] or  x['src'].startswith(y['orignalurl']) or x['src'].endswith(y['orignalurl']):
                            x['src']=y['newurl'] 
                    except:pass
            hrefs=soup.find_all('a')      
            for x in hrefs:
                for y in getfilteredhrefs():
                    try:
                        if x['href']==y['old']:  
                            x['href']=y['new'] 
                            
                    except:pass        
            writeHTML(url,soup)   
            print(url,'HAS BEEN UPDATED')        
    except Exception as e:
        if repeat==0:
            fetcher(rawhtmlfile)       
        else:
            print(str(e)[:400])

            
            
def updateHTML():          
    fetcher(rawhtmlfile) 
 
 
updateHTML()
 
 