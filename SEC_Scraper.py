from links import Scraper
from links import File
import requests
import PyPDF2
import urllib
import sys, io
import bs4
import re
import os
from urllib.request import urlopen

#
AP_main = Scraper('https://www.sec.gov/litigation/admin.shtml')
years = AP_main.special_links(extension='shtml', keywords=['litigation', 'admin'], condition='and')
abs_years = AP_main.url_list_to_absolutes('https://www.sec.gov/litigation/admin.shtml', years)
all_proceedings = []
for year in abs_years:
    year_page = Scraper(year)
    #print(year)
    proceedings = year_page.special_links(extension=['.pdf', '.txt', '.htm'], keywords=['litigation', 'admin'], condition = 'and')
    all_proceedings.append(year_page.url_list_to_absolutes('https://www.sec.gov/litigation/admin.shtml', proceedings))

errors = []
main_proceedings = [proceeding for year in all_proceedings for proceeding in year]
for proceeding in main_proceedings:
    if proceeding.endswith('pdf'):
        File.create_dir()
        obj = File(proceeding)
        doc = obj.filename
        if os.path.isfile(doc):
            print("{} already exists".format(doc))
            print('Next Proceeding ========================================================================================')
            continue
        download_pdf = obj.download_PDF()
        print('Next Proceeding ========================================================================================')
        continue
    elif proceeding.endswith('txt'):
        File.create_dir()
        obj = File(proceeding)
        doc = obj.filename
        error = obj.download_TXT()
        if isinstance(error, dict):
            errors.append(error)
        elif isinstance(error, str):
            print(error)
        print('Next Proceeding ========================================================================================')
        continue
    elif proceeding.endswith('htm'):
        File.create_dir()
        obj = File(proceeding)
        doc = obj.filename.replace('htm', 'txt')
        if os.path.isfile(doc):
            print("{} already exists".format(doc))
            print('Next Proceeding ========================================================================================')
            continue
        else:
            obj.download_HTM()
            if isinstance(error, dict):
                errors.append(error)
            elif isinstance(error, str):
                print(error)
            print('Next Proceeding ========================================================================================')
            continue
# USED THIS TO MAKE SEPARATE DIRECTORY FOR MATCHING Files
# os.makedirs('.\\Downloaded Files\\Text File')
for doc in os.listdir('.\\Downloaded Files'):
    File.create_dir()
    if doc.endswith('pdf'):
        txt = str(doc).replace('pdf', 'txt')
        if os.path.isfile(txt):
            "file already converted.. moving on.."
            continue
        error = File.convert_PDF(doc)
        #error = obj.convert_PDF()
        if isinstance(error, dict):
            errors.append(error)
        elif isinstance(error, str):
            print(error)
        os.remove(file)
    # if doc.endswith('txt'):
    #     text = open(doc).read()
    #     AP = re.search(r'ORDER.+PROCEEDINGS', text, flags=re.DOTALL|re.MULTILINE)
    #     SUS = re.search(r'ORDER.+SUSPENSION', text, flags=re.DOTALL|re.MULTILINE)
    #     if AP:
    #         File.copy_file(doc, dir='.\\Text File')
    #         #print(text)
    #     if SUS:
    #         #print(SUS.group(0))
    #         print(text)
    #         break
    #

#
# for error in errors:
#     print(error)
            # if 'Order Instituting Administrative Proceedings'.upper() in text:
            #     public_proceedings.append(text)
            # elif 'Order Instituting Public Administrative Proceedings'.upper() in text:
            #     public_proceedings.append(text)
            # elif 'Order Instituting Administrative and Cease-and-Desist Proceedings'.upper() in text:
            #     public_proceedings.append(text)
            # elif 'Order Instituting Public Administrative and Cease-and-Desist Proceedings'.upper() in text:
            #     public_proceedings.append(text)
            # elif 'Order Instituting Cease-and-Desist Proceedings'.upper() in text:
            #     public_proceedings.append(text)
            # elif 'Order of Forthwith Suspension'.upper() in text:
            #     public_proceedings.append(text)
            # elif 'Order of Suspension'.upper() in text:
            #     public_proceedings.append(text)
            # else:
            #     pass

            #         public_proceedings.append(body)
