import  requests,os
from concurrent.futures import ThreadPoolExecutor
from generate_sitemap import root_url
rawfiles=[]
with open('sitemap.txt','r') as target: 
    for x in [x.strip() for x in target.readlines() if not '.css' in x.strip() and not '.js' in x.strip() and not x.strip().endswith(tuple(['png', 'jpg', 'jpeg','wepb'])) ]:
        url=x[0:-1] if x.strip().endswith('/') else x.strip()
        if url==root_url[0:-1]:filename='default_home.html'
        else:filename=url.split('/')[-1]
        if filename.endswith('.html'):filename=filename
        else:filename=filename+'.html'
        if filename.endswith('.asp'):filename=filename.replace('.asp','.html')  
        rawfiles.append([x.strip(),filename])
    
    
    
# def fetcher(alllinks): 
#     if os.path.exists(os.path.join(os.getcwd(),'HTML')): pass
#     else:os.makedirs(os.path.join(os.getcwd(),'HTML'))
#     def fetch(session, url):   
#         with session.get(url[0]) as results:
#             with open(os.path.join(os.getcwd(),'HTML',url[1]),'w') as file:
#                 file.write(str(results.text))
#                 print('______________________HTML___________100%')
            
            
#     def starter():
#         with ThreadPoolExecutor(max_workers=100) as executor:
#             with requests.Session() as session:
#                 executor.map(fetch, [session] * len(alllinks), [x for x in alllinks])
#                 executor.shutdown(wait=True)
#     starter()  

            
            
#     starter()  

def html_fetcher(alllinks):
    if os.path.exists(os.path.join(os.getcwd(),'HTML')): pass
    else:os.makedirs(os.path.join(os.getcwd(),'HTML'))
    with requests.Session() as session:
        for url in alllinks:  
            print(url[-1])
            
            results=session.get(url[0])  
            print(results.status_code)
            try:
                if results.status_code==200: 
                    with open(os.path.join(os.getcwd(),'HTML',url[-1]) ,'wb') as file:
                        file.write(results.text.encode('utf-8')) 
                        print('____________________HTML______100')
            except:print('____________________EXCEPTION___HANDLING')
          
    
def downloadHTMLfiles():                     
    html_fetcher(rawfiles)
    
downloadHTMLfiles()