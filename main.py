import requests
from bs4 import BeautifulSoup
from helper_class import Helper
import random
from math import ceil
import concurrent.futures
import os

class Scraper:
    def __init__(self):
        self.helper = Helper()
        self.proxy_filename = "data.json"
        self.all_proxies = list(
            filter(
                lambda c: c["country_code"] == "US",
                self.helper.read_json_file(self.proxy_filename)["proxies"],
            )
        )
        self.data = {
            "name":'',
            "description":'',
            'price':"",
            'image':[],
            'condition':'',
            'shippingFee':''
        }
        self.cookies = {
            # 'QuantumMetricSessionID': 'a84fc7c1b9b7e77fcb769f2af7137c80',
            # 'ebay': '%5Ejs%3D1%5E',
        }
        self.headers = {
            'authority': 'www.ebay.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            # 'cookie': 'QuantumMetricSessionID=a84fc7c1b9b7e77fcb769f2af7137c80; ebay=%5Ejs%3D1%5E',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-full-version': '"117.0.5938.89"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        }
        self.all = []
        self.step = 1
        self.url = 'https://www.ebay.com/b/Other-Business-Industrial-Equipment/26261/bn_1865499'

    def getProxy(self):
        proxy = random.choice(self.all_proxies)
        proxyHandler = f'http://{proxy["username"]}:{proxy["password"]}@{proxy["proxy_address"]}:{proxy["ports"]["http"]}'
        return {"https": proxyHandler, "http": proxyHandler}

    def getListing(self, price):
        outer = []
        prev = price + self.step
        print('*'*50)
        print('*'*50)
        print(price,prev,1)
        params = {
            'mag': '1',
            'rt': 'nc',
            'LH_BIN': '1',
            '_dmd':'1',
            '_sop':'1',
            '_udlo': str(price),
            '_udhi':str(prev)
        }
        while True:
            try:
                proxies = self.getProxy()
                    # https://www.ebay.com/b/Enterprise-Networking-Servers/175698/bn_1309143?LH_BIN=1&mag=1&rt=nc&_dmd=1&_sop=15&_udlo=310
                response = requests.get(
                    self.url,
                    params=params,
                    cookies=self.cookies,
                    headers=self.headers,
                    timeout=10,
                    proxies=proxies,
                )
                if response.status_code == 200: 
                    break
            except Exception as e:
                print(e)
                # time.sleep(10)
                pass
        soup = BeautifulSoup(response.content, 'lxml')

        results =  self.helper.dollar_to_int(self.helper.get_text_from_tag(soup.find('h2',{'class':'srp-controls__count-heading'})).split(' Results')[0])

        print(self.helper.get_text_from_tag(soup.find('h2',{'class':'srp-controls__count-heading'})),ceil(results/45))

        n= 2
        point = 0
        if ceil(results/45) > 200:
            print('pages splited')
            n = 3

        for i in range(1,n):

            if n==3:
                if i == 1:
                    price = price 
                    prev = price + 0.5
                if i == 2:
                    price = price + 0.5
                    prev = price + 0.5
                print(price,prev)
            elif n==2:
                
                prev = price + self.step
                print(price,prev)
            # else:
            #     prev = price +1
            print('*'*50)
            
            print(price,prev,1)
            params = {
                'mag': '1',
                'rt': 'nc',
                'LH_BIN': '1',
                '_udlo': str(price),
                '_udhi':str(prev)
            }

            while True:
                proxies = self.getProxy()

                try:
                    response = requests.get(
                        self.url,
                        params=params,
                        cookies=self.cookies,
                    proxies=proxies,
                        headers=self.headers,
                    timeout=10
                    )
                    if response.status_code == 200: 
                        break
                except Exception as e:
                    print(e)
                    # time.sleep(10)
                    pass
            soup = BeautifulSoup(response.content, 'lxml')

            results =  self.helper.dollar_to_int(self.helper.get_text_from_tag(soup.find('h2',{'class':'srp-controls__count-heading'})).split(' Results')[0])
            print(self.helper.get_text_from_tag(soup.find('h2',{'class':'srp-controls__count-heading'})))
            listing = []
            for li in soup.find_all('li',{"class":'s-item s-item--large'}):
                listing.append(self.helper.get_url_from_tag(li.find('a')).split('?')[0])
                outer.append(self.helper.get_url_from_tag(li.find('a')).split('?')[0])
                # all.append(helper.get_url_from_tag(li.find('a')).split('?')[0])
            print(len(listing),len(list(set(outer))),len(list(set(self.all))))

            self.helper.write_json_file(listing, self.Directory +str(price)+'_'+str(prev)+'_1.json')

            pages = ceil(results/45)
            print(pages)
            for page in range(2,pages+1):
                print('*'*50)
                print(price,prev,page)

                lastOuter = len(list(set(outer)))
                params = {
                    'mag': '1',
                    'rt': 'nc',
                    '_pgn': str(page),
                    '_udlo': str(price),
                    '_udhi':str(prev)
                }

                while True:
                    try:
                        proxies = self.getProxy()
                
                        response = requests.get(
                            self.url,
                            params=params,
                            cookies=self.cookies,
                    proxies=proxies,
                            headers=self.headers,
                    timeout=10
                        )
                        if response.status_code == 200: 

                            break
                    except:
                        # time.sleep(10)
                        pass
                soup = BeautifulSoup(response.content, 'lxml')

                results =  self.helper.dollar_to_int(self.helper.get_text_from_tag(soup.find('h2',{'class':'srp-controls__count-heading'})).split(' Results')[0])

                listing = []
                for li in soup.find_all('li',{"class":'s-item s-item--large'}):
                    listing.append(self.helper.get_url_from_tag(li.find('a')).split('?')[0])
                    outer.append(self.helper.get_url_from_tag(li.find('a')).split('?')[0])
                    # all.append(helper.get_url_from_tag(li.find('a')).split('?')[0])
                print(len(listing),len(list(set(outer))),len(list(set(self.all))))


                self.helper.write_json_file(listing, self.Directory +str(price)+'_'+str(prev)+'_'+str(page)+'.json')

            self.helper.write_json_file(list(set(outer)),self.Directory+str(price)+'_output.json')
        # ... (rest of the code for getListing method)

    def scrape(self):
        start = 500
        end = 5000
        links = [price for price in range(start, end, self.step)]
        self.Directory = input("Creating files in Directory: ") +"/"
        os.mkdir(self.Directory)

        

        # for i in range(start, end, self.step):
        #     self.getListing(i)
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(self.getListing, links)

if __name__ == "__main__":
    scraper = Scraper()
    scraper.scrape()



# helper.write_json_file(list(set(all)),'Output/all_output13.json') 