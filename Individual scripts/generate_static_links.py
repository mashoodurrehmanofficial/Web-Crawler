import  requests,os,json
from concurrent.futures import ThreadPoolExecutor

from generate_sitemap import root_url
from bs4 import BeautifulSoup as bs4



rawhtmlfile=[os.path.join(os.getcwd(),'HTML',x) for x in os.listdir(os.path.join(os.getcwd(),'HTML'))]


def fetcher(alllinks):   
    jslinks=[]
    csslinks=[]
    imglinks=[]
    index=1
    for url in alllinks:
        with open(url, 'rb') as htmlfile:  
            soup = bs4(htmlfile,'lxml')  
            rawcsslinks=soup.find_all('link')
            for x in rawcsslinks:
                if '.css' in x['href']:csslinks.append(x['href'])
            
            rawjslinks=soup.find_all('script')
            for x in rawjslinks:
                try:
                    if '.js' in x['src']:jslinks.append(x['src'])
                except:pass
            
            rawimglinks=soup.find_all('img')
            for x in rawimglinks:
                imglinks.append(x['src'])
        print(f'{index} files have been fileterd !!!')
        index=index+1

    return [list(set(csslinks)),list(set(jslinks)),list(set(imglinks))]

 

data=fetcher(rawhtmlfile) 

def generatestaticlinks():
    with open('static_links.json', 'w') as outfile:
        json.dump({"all_links":data}  , outfile)
        print('_____________________________STATIC_FILES_REGISTERED__100%')
  
   
generatestaticlinks()