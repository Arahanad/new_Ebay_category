import requests
from bs4 import BeautifulSoup
from helper_class import *
from selenium import webdriver
import time
import json
import concurrent.futures
import os
import pandas as pd

# import requests
# from bs4 import BeautifulSoup
# from helper_class import *
# from selenium import webdriver
# import time,json
# import concurrent.futures

# import os 
# x = os.walk("Output")

# # print(x)
# data = []
# for filename in x: 
#     # print(filename)
#     with open('Output/'+filename, encoding='utf-8') as json_data:   
#                 data += json.load(json_data)

# print(len(list(set(data))))

class JSON_HELPER():
    def __init__(self) -> None:
        self.data = []
        self.helper = Helper()

    def json_in_output(self):
        x = os.listdir("Other-Business")
        for filename in x:
            with open('Other-Business/' + filename, encoding='utf-8') as json_data:
                self.data += json.load(json_data)

    def create_final_output(self):
        listing_urls = []
        data = self.json_in_output()
        for url in self.data:
            if '/itm/' in url:
                listing_urls.append(url)
        listing_urls = list(set(listing_urls))
        print(len(listing_urls))
        with open('Output_Final.json', 'w', encoding='utf-8') as outfile:
            json.dump(listing_urls, outfile, indent=4)


    def create_CSV(self):
        directory = input("Creating files in Directory: ")

        output = []
        with open('main_output.json', encoding='utf-8') as json_data:
            output += json.load(json_data)

        print(len(output))

        filtered_data = []
        for item in output:
            print(item['url'])
            # data = item['price'].replace("PLN", "").replace("HF", "").replace("/ea", "").replace("C", "").replace("GBP", "").replace("EUR", "").replace("AU", "").replace(",", "").replace("US", "").replace("$", "")
            data = self.helper.dollar_to_int(item['price'])
            # print(data)
            # if item['price'] == '':
            #     item['price'] = '0.00'
            # print(data >= 300)
            if item['Condition'] not in ['開封済み', '中古品', '出品者再生品', 'パーツ用または不稼働品', '新品'] and data >= 500:
                filtered_data.append(item)

        print(len(filtered_data))

        if len(filtered_data) < 10000:
            for i in range(len(filtered_data)):
                df = pd.DataFrame(filtered_data)
            df.to_csv(directory + str(len(filtered_data)) + '.csv', sep=',', index=False)
        else:
            for i in range(10000, len(filtered_data), 10000):
                print(i)
                if i > 10000:
                    df = pd.DataFrame(filtered_data[i - 10000:i])
                    df.to_csv(directory + str(i) + '.csv', sep=',', index=False)
                else:
                    df = pd.DataFrame(filtered_data[:i])
                    df.to_csv(directory + str(i) + '.csv', sep=',', index=False)

            df = pd.DataFrame(filtered_data[10000:])
            # df = pd.DataFrame(x[:10000])
            # df.to_csv('Output/outputWithEncodding.csv', sep='\t',index=False)
            # df.to_csv('Output/outputWithComma.csv', sep=',',index=False)
            # df.to_csv('Output/outputWithComma.csv', sep=',',index=False)
            # print(len(output))
            df.to_csv(directory + str(20000) + '.csv', sep=',', index=False)

    def wtite_csv(self):
        with open('output.json', 'r') as json_file:
            data = pd.read_json(json_file)

        data.to_csv('output111.csv', index=False)


    def total_data(self):
        data = []

        for dirpath, dirnames, filenames in os.walk("Output"):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                
                with open(file_path, encoding='utf-8') as json_data:
                    data += json.load(json_data)

        print(len(set(data)))

    def create_test_csv(self):
        output = []
        with open('output.json', encoding='utf-8') as json_data:
                    output += json.load(json_data)
        test = []
        for d in output[:50000]:
            if d['title'] != '':
                    test.append(d)
                    # print(d)
        print(len(test),len(output))
        df = pd.DataFrame(test)
        df.to_csv('test.csv', sep='\t')
    
    def delate_json_link(self):
        with open('marged_all_data.json', 'r', encoding='utf-8') as json_file:
            main_data = json.load(json_file)
        print(len(main_data))


        data = []
        for i in main_data:
            u = i['url']
            # if u and u not in data:
            data.append(u)
        data = list(set(data))
        print("+"*25,len(data))


        with open("Output_Final.json", 'r', encoding='utf-8') as link_file:
            link_to_remove = json.load(link_file)
        print("*"*50,len(link_to_remove ))


        link = []

        link = list(set(link_to_remove) -set(data))

        # for i in link_to_remove:
        #     if i not in data:
        #         link.append(i)
        print(len(link))

        with open('modified_file21.json', 'w', encoding='utf-8') as modified_json_file:
            json.dump(link, modified_json_file, indent=4)

    def marge_json_data(self):
        merged_data = []

        file_paths = ['output1.json', 'output2.json', 'output3.json', 'output5.json', 'output6.json']

        for file_path in file_paths:
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    merged_data += data
                    print()
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in file {file_path}: {str(e)}")

        with open('marged_all_data.json', 'w', encoding='utf-8') as outfile:
            json.dump(merged_data, outfile, indent=4)
if __name__ == "__main__":
    object = JSON_HELPER()
    # object.create_final_output()
    object.create_CSV()






        