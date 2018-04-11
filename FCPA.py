### Name: Ahmad Al-Dajani
### Filename: scraper.py
### Description: library of functions that will webscrape.
### Time: unlimited
### Dependencies: scraper.py, requests, BeautifulSoup, urllib.parse, OS, PyPDF2, re, csv
### Help: supremeCourtOpinionDownload.py
import scraper
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


# Function that takes string argument of URL, will return an html string containing the contents of the entire web page available at the URL
    # def downloadURL(self):
    #     ### Method that will return the html of a given url
    #     content = requests.get(self.url)
    #     return content.text
class Scraper():
    def __init__(self, url, urlList=None):
        self.url = url
        self.urlList = urlList
        self.links = Scraper.get_all_links(self, url)
        self.absolute_links = Scraper.url_list_to_absolutes(self, base = input('Base: '), urlList=self.links)
        self.soup = Scraper.get_soup(self, url)
    def get_all_links(self, url):
        urlList = []
        html = requests.get(url)
        soup = bs4.BeautifulSoup(html.text, 'html5lib')
        allLinks = []
        for link in soup.find_all('tr'):
            if link.get('onclick'):
                urlList.append(link.get('onclick'))
        return urlList
    #### Get certain urls that end with something, or have certain keywords in them. If using list of keywords, you must specify whether you want links that contain all the words in the keywords list or you want links that contain any one of the words in the keywords list.
    def get_type(self):
        try:
            return type(literal_eval(self))
        except (ValueError, SyntaxError):
            # A string, so return str
            return str
    def url_list_to_absolutes(self, base, urlList):
        absoluteURLs = []
        for url in urlList:
        #unpack each url in the url list, attach it to the base, and stick the result in a list.
            convertURLs = urllib.parse.urljoin(base, url)
            absoluteURLs.append(convertURLs)
        return absoluteURLs
    def get_soup(self, url):
        html = requests.get(url)
        soup = bs4.BeautifulSoup(html.text, 'html5lib')
        return soup
    def special_links(self, extension=None, keywords=None, condition=None):
        ### print("created the list")
        if extension and not keywords:
            ### print('found extension argument')
            soup = Scraper.get_soup(url)
            ### print("we got the soup")
            hrefs = [link.get('onclick') for link in soup.select('tr') if link.get('onclick')]
            if isinstance(extension, str):
                ### print('extension is string. Next, create the list of special links')
                specified_list = [href for href in hrefs if href.endswith(extension) if href not in specified_list]
                ### print('created the list of special links')
                return specified_list
            if isinstance(extension, list):
                ### print('extension is a list')
                for href in hrefs:
                    for ext in extension:
                        if href.endswith(ext):
                            if href not in specified_list:
                                specified_list.append(href)
                return specified_list
        if keywords and not extension:
            ### print("Found Keywords Argument")
            soup = Scraper.get_soup(url)
            hrefs = [link.get('onclick') for link in soup.select('tr') if link.get('onclick')]
            if isinstance(keywords, str):
                ### print('keywords is one string')
                specified_list = [href for href in hrefs if keywords in href if href not in specified_list]
                return specified_list
            if isinstance(keywords, list):
                ### print('keywords is a list')
                if 'and' in condition:
                    ### print('found condition: {}'.format(condition))
                    #check if all the words in the list are in the href, and if so, append it to the specified_list
                    for href in hrefs:
                        if all(word in href for word in keywords):
                            if href not in specified_list:
                                specified_list.append(href)
                    return specified_list
                if 'or' in condition:
                    ### print('found condition: {}'.format(condition))
                    for href in hrefs:
                        for word in keywords:
                            ### print('finding match for ', word)
                            if word in href:
                                ### print('found match for {} in {}'.format(word, href))
                                if href not in specified_list:
                                    specified_list.append(href)
                    return specified_list
        if (extension and keywords):
            soup = Scraper.get_soup(url)
            hrefs = [link.get('onclick') for link in soup.select('tr') if link.get('onclick')]
            if isinstance(extension, str):
                if isinstance(keywords, str):
                    ### go through each href, check i fit ends with the extension, then check if it has the keyword, then check if the href is not already in the list, then append
                    new_list=[]
                    for href in hrefs:
                        if href.endswith(extension):
                            if keywords in href:
                                if href not in specified_list:
                                    specified_list.append(href)
                    return specified_list
                if isinstance(keywords, list):
                    ### go through each href, if the href ends with the extension, then go through each keyword, if the condition is 'and', then check if all keywords are in the href, then check if the href is not already in the list, and appendself.
                    selected_hrefs = [href for href in hrefs if href if href.endswith(extension)]
                    if 'and' in condition:
                        for href in selected_hrefs:
                            if all(word in href for word in keywords):
                                ### print(href)
                                if href not in specified_list:
                                    ### print('href not in list')
                                    specified_list.append(href)
                                else:
                                    print('href already exists, will not append')
                    ### if or is the condition, go through each href that ends with the extension, go through each word inthe keywords, if you find a match between the word and the href, and the href is not already in the list, then append it to the list.
                    if 'or' in condition:
                        for href in selected_hrefs:
                            for word in keywords:
                                if word in href:
                                    if href not in specified_list:
                                        # print('found {} that was not in the list'.format(href))
                                        specified_list.append(href)
                    return specified_list
            if isinstance(extension, list):
                for ext in extension:
                    selected_hrefs = [href for href in hrefs if href if href.endswith(ext)]
                    if isinstance(keywords, str):
                        #print("executing codeblock at 117")
                        specified_list = [href for href in selected_hrefs if (keywords in href and href not in specified_list)]
                    if isinstance(keywords, list):
                        if 'and' in condition:
                            for href in selected_hrefs:
                                if all(word in href for word in keywords):
                                    if href not in specified_list:
                                        ### print("executing codeblock at 125")
                                        specified_list.append(href)
                        if 'or' in condition:
                            ### print("executing codeblock at 130")
                            for href in selected_hrefs:
                                for word in keywords:
                                    if (word in href) and (href not in specified_list):
                                        specified_list.append(href)
                return specified_list


# class Scraper_File_Downloader:
#     def __init__(self)
#
#         match = re.search(r'(?<=litigation)(?:\/).+', url)
#         if match:
#             match = re.sub(r'\/.+\/', r'', match.group(0))
#             DocName = str(match)
#         else:
#             DocName = 'unknown file'
#         return DocName
# # self.url = url
# #     def base(self):
# #     #     ### Method that will get the base of a url
# #          components = urllib.parse.urlparse(self.url)
# #          base = str(components[1]) + '/'
# #          return base
#     ### if the links you want end with a specific extension, pass the extension to the extension argument
#      ## get me the links with optional extensions from the url
#     def urlListToAbsolutes(self, urlList):
#     ## make any relative urls into absolute URLS
#
#         base = Scraper.base(self)
#
#         absoluteURLs = []
#         for url in urlList:
#             #unpack each url in the url list, attach it to the base, and stick the result in a list.
#             print(os.path.join().urljoin(base, url))
#             #absoluteURLs.append(convertURLs)
#         return# absoluteURLs
#
# #Function to Get Docket Number from URL as Filename
#
#
# #Get links for all years in SEC Website
# def get_all_years_links(url):
#     response = requests.get(url)
#     soup = bs4.BeautifulSoup(response.text, 'html5lib')
#     relative_links = []
#     year_urls = []
#     for link in soup.findAll('a'):
#         if 'admin' in link.get('href') or 'suspensions' in link.get('href'):
#             if link.get('href').endswith('shtml'):
#                 relative_links.append(link['href'])
#                 for link in relative_links:
#                     if urllib.parse.urljoin('https://www.sec.gov/', link) in year_urls:
#                         continue
#                     year_urls.append(urllib.parse.urljoin('https://www.sec.gov/', link))
#     return year_urls
#
# # Function that will Download a PDF file from a given URL and save it. Then produce a response that I can operate on.
# def downloadPDF(url):
#     # go to the URL i gave you and download the PDF file
#     getPDF = requests.get(url)
#     # I did this in order to change the name of the file according to the URL
#     DocName = get_filename(url)
#     DocName = DocName
#     cwd = os.getcwd()
#     print("Currently Downloading: " + str(DocName) + " in " + str(cwd))
#     # save the PDF in the working directory as pdfFile.pdf
#     fp = open(DocName, 'wb')
#     for chunk in getPDF.iter_content():
#         fp.write(chunk)
#     fp.close()
#     # open the file you saved
#     fp = open(DocName, 'rb')
#     # # read it and give me an object.
#     reader = PyPDF2.PdfFileReader(fp)
#     return reader
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
