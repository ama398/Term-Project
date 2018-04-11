### Name: Ahmad Al-Dajani
### Filename: scraper.py
### Description: library of functions that will webscrape.
### Time: unlimited
### Dependencies: scraper.py, requests, BeautifulSoup, urllib.parse, OS, PyPDF2, re, csv
### Help: supremeCourtOpinionDownload.py
# import pip
# def import_or_install(package):
#     try:
#         __import__(package)
#     except ImportError:
#         pip.main(['install', package])
# packages = ['csv', 'bs4', 're', 'os', 'requests', 'urllib.parse', 'PyPDF2', 'sys', 'io', 'datetime', 'json', 'ast', 'urllib.request', 'pdfminer.six']
#
# for package in packages:
#     import_or_install(package)
import csv
import bs4
import re
import os
import requests
import urllib.parse
import PyPDF2
import sys
import io
import datetime
import json
from urllib.parse import urljoin
from ast import literal_eval
from urllib.request import urlopen
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO
import codecs
import os
import sys, getopt



# Function that takes string argument of URL, will return an html string containing the contents of the entire web page available at the URL
    # def downloadURL(self):
    #     ### Method that will return the html of a given url
    #     content = requests.get(self.url)
    #     return content.text
class Scraper():
    def __init__(self, url):
        self.url = url
        self.relative_links = []
        self.absolute_links = []
        self.soup = Scraper.get_soup(url)
        self.special_relative_links = []
    #### Method to Soup Given URL
    def get_soup(self):
        html = requests.get(self)
        soup = bs4.BeautifulSoup(html.text, 'html5lib')
        return soup
    ### Method to get all links from url
    def get_all_links(self):
        html = requests.get(self)
        soup = bs4.BeautifulSoup(html.text, 'html5lib')
        for link in soup.find_all('a'):
            self.relative_links.append(link.get('href'))
        return self.relative_links
    ### Get certain urls that end with something, or have certain keywords in them. If using list of keywords, you must specify whether you want links that contain all the words in the keywords list or you want links that contain any one of the words in the keywords list.
    def url_list_to_absolutes(self, base, urlList):
        for url in urlList:
        #unpack each url in the url list, attach it to the base, and stick the result in a list.
            convertURLs = urllib.parse.urljoin(base, url)
            self.absolute_links.append(convertURLs)
        return self.absolute_links
    ### Method for selecting certain links with extensions or keywords.
    def special_links(self, extension=None, keywords=None, condition=None):
        ### print("created the list")
        if extension and not keywords:
            ### print('found extension argument')
            soup = self.soup
            ### print("we got the soup")
            hrefs = [link.get('href') for link in soup.select('a')]
            if isinstance(extension, str):
                ### print('extension is string. Next, create the list of special links')
                for href in hrefs:
                    if href.endswith(extension):
                        if href not in self.special_relative_links:
                            self.relative_links.append(href)
                ### print('created the list of special links')
                return self.relative_links
            if isinstance(extension, list):
                ### print('extension is a list')
                for href in hrefs:
                    for ext in extension:
                        if href.endswith(ext):
                            if href not in self.relative_links:
                                self.relative_links.append(href)
                return self.relative_links
        if keywords and not extension:
            ### print("Found Keywords Argument")
            soup = self.soup
            hrefs = [link.get('href') for link in soup.select('a')]
            if isinstance(keywords, str):
                ### print('keywords is one string')
                for href in hrefs:
                    if keywords in href:
                        if href not in self.relative_links:
                            self.relative_links.append(href)
                return self.relative_links
            if isinstance(keywords, list):
                ### print('keywords is a list')
                while condition == None:
                    print("You must provide a condition when using keywords.\n You can type \'and\' to require that all keywords are in the link. Alternatively, you type 'or' which will return links containing any one of the keywords provided")
                    condition = input('Condition: ')
                    continue
                if 'and' in condition:
                    ### print('found condition: {}'.format(condition))
                    #check if all the words in the list are in the href, and if so, append it to the specified_list
                    for href in hrefs:
                        if all(word in href for word in keywords):
                            if href not in self.relative_links:
                                self.relative_links.append(href)
                if 'or' in condition:
                ### print('found condition: {}'.format(condition))
                    for href in hrefs:
                        for word in keywords:
                        ### print('finding match for ', word)
                            if word in href:
                            ### print('found match for {} in {}'.format(word, href))
                                if href not in self.relative_links:
                                    self.relative_links.append(href)
                return self.relative_links
        if (extension and keywords):
            soup = self.soup
            hrefs = [link.get('href') for link in soup.select('a')]
            if isinstance(extension, str):
                if isinstance(keywords, str):
                    ### go through each href, check i fit ends with the extension, then check if it has the keyword, then check if the href is not already in the list, then append
                    new_list=[]
                    for href in hrefs:
                        if href.endswith(extension):
                            if keywords in href:
                                if href not in self.relative_links:
                                    self.relative_links.append(href)
                    return self.relative_links
                if isinstance(keywords, list):
                    ### go through each href, if the href ends with the extension, then go through each keyword, if the condition is 'and', then check if all keywords are in the href, then check if the href is not already in the list, and appendself.
                    selected_hrefs = [href for href in hrefs if href if href.endswith(extension)]
                    while condition == None:
                        print("You must provide a condition when using keywords.\n You can type \'and\' to require that all keywords are in the link. Alternatively, you type 'or' which will return links containing any one of the keywords provided")
                        condition = input('Condition: ')
                        continue
                    if 'and' in condition:
                        for href in selected_hrefs:
                            if all(word in href for word in keywords):
                            ### print(href)
                                if href not in self.relative_links:
                                ### print('href not in list')
                                    self.relative_links.append(href)
                    ### if or is the condition, go through each href that ends with the extension, go through each word inthe keywords, if you find a match between the word and the href, and the href is not already in the list, then append it to the list.
                    if 'or' in condition:
                        for href in selected_hrefs:
                            for word in keywords:
                                if word in href:
                                    if href not in self.relative_links:
                                    # print('found {} that was not in the list'.format(href))
                                        self.relative_links.append(href)
                return self.relative_links
            if isinstance(extension, list):
                for ext in extension:
                    selected_hrefs = [href for href in hrefs if href if href.endswith(ext)]
                    if isinstance(keywords, str):
                        #print("executing codeblock at 117")
                        for href in selected_hrefs:
                            if (keywords in href and href not in self.relative_links):
                                self.relative_links.append(href)
                    if isinstance(keywords, list):
                        while condition == None:
                            print("You must provide a condition when using keywords.\n You can type \'and\' to require that all keywords are in the link. Alternatively, you type 'or' which will return links containing any one of the keywords provided")
                            condition = input('Condition: ')
                            continue
                        if 'and' in condition:
                            for href in selected_hrefs:
                                if all(word in href for word in keywords):
                                    if href not in self.relative_links:
                                    ### print("executing codeblock at 125")
                                        #print(href)
                                        self.relative_links.append(href)
                        if 'or' in condition:
                            ### print("executing codeblock at 130")
                            for href in selected_hrefs:
                                for word in keywords:
                                    if (word in href) and (href not in self.relative_links):
                                        self.relative_links.append(href)
                return self.relative_links
class File():
    def __init__(self, url):
        if url.startswith("http"):
            self.url = url
            self.soup = Scraper.get_soup(url)
            self.filename = File.get_filename(url)
            self.new_dir = File.create_dir()
            self.error_dict = {}
        else:
            self.filename = url
            self.new_dir = File.create_dir()
            self.error_dict = {}

    def live_dangerously(self, fn, *args):
        ### Function to be called by other methods. This is a recursive exception handler.
        ### Designed to handle unicode errors by replacing error characters with empty string.
        error_dict = {}
        try:
            writer = fn(*args)
            return writer
        except UnicodeEncodeError as e:
            print("got an error{}".format(e))
            ### Find the problem character from the Exception string. Isolate it. Then replace it.
            problem_character = re.search(r'(?<=\')\\.+(?=\')', str(e))
            print("looking for your rascal")
            if problem_character != None:
                print(problem_character)
                character = problem_character.group(0)
                error_dict.setdefault(self.filename, []).append(character)
                args = args.replace(character, '')
                print("Got the error. But dont worry, I'm fixing it")
            return live_dangerously(self, fn, *args)
        finally:
            return error_dict

    def get_filename(self):
        # Get everything after the first slash
        pattern = re.search(r'(?<=[a-z]{3})(/)(.+)', self)
        if pattern:
            return re.sub('/', '-', pattern.group(2))

    ### Method for converting PDF Files to TXT files
    def convert_PDF(self):
        print('converting pdf to text')
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(self, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()
        for page in PDFPage.get_pages(fp, pagenos,
                                      maxpages=maxpages,
                                      password=password,
                                      caching=caching,
                                      check_extractable=True):
            interpreter.process_page(page)
        print("Converted PDF to Text, now writing to text file")
        text = retstr.getvalue()
        DocName = self.replace('pdf', 'txt')
        text_file = open(DocName, 'w')
        print('Starting Live Dangerously')
        #print(text)
        error = File.live_dangerously(self, text_file.write, text)

        print('Successfully Living Dangerously')
        text_file.close()
        # try:
        #     try:
        #         try:
        #             text_file = open(fname.replace('pdf', 'txt'), 'w')
        #             text_file.write(text)
        #         except BaseException as e:
        #             if re.search(r'(?<=\')\\.+(?=\')', str(e)):
        #                 match = re.search(r'(?<=\')\\.+(?=\')', str(e))
        #                 character = match.group(0)
        #                 error_dict.setdefault(fname, []).append(character)
        #                 new_body = re.sub(character, '', text)
        #                 text_file.write(new_body)
        #             else:
        #                 error_dict.setdefault(fname, 'File Encoding: UTF-8')
        #                 text_file = open(fname.replace('pdf', 'txt'), 'w', encoding='utf-8')
        #                 text_file.write(text)
        #     except BaseException as f:
        #         if re.search(r'(?<=\')\\.+(?=\')', str(f)):
        #             match = re.search(r'(?<=\')\\.+(?=\')', str(f))
        #             character = match.group(0)
        #             error_dict.setdefault(fname, []).append(character)
        #             new_body = re.sub(character, '', text)
        #             text_file.write(new_body)
        #         else:
        #             error_dict.setdefault(fname, 'File Encoding: UTF-8')
        #             text_file = open(fname.replace('pdf', 'txt'), 'w', encoding='utf-8')
        #             text_file.write(text)
        # except BaseException as g:
        #     if re.search(r'(?<=\')\\.+(?=\')', str(g)):
        #         match = re.search(r'(?<=\')\\.+(?=\')', str(g))
        #         character = match.group(0)
        #         error_dict.setdefault(fname, []).append(character)
        #         new_body = re.sub(character, '', text)
        #         text_file.write(new_body)
        #     else:
        #         error_dict.setdefault(fname, 'File Encoding: UTF-8')
        #         text_file = open(fname.replace('pdf', 'txt'), 'w', encoding='utf-8')
        #         text_file.write(text)
        # text_file.close()
        fp.close()
        device.close()
        retstr.close()
        return error
        # if len(self.error_dict) > 0:
        #     print("Detected Error: {0}".format(self.error_dict))
        #     return self.error_dict
        # else:
        #     return print("Converted PDF File {0}. No Errors Detected.".format(fname))
    def download_PDF(self):
        PDF = requests.get(self.url)
        print('got html, now getting filename')
        DocName = self.filename
        print('got filename, now writing file')
        fp = open(DocName, 'wb')
        for chunk in PDF.iter_content():
            fp.write(chunk)
        print('wrote file')
        fp.close()
    def download_HTM(self):
        error_dict = {}
        response = requests.get(self.url)
        print('got response')
        soup = Scraper.get_soup(self.url)
        print('souped up')
        body = soup.strings
        print('got text')
        DocName = File.get_filename(self.url).replace('htm', 'txt')
        print('got name')
        cwd = os.getcwd()
        text = ''.join(body)
        fp = open(DocName, 'w', encoding='utf-8')
        try:
            fp.write(text)
            print('trying to write file to text')
        except BaseException:
            print('got an exception, will replace character')
            character = '{0}'.format(re.search(r'(?<=\')\\.+(?=\')', str(e)).group(0))
            if character:
                print('found character'.format(character))
                error_dict.setdefault(DocName, []).append(character)
                print('loggin error')
                new_body = re.sub(character, '', text)
                print('subbed character, now writing new file')
                fp.write(new_body)
                print('wrote new file')
        fp.close()
        if len(error_dict) > 0:
            return error_dict
        else:
            return print("Downloaded HTM File. No Errors Detected.")
    def download_TXT(self):
        error_dict = {}
        response = urlopen(self)
        data = response.read()
        body = data.decode('utf-8', errors='ignore')
        DocName = File.get_filename(self)
        fp = open(DocName, 'w')
        try:
            fp.write(body)
        except BaseException as e:
            character = '{0}'.format(re.search(r'(?<=\')\\.+(?=\')', str(e)).group(0))
            error_dict.setdefault(DocName, []).append(character)
            new_body = re.sub(character, '', body)
            fp.write(new_body)
        fp.close()
        if len(error_dict) > 0:
            return error_dict
        else:
            return print("Downloaded TXT File. No Errors Detected.")
    ### Method for creating directories:
    def create_dir():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        new_path = str(dir_path) + '\\' + "Downloaded Files"
        cwd = os.getcwd()
        if cwd != new_path:
            if not os.path.isdir(new_path):
                os.makedirs(new_path)
            change_cwd = os.chdir(new_path)
        return
    def copy_file(file, dir):
        fp = open(file)
        text = fp.read()
        os.chdir(dir)
        new_file = open(file, 'w')
        new_file.write(text)
        new_file.close()
        os.chdir('..')
        fp.close()
        os.remove(file)
        return "Copied File to Text Directory"
    ### Method for Downloading PDF Files in a given page
# # Function that will download TXT Files from a given URL, save it, then produce a response that can be operated on.
# def download_text(url):
#     # Get URL Contents
#     html = downloadURL(url)
#     # turn it into a bs4 object then encode it. ###Encoding is required because I ran into encoding errors without it.
#     soup = bs4.BeautifulSoup(html, 'html5lib').encode('utf-8')
#     # Each File is given its docket number as its name.
#     DocName = get_filename(url)
#     # Create a new file with the same name of the file we are downloading
#     fp = open(DocName, 'w')
#     # Write the contents of the current file we are downloading into this new file.
#     fp.write(soup.decode('utf-8', 'ignore'))
#     cwd = os.getcwd()
#     # Give user status on which file we are downloading and where?
#     print("Currently Downloading: {0} in {1}".format(DocName, cwd))
#     # Close the New File.
#     fp.close()
#     return
# # Function that will get the text from a pdf file
# def textFromPDF(reader, url):
#     error_dict = {}
#     docText = ''
#     filename = get_filename(url).replace('pdf', 'txt')
#     numberOfPages = reader.getNumPages()
#     for i in range(0, numberOfPages):
#         pages = reader.getPage(i)
#         allText = pages.extractText()
#         docText = docText + allText
#         file_page = "Ran into Error in File {0} at Page {1}".format(str(filename), i)
#     #docText = docText.replace('\ufb01', ' ').replace('\ufb02', ' ').replace('\u02c7', ' ')
#         try:
#             fp = open(filename, 'w')
#             fp.write(docText)
#         except BaseException as e:
#             print(type(docText))
#             break
#             error_dict[file_page] = str(e)
#             fp.write(docText.decode('ascii', 'backslashreplace'))
#             ##fp.write(docText.encode('ascii', 'ignore'))
#             #fp.write(docText.encode('utf-8'))
#         fp.close()
#     return error_dict
# # Function to Fix URLs
# def adjust_url(year):
#     now = datetime.datetime.now()
#     current_year = str(now.year)
#     if year.isdigit() and year != current_year:
#         url = "https://www.sec.gov/litigation/admin/adminarchive/adminarc" + str(year) + ".shtml"
#         suspensions_url = "https://www.sec.gov/litigation/suspensions/suspensionsarchive/susparch" + str(year) + ".shtml"
#     else:
#         url = "https://www.sec.gov/litigation/admin.shtml"
#         suspensions_url = "https://www.sec.gov/litigation/suspensions.shtml"
#     return [url, suspensions_url]
# # Create directory for saving data in one place based by year
# def create_dir(year, url):
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     folder_name = re.sub('(\/.+\/)', r'', url)
#     if 'admin' in folder_name:
#         new_path = str(dir_path) + "\\" + "Data" + "\\" + str(year) + " SEC Administrative Proceedings"
#     else:
#         new_path = str(dir_path) + "\\" + "Data" + "\\" + str(year) + " SEC Suspensions"
#     if not os.path.isdir(new_path):
#         os.makedirs(new_path)
#     change_cwd = os.chdir(new_path)
#     return print("Changed Current Working Directory to {}".format(os.getcwd()))
# # Function that will collect document urls from a given url and put them in a list.
# def get_docs(url):
#     html = downloadURL(url)
#     #look for document links in that url, and add them to a list
#     text_links = linksInHTML(html, 'txt')
#     pdf_links = linksInHTML(html, 'pdf')
#     htm_links = linksInHTML(html, 'htm')
#     document_links = text_links + pdf_links + htm_links
#     # collect take the links in the list, and turn them into absolute links.
#     document_url_list = urlListToAbsolutes("https://www.sec.gov", document_links)
#     return document_url_list
# #write function pull the error out, identify the character and replace it in the binary
# def Download_Administrative_Proceedings(year):
#     errors = {}
#
#     if year.isdigit():
#         url_list = adjust_url(year)
#         for url in url_list:
#             create_dir(year, url)
#             document_url_list = get_docs(url)
#             for url in document_url_list:
#                 # if url.endswith('htm') or url.endswith('txt'):
#                 #     download_text(url)
#                 if url.endswith('pdf'):
#                     reader = downloadPDF(url)
#                     error_dict = textFromPDF(reader, url)
#                     filename = get_filename(url)
#                     for key in error_dict.keys():
#                         errors[key] = error_dict
#                 # if url.endswith('txt'):
#                 #     reader = scraper.download_text(url)
#
#
#         # Go through each url we have collected from this year, and check if it is a PDF or a TXT. If it is, then download the files.
#         # Create a new folder for these files called Year SEC Administrative Proceedings
#         # create_dir(year)
#         # for url in document_url_list:
#         #     url = url.strip()
#         #     if ('litigation' and 'admin') in url or ('litigation' and 'suspensions') in url:
#         #         print(url[-4] + url[-3] + url[-2] + url[-1] )
#         #         if url.endswith('htm'):
#         #             scraper.download_text(url)
#         #             print(url)
#     elif year == 'ALL':
#         url = "https://www.sec.gov/litigation/admin.shtml"
#         year_urls = get_all_years_links(url)
#         for date in year_urls:
#             if re.search(r'\d\d\d\d', date):
#                 year = re.search(r'\d\d\d\d', date).group(0)
#             else:
#                 year = 2018
#             # create a seperate folder for each year
#             create_dir(year)
#             document_url_list = get_docs(date)
# #    open("Error_Files.json", 'w').write(json.dumps(errors))
# #Download_Administrative_Proceedings('2018')
#             #print(document_url_list)
#             # Go through each document filed in this year
#             #for document in document_url_list:
#
#             #     for url in document_url_list:
#             #         url = url.strip()
#             #
#             #             extension = url[-4] + url[-3] + url[-2] + url[-1]
#             #             if url.endswith('htm'):
#             #                 reader = scraper.download_text(url)
#             #             if url.endswith('pdf'):
#             #                 reader = scraper.downloadPDF(url)
#             #             if url.endswith('txt'):
#             #                 reader = scraper.download_text(url)
#             # return
#
#                             #print(response.text)
#         # Prior to 2000, the SEC predominantly published proceedings in txt format. This accounts for those years, depending on the file type.
#         #html = scraper.downloadURL(url)
#         #print(html)
#         #soup = bs4.BeautifulSoup(html, 'html5lib')
#         #print(soup.prettify())
#         #print(soup.get_text(strip=True))
# #Download_Administrative_Proceedings('2018')
#
#         #     reader = scraper.downloadPDF(url)
#         #     readerList.append(reader)
#         # elif url.endswith(".txt"):
#         #     reader = scraper.download_text(url)
#         #     #readerList.append(reader)
#         # elif url.endswith(".htm"):
#         #     reader = scraper.download_text(url)
#         #     readerList.append(reader)
#         #     #reader = reader.decode('utf-8')
#         # for thing in readerList:
#         #     if thing == 'Empty':
#         #         readerList.remove(thing)
#     #return readerList
# # text_list = []
# # dir_path = str(os.path.dirname(os.path.realpath(__file__)))
# for subdir, dirs, files in os.walk(dir_path):
#     for File in files:
#         if File.endswith('.pdf'):
#             path = os.chdir(subdir)
#             print(path)
#             pdfFileObj = open(File, 'rb')
#             reader = PyPDF2.PdfFileReader(pdfFileObj)
#             pdfFiles = []
#             docText = ''
#             numberOfPages = reader.getNumPages()
#             for i in range(0, numberOfPages):
#                 pages = reader.getPage(i)
#                 allText = pages.extractText().encode('utf-8')
#                 print(File, i, len(allText.decode('utf-8', 'ignore')))
#             #pageObj = pdfReader.getPage(0)
            #print(pageObj.extractText())
# COME BACK TO THIS LATER
# def create_csv(file):
#     fp = open(str(year) + "SEC Proceedings.csv", "w", newline='', encoding = 'latin-1')
#     #read the csv you created
#     reader = csv.reader(fp)
#
#     # this is a list of the headers I would like to have
#     fieldNames = ["Date Initiated", "Docket Number", "Respondents", "Order Title"]
#     headingWriter = csv.DictWriter(fp, fieldNames)
#     headingWriter.writeheader()
