import  requests,os,json
from concurrent.futures import ThreadPoolExecutor
from generate_sitemap import root_url
from bs4 import BeautifulSoup as bs4



from iteration_utilities import unique_everseen 
rawhtmlfile=[x for x in os.listdir(os.path.join(os.getcwd(),'HTML'))]
rawfiles=[x.replace('.html','') for x in os.listdir(os.path.join(os.getcwd(),'HTML'))]
FILTERED_HREFS=[]

def fetcher(alllinks):  
    def fetch(url):    
        with open(os.path.join(os.getcwd(),'HTML',url), 'rb') as target:
            data=" ".join([x.decode('utf8') for x in target.readlines()]) 
            soup=bs4(data,'lxml')
            allhrefs=[x for x in soup.find_all('a')]
            pureallhrefs=[]
            for x in allhrefs:
                try:
                    if not x['href'].startswith('#') and not x['href'].startswith('http'):
                        pureallhrefs.append(x)
                except :pass
            
            
            for x in pureallhrefs:
                targethref=''
                if '.html' in x['href']:
                    targethref=[y for y in rawhtmlfile if y in x['href'][0]] 
                elif x['href']=='/':
                    targethref='default_home.html'
                for z in rawfiles:
                    if x['href'].endswith(z):
                        targethref=z+'.html' 
                for z in rawfiles:
                    if z in x['href']:
                        targethref=z+'.html'
                else:
                    targethref=x['href']
                print({'old':x['href'],'new':targethref})
                
                targethref=targethref[0:-1] if targethref.endswith('/') else targethref
                targethref=targethref.split('/')[-1]
                targethref=targethref+'.html' if not targethref.endswith('.html') else targethref
                FILTERED_HREFS.append({'old':x['href'],'new':targethref})
        print(f'LINK___{url}____FILTERED ')
                        
                
            
            
    def starter():
        with ThreadPoolExecutor(max_workers=100) as executor: 
            executor.map(fetch,  [x for x in alllinks])
            executor.shutdown(wait=True)
    starter()  

            
            
            
FILTERED_HREFS=list(unique_everseen(FILTERED_HREFS)) 



def handleinternalhref():
    fetcher(rawhtmlfile) 
    with open('filtered_hrefs.json', 'w') as outfile:
        json.dump({"all_links":FILTERED_HREFS}  , outfile)
        print('_____________________________FILTERED_HREFS__100%')
handleinternalhref()