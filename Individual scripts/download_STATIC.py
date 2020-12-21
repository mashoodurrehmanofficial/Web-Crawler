import  requests,os,json,urllib,uuid
from concurrent.futures import ThreadPoolExecutor
from generate_sitemap import root_url
from bs4 import BeautifulSoup as bs4 




root_url=root_url+'/' if not root_url.endswith('/') else root_url
PARSED_ROOT_URL=urllib.parse.urlsplit(root_url)
ENCODED_STATIC_FILES_DATA=[]
def get_static_links():
    with open('static_links.json') as json_file:
        static_links = json.load(json_file)['all_links']
        return static_links
STATIC_FILES=get_static_links()

ACCURATE_CSS_ROOT_URL=''

def createcssfiles(url,session):
    url=url[0:-1] if url.endswith('/') else url
    filename=url.split('/')[-1] 
    fileextension=filename.split('.')[-1]
    if '?' in filename:
        if '.css' in filename:fileextension='.css'
        elif '.js' in filename:fileextension='.js'
        elif '.png' in filename:fileextension='.php'
        elif '.jpg' in filename:fileextension='.jpg'
        elif '.jpeg' in filename:fileextension='.jpeg'
        elif '.ico' in filename:fileextension='.ico'
        elif '.gif' in filename:fileextension='.gif'
        elif '.webp' in filename:fileextension='.webp'
        filename=str(uuid.uuid4()).replace('-','')+'.'+fileextension
        print('+++++++++++++++',filename)
    
    
    if not os.path.exists(os.path.join(os.getcwd(),'Static',filename)):
        if 'js' in fileextension or 'css' in fileextension:
            with open(os.path.join(os.getcwd(),'Static',filename),'wb') as target:
                target.write(session.get(ACCURATE_CSS_ROOT_URL+url).text.encode('utf-8'))
                print(f'________{fileextension}___WRITTEN')    
        else:
            with open(os.path.join(os.getcwd(),'Static',filename),'wb') as target:
                target.write(session.get(ACCURATE_CSS_ROOT_URL+url).content)
                print(f'________{fileextension}___WRITTEN')    
    else:print('____________ALREADY___EXISTS !!!')
    data={
        'orignalurl':url,
        'newurl':f'../Static/{filename}',
        'encodedurl':True if '?' in filename else False
    } 
    ENCODED_STATIC_FILES_DATA.append(data)
def getcssfiles(cssfiles):  
    global ACCURATE_CSS_ROOT_URL
    if os.path.exists(os.path.join(os.getcwd(),'Static')):pass
    else:os.makedirs(os.path.join(os.getcwd(),'Static'))
    with requests.Session() as session:
        for x in cssfiles:
            if not x.startswith('http'):
                # main function to handle 100% ACCURATE url of STATIC FILES
                
                # accurate root is alreay avaliable
                if ACCURATE_CSS_ROOT_URL!='':
                    createcssfiles(x, session)
                else:
                    acuuratestaticurl=''
                    if PARSED_ROOT_URL.path=='/': 
                        acuuratestaticurl=root_url
                        ACCURATE_CSS_ROOT_URL=acuuratestaticurl
                        createcssfiles(x, session)
                    elif PARSED_ROOT_URL.path!='/':
                        acuuratestaticurl=root_url
                        if requests.get(acuuratestaticurl+x).status_code==200:
                                # write file
                                ACCURATE_CSS_ROOT_URL=acuuratestaticurl
                                createcssfiles(x, session)
                                continue
                        # if DOT is in last string 
                        if '.'  in root_url[0:-1].split('/')[-1]:
                            acuuratestaticurl=root_url[0:-1].replace(root_url[0:-1].split('/')[-1],'')+x
                            test1url=root_url[0:-1].replace(root_url[0:-1].split('/')[-1],'')
                            if requests.get(acuuratestaticurl).status_code==200:
                                # write file
                                ACCURATE_CSS_ROOT_URL=test1url
                                createcssfiles(x, session)
                                
                            elif requests.get(acuuratestaticurl).status_code!=200:
                                test2url=test1url[0:-1].replace(test1url[0:-1].split('/')[-1],'')
                                acuuratestaticurl=test2url+x
                                if requests.get(acuuratestaticurl).status_code==200:
                                    # write file
                                    ACCURATE_CSS_ROOT_URL=test2url
                                    createcssfiles(x, session)
                                    pass
                                else:
                                    test3url=test2url[0:-1].replace(test2url[0:-1].split('/')[-1],'')
                                    acuuratestaticurl=test3url+x
                                    ACCURATE_CSS_ROOT_URL=test3url
                                    createcssfiles(x, session)
                        # IF DOT isn't in the last string
                        else:         
                            acuuratestaticurl=root_url[0:-1].replace(root_url[0:-1].split('/')[-1],'')+x
                            test1url=root_url[0:-1].replace(root_url[0:-1].split('/')[-1],'')
                            if requests.get(acuuratestaticurl).status_code==200:
                                # write file
                                ACCURATE_CSS_ROOT_URL=test1url
                                createcssfiles(x, session)
                            elif requests.get(acuuratestaticurl).status_code!=200:
                                test2url=test1url[0:-1].replace(test1url[0:-1].split('/')[-1],'')
                                acuuratestaticurl=test2url+x
                                if requests.get(acuuratestaticurl).status_code==200:
                                    # write file
                                    ACCURATE_CSS_ROOT_URL=test2url
                                    createcssfiles(x, session)
                                    pass
                                else:
                                    test3url=test2url[0:-1].replace(test2url[0:-1].split('/')[-1],'')
                                    acuuratestaticurl=test3url+x
                                    ACCURATE_CSS_ROOT_URL=test3url
                                    createcssfiles(x, session)
                
                        # if '.' in root_url:
                        # root_url=root_url[0:-1] if root_url.endswith('/') else root_url
                    #    test1=root_url
                    
            
def downloadSTATICfiles():      
    getcssfiles(STATIC_FILES[0])
    getcssfiles(STATIC_FILES[1])
    getcssfiles(STATIC_FILES[2]) 
    with open('encoded_static_files_data.json', 'w') as outfile:
        json.dump({"allstaticdata":ENCODED_STATIC_FILES_DATA}  , outfile)
 

downloadSTATICfiles()
