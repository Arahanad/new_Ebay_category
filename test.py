import requests
from bs4 import BeautifulSoup
from helper_class import *
from selenium import webdriver
import time,json
import concurrent.futures
import os 

x = os.listdir("Other-Business_output")
data = []
# # print(x)
for filename in x: 

    with open('Other-Business_output/'+filename, encoding='utf-8') as json_data:
                data += json.load(json_data)

# with open('output.json', encoding='utf-8') as json_data:
#                 data += json.load(json_data)

# with open('output1.json', encoding='utf-8') as json_data:
#                 data += json.load(json_data)
                
# with open('output2.json', encoding='utf-8') as json_data:
#                 data += json.load(json_data)
# with open('output3.json', encoding='utf-8') as json_data:
#                 data += json.load(json_data)
# with open('output4.json', encoding='utf-8') as json_data:
#                 data += json.load(json_data)
print(len(data))
with open('main_output.json','w', encoding='utf-8') as json_data:
    json.dump(data,json_data)

# lists = []
# print(data[:10])
# for i in (data):
#     # col.append(i.split('bay.com/')[1].split('/')[0])
#     if '/itm/' in i:
#         lists.append(i)
# lists = list(set(lists))
# print(len(lists))
# with open('Output_Final.json', 'w', encoding='utf-8') as outfile:
#             json.dump(lists, outfile, indent=4)
# curr= []
# # with open('Output_Final.json', encoding='utf-8') as json_data:
# #             curr += json.load(json_data)

# new = set(curr) - set(lists)
# print(len(set(new)))


# done = []
# with open('done.json', encoding='utf-8') as json_data:
#             done += json.load(json_data)
# col = []
# for i in list(set(new)):
#     # col.append(i.split('bay.com/')[1].split('/')[0])
#     if '/itm/' in i:
#            col.append(i)
# #     if len(col) >50:
# #         break
# # #         # 
# print(len(list(set(col))))
# with open('output_f.json', 'w', encoding='utf-8') as outfile:
#                                 json.dump(list(set(col)), outfile, indent=4)
# print(len(list(set(set(data)- set(done)))))


# # print(list(set(col)))