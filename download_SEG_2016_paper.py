import os
import sys  
import urllib
import requests
import re
import shutil

# dir path & file path
beginpath = "E:\EndNoteDownload\SEG"
foldername="test"
fullpath = os.path.join(beginpath, foldername)
print(fullpath)
if not os.path.exists(fullpath):
            os.makedirs(fullpath)

filename = os.path.join(fullpath, "html_info.txt")
filename2 = os.path.join(fullpath, "pdf_info_list.txt")
filename3 = os.path.join(fullpath, "fname.txt")
filename4 = os.path.join(fullpath, "download_url.txt")
print(filename)

# 代理设置
proxies = {
  'http': '127.0.0.1:8087',
  'https': '127.0.0.1:8087',
}

# 伪造cookies
hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}  
# html=requests.get('http://library.seg.org/doi/pdf/10.1190/segam2016-13957987.1')
# html=requests.get('http://library.seg.org/doi/pdf/10.1190/segam2016-13957987.1', proxies=proxies)
html=requests.get('http://library.seg.org/doi/book/10.1190/segeab.35?ct=098151bb0cab683119c67758b3af4ade28bceffeca51199893262f7165646cc97c796d1fed0dacb8282c24a9d844ca799781c3448b014422bc6f56c6cf6e006e', proxies=proxies)

html.encoding = 'utf-8' #这一行是将编码转为utf-8否则中文会显示乱码。  
print(html.headers['content-type'])

with open(filename,'w',encoding='utf-8') as f:
 f.write(html.text)

#获得所有info  
total_info = re.findall('<table class="articleEntry">(.*?)<div class="citation tocCitation">',html.text,re.S)  
#re.findall('</div><div class="doiCrossRef">(.*?)<div class="citation tocCitation">',html.text,re.S)  
number=1
with open(filename2,'w',encoding='utf-8') as f:
    for each in total_info: 
        f.write(str(number))  
        f.write('\n')
        f.write(each)
        f.write('\n')
        number+=1

#获得文件名、作者
number=1
with open(filename3,'w',encoding='utf-8') as f,open(filename4,'w',encoding='utf-8') as f1:
    for index in range(len(total_info)): 
        each=total_info[index]
        title = re.findall('"hlFld-Title">(.*?)</span>',each,re.S) 
        title_new = re.sub('[^a-zA-Z]',' ',title[0])
        #title[0].replace(':',' ').replace('?',' ').replace('<sub>',' ').replace('</sub>',' ').replace('/',' ').replace('*',' ')

        author = re.findall('<a class="entryAuthor"(.*?)</a></span>',each,re.S)
        author1 = re.findall('(?:">)(.*)',author[0],re.S) 
        author_new=re.sub('[^a-zA-Z]',' ',author1[0])

        pdf_url = re.findall('<a class="ref nowrap" href="(.*?)"><div class="art_title">',each,re.S) 
        #re.findall('<a class="ref nowrap" href="(.*?)"><div class="art_title">',each,re.S)
        pdf_url_new=pdf_url[0].replace('/doi/abs/','http://library.seg.org/doi/pdf/')

        
        f.write(str(number))  
        f.write('\n')
        #f.write(str(title))
        pdf_name = "2016"+"-"+author_new+"-"+title_new+".pdf"
        f.write(pdf_name)
        f.write('\n')
        f.write(pdf_url_new) 
        f.write('\n')
        # print debug infor & download files
        #print(author[0])
        print(author_new)   
        print(pdf_name)
        print(pdf_url_new)
        if index>452 and index<484:#326:
            filename5 = os.path.join(fullpath,pdf_name)
            response = requests.get(pdf_url_new, stream=True, proxies=proxies)
            with open(filename5, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
        f.write('\n')
        number+=1
