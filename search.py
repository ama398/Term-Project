# coding=utf-8
import re
import os
from links import Download
from links import Order
import time
import re
os.chdir('.\htm files')
# relevant_orders = []
# for doc in os.listdir('.'):
#     if doc.endswith('txt'):
#         text = open(doc, 'r', encoding='utf-8').read()
#         title = re.compile( r'order.+((Administrative|cease).+?Proceedings)'.upper(), flags=re.DOTALL)
#         sus =  re.compile( r'order.+suspension'.upper(), flags=re.DOTALL)
#         for match in re.finditer(title, text):
#             relevant_orders.append(doc)
#             # print(doc)
#             # print(re.sub('\n', ' ', match.group(0)))
#         for match in re.finditer(sus, text):
#             relevant_orders.append(doc)
#             # print(doc)
#             # print(match.group(0))
#
# for order in relevant_orders:
#     object = Download(order)
#     object.copy_file('.\orders')
# os.chdir('.\orders')
no_matches = []
for file in os.listdir('.'):
    if file.endswith('txt'):
        print('--------------- New Proceeding ---------------------')
        print(file)
        doc = Order(file)
        doc.filter_proceeding()



        # print(doc.proceeding_header)
        # doc.get_names()
        # doc.get_filing_date()
        # print(doc.filing_date)
        # doc.defendants
        # doc.get_file_number()
        # print(doc.file_no)
        # print(doc.defendants)
        # doc.get_proceeding_type()
        # print(doc.filing_status)
        # print(doc.settlement)
        # print(doc.proceeding_type)
        print('--------------- ------------ ---------------------')
        # print('NO TIMER')
        # time.sleep(0.2)
print(len(Order.matches))
print('--------------------------------')
print(len(Order.no_matches))
# #
# for order in Order.no_matches:
#     Download.copy_file(order, "NO_MATCHES")
#     doc = Order(order).text
#     if len(doc.split('\n')) <= 100:
#         percentage = int((len(doc.split('\n')) * 60) / 100)
#     elif len(doc.split('\n')) > 100 and len(doc.split('\n')) <= 135:
#         percentage = int((len(doc.split('\n')) * 70) / 100)
#     elif len(doc.split('\n')) > 135 and len(doc.split('\n')) <= 220:
#         percentage = int((len(doc.split('\n')) * 30) / 100)
#     elif len(doc.split('\n')) > 220 and len(doc.split('\n')) <= 400:
#         percentage = int((len(doc.split('\n')) * 25) / 100)
#     elif len(doc.split('\n')) > 400 and len(doc.split('\n')) <= 500:
#         percentage = int((len(doc.split('\n')) * 15) / 100)
#     elif len(doc.split('\n')) > 500 and len(doc.split('\n')) <= 800:
#         percentage = int((len(doc.split('\n')) * 10) / 100)
#     else:
#         percentage = int((len(doc.split('\n')) * 5) / 100)
#     i = 0
#     text = doc.split('\n')
#     print(len(doc.split('\n')))
#     print(order)
#     for line in text:
#         print(line)
#         i += 1
#         if i == percentage:
#             break
#     print('--------------New Proceeding-------------------------')
#     time.sleep(2)
# false_negs = []
# for order in Order.no_matches:
#     doc=Order(order)
#     doc.filter_proceeding()
#     pattern = re.compile(r'(administrative|suspension|cease.+?and.+?decist)', flags=re.IGNORECASE)
#     if re.search(pattern, doc.proceeding_header):
#         print(doc.proceeding_header)
#         false_negs.append(order)
# print(len(false_negs))
# for doc in Order.no_matches:
#      Download.copy_file(doc, '.\\nomatches')

# os.chdir('.\date_mismatch')
# for file in os.listdir('.'):
#     Download.copy_file(file, '..')
#
#     print('--------------------------------------------------------------------------------')