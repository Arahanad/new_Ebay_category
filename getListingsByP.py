import requests
from bs4 import BeautifulSoup
from helper_class import *
import urllib3,time

helper = Helper()
proxy_filename = "data.json"

all_proxies = list(
            filter(
                lambda c: c["country_code"] == "US",
                helper.read_json_file(proxy_filename)["proxies"],
            )
        )

def getProxy():
        proxy = random.choice(all_proxies)

        proxyHandler = f'http://{proxy["username"]}:{proxy["password"]}@{proxy["proxy_address"]}:{proxy["ports"]["http"]}'

        return {"https": proxyHandler, "http": proxyHandler}

def getListingsByp(url):
    try:
        data = {}
        # headers = {
        #     'authority': 'www.ebay.com',
        #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        #     'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8',
        #     'cache-control': 'max-age=0',
        #     # 'cookie': '__ssds=2; __ssuzjsr2=a9be0cd8e; __uzmaj2=eaf211c4-66da-41c9-8263-1fc8d86bfbed; __uzmbj2=1691034516; __gsas=ID=2009903dea8544be:T=1691034518:RT=1691034518:S=ALNI_Mb-QFiwUSpbK-8-kqPnXzae5wvOGg; QuantumMetricUserID=bb4195d054dc8ca0a30c54a3a68c2b4f; __uzma=92421dbc-5c1b-4ffb-a101-26bc22e66588; __uzmb=1691037235; __uzme=9811; QuantumMetricSessionID=95cdd5b0672f65092368f770607e9264; ak_bmsc=D6285B4D64ACBFF09EC6CDD332EA9850~000000000000000000000000000000~YAAQbwkuF2rq9XiJAQAAiKM9vBTUbW8C9QTbQBZ35wM+n/UakTyrpOV2oesXDnupuf5jTcfFMvXdlTKfxWHwtwGcloVZJz09PBiN0acvOf/4lpk6cjSeUBgoRA7o2O77eFCkOeIECsejKA1EN/PcWwnNWdpHbbdmpY8cdI/uSxeHSaFDIuVqZXnHOI45/XUixt4p7ZUI8FxPgflXsDn7ZJCkGKUbaV3/75Nbm5fMftq1swb65VVtqoiJWJILc1PjCXbx8J+ubhiEgPkHNiC8Y7p6uHYRvxqhYq+3W9S0uUVXY+tHMGbU9KqMnt2zKW/Gl8kUhXr+SSUWlYYyHmOJKkcyH/K8mFzUG9H9dTQAqMSuWd9AhxYlp07G4Nx9kyzVDc09UFs9YA==; __gads=ID=7c2d98507b901601:T=1691037247:RT=1691080327:S=ALNI_MYvE1EG3GCf3KpPkBcmSD0DMlBH9g; __gpi=UID=00000c267fcdb883:T=1691037247:RT=1691080327:S=ALNI_MYTHa9DFfP72qcODbQRUmUpc0r5UA; __uzmc=305702869088; __uzmd=1691080328; __uzmf=7f60002edc34f1-8306-4c61-b206-d36ccdeee9f3169103723531843093107-b47d2c0b6e7cd04f28; JSESSIONID=E9F7E4266752BEF49A19FA60BE01928E; s=CgADuAH9kzSiOMTQGaHR0cHM6Ly93d3cuZWJheS5jb20vYi9Db21wdXRlci1Db21wb25lbnRzLVBhcnRzLzE3NTY3My9ibl8xNjQzMDk1P0xIX0JJTj0xJm1hZz0xJnJ0PW5jJl9wZ249MjAwJl9zb3A9NTAwJl91ZGhpPTc2Jl91ZGxvPTc1BwD4ACBkzSiOYjk4MmRlMTcxODkwYTgyNWNjMDQzMzg0ZmZmNWNiZjRdyTdP; bm_sv=6830A0340D0FA2F6EACACF47D285215B~YAAQrw7EF3tSUXKJAQAAMk1AvBRrmk/iAMMChAUxXbCqpRP6tBD7K9rjDW787lqPMzCk6v0mAk09K1DcWuNzUeyw2eLuo0MU6M2Z9pskO9XgIzGBVEFwfc3625psoq6ygFZ+yJL1CAy0rT6uezCRJnb+HI9boBPngfdka5f25KHLICARVt5Qn5sdo7x82T6zTSEnFdWHWiEnYqqqjdigjwQOrG2vhiBejQUSRYvc170PQznWYz50wd1xjD07xMg=~1; ebay=%5Ejs%3D1%5Esbf%3D%23000000%5E; dp1=bu1p/QEBfX0BAX19AQA**688e3e1f^pbf/%23e00020000000000000000066ad0a9f^bl/US688e3e1f^; nonsession=BAQAAAYhF58hiAAaAADMABWatCp8zMzE4NgDKACBojj4fYjk4MmRlMTcxODkwYTgyNWNjMDQzMzg0ZmZmNWNiZjQAywACZMveJzMx5uoTQScsmuxCkhpOSdXkyBxzcWQ*; __deba=eWT3gMBIqFAlc-t_yAP5sZRXz1wLnDyJC9NTlh36vhh03XVtE3VQAG6cJzOtz3wpWAeE4oPxf7zDmm5FZLYHCJ7sxGljVAqrmnhYwCSc_VqnzlwHgWDWp2vZ8uD0b1B2qoaIJrcf4p6NPxS5H5EPBw==; __uzmcj2=101443124459; __uzmdj2=1691080488; ds2=ssts/1691080506232^',
        #     'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        #     'sec-ch-ua-full-version': '"115.0.5790.110"',
        #     'sec-ch-ua-mobile': '?0',
        #     'sec-ch-ua-model': '""',
        #     'sec-ch-ua-platform': '"Windows"',
        #     'sec-ch-ua-platform-version': '"15.0.0"',
        #     'sec-fetch-dest': 'document',
        #     'sec-fetch-mode': 'navigate',
        #     'sec-fetch-site': 'none',
        #     'sec-fetch-user': '?1',
        #     'upgrade-insecure-requests': '1',
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        # }


        # proxies = getProxy()
        
        # response = requests.get('https://www.ebay.com/itm/182582512768',  headers=headers)
        response = requests.get(url)
        if response.status_code != 200:
            return -1,response.status_code


        soup = BeautifulSoup(response.content,'lxml')

        if soup.find('div',{'class':'ux-layout-section-evo__item'}):

            for rows in soup.find('div',{'class':'ux-layout-section-evo__item'}).find_all('div',{'class':'ux-layout-section-evo__col'}):
                pass
                data[helper.get_text_from_tag(rows.find('div',{'class':'ux-labels-values__labels'}))] =helper.get_text_from_tag(rows.find('div',{'class':'ux-labels-values__values'}))
            


        title = helper.get_text_from_tag(soup.find('h1',{'class':'product-title'}))

        price = helper.get_text_from_tag(soup.find('div',{'class':'display-price'}))

        condition = ''
        container = soup.find('div', {'class':'item-desc'})
        if container:
            for ul_element in container.find_all('ul', {'class': 'item-highlights'}):
                for li in ul_element.find_all('li', {'class': 'item-highlight'}):
                    if 'condition' in li.text.lower():
                        condition = helper.get_text_from_tag(li.find('span', {"class": "cc-ts-BOLD"}))
                    break

    
        shipping = ''
        # if soup.find('div',{'class':'ux-labels-values-with-hints ux-labels-values-with-hints--SECONDARY-SMALL'}) is not None:
        #     shipping = helper.get_text_from_tag(soup.find('div',{'class':'ux-labels-values-with-hints ux-labels-values-with-hints--SECONDARY-SMALL'}).find('span',{'class':'ux-textspans ux-textspans--POSITIVE ux-textspans--BOLD'})).strip()
        #     if shipping == '':
        #         shipping = helper.get_text_from_tag(soup.find('div',{'class':'ux-labels-values-with-hints ux-labels-values-with-hints--SECONDARY-SMALL'}).find('span',{'class':'ux-textspans ux-textspans--BOLD'}))
                # print(shipping)
                
        img = ''
        if soup.find('a',{'class':'vi-image-gallery__enlarge-link'}) is not None:
            img = helper.get_src_from_tag(soup.find('a',{'class':'vi-image-gallery__enlarge-link'}).find('img'))


        product_details = {}
        all_details = soup.find('section', {"class": "product-spectification"})
        details = all_details.find_all('li')
        for detail in details:
            key = helper.get_text_from_tag(detail.find('div', {"class": "s-name"}))
            value = helper.get_text_from_tag(detail.find('div', {"class": "s-value"}))
            product_details[key] = value

        
        proxies = getProxy()

        description = ''
        # if soup.find('div',{'class':'vim d-item-description'}) is not None:
        #     descriptionAddr =  helper.get_src_from_tag(soup.find('div',{'class':'vim d-item-description'}).find('iframe'))
        #     description = helper.get_text_from_tag(BeautifulSoup((requests.get(descriptionAddr, proxies=proxies,  headers=headers).content),'lxml'))
        #     print(description)
        

        data['title']=title
        data['ProductDetails'] = product_details
        data['description']=description
        data['price']=price
        data['img']=img
        data['Condition']=condition
        data['shipping']=shipping
        data['url']=url

        
        return data,response.status_code
    except urllib3.exceptions.HTTPError as e:
        print("HTTP Error:", e)
        return -1, e
    except urllib3.exceptions.ConnectTimeoutError as e:
        print("Connection Timeout Error:", e)
        return -1, e
    except urllib3.exceptions.MaxRetryError as e:
        print("Max Retry Error:", e)
        return -1, e
    except Exception as e:
        print(e,url)
        return -1,e
    

if __name__ == "__main__":
    # listings = ['https://www.ebay.com/p/149976423']
    listings = ['https://www.ebay.com/p/149976423', 'https://www.ebay.com/p/1618024352', 'https://www.ebay.com/p/74102241', 'https://www.ebay.com/p/1801454643', 'https://www.ebay.com/p/25037005040', 'https://www.ebay.com/p/13040127276', 'https://www.ebay.com/p/1330521799', 'https://www.ebay.com/p/19029697647', 'https://www.ebay.com/p/4033871397', 'https://www.ebay.com/p/28042406554', 'https://www.ebay.com/p/6044023043', 'https://www.ebay.com/p/20052206642', 'https://www.ebay.com/p/27037176800', 'https://www.ebay.com/p/15051718028', 'https://www.ebay.com/p/74111100', 'https://www.ebay.com/p/18045989494', 'https://www.ebay.com/p/15043082668', 'https://www.ebay.com/p/13056996707', 'https://www.ebay.com/p/8034498902', 'https://www.ebay.com/p/2262827542', 'https://www.ebay.com/p/2093563868', 'https://www.ebay.com/p/3042397506', 'https://www.ebay.com/p/3021448648', 'https://www.ebay.com/p/5019436093', 'https://www.ebay.com/p/26030526993', 'https://www.ebay.com/p/1586586774', 'https://www.ebay.com/p/19009536522', 'https://www.ebay.com/p/129889368', 'https://www.ebay.com/p/1000606396', 'https://www.ebay.com/p/17017879425', 'https://www.ebay.com/p/14042424240', 'https://www.ebay.com/p/17053311931', 'https://www.ebay.com/p/4039500313', 'https://www.ebay.com/p/153513148', 'https://www.ebay.com/p/596071709', 'https://www.ebay.com/p/12053976404', 'https://www.ebay.com/p/23052416719', 'https://www.ebay.com/p/20053011676', 'https://www.ebay.com/p/10024857202', 'https://www.ebay.com/p/25020318700', 'https://www.ebay.com/p/20051792397', 'https://www.ebay.com/p/6041247232', 'https://www.ebay.com/p/10036010713', 'https://www.ebay.com/p/18039071909', 'https://www.ebay.com/p/2071239409', 'https://www.ebay.com/p/27061421125', 'https://www.ebay.com/p/1383421278', 'https://www.ebay.com/p/9035082590', 'https://www.ebay.com/p/27049352725', 'https://www.ebay.com/p/1506220093', 'https://www.ebay.com/p/127430948']

    dataList = []
    for i in listings:
        print(i)
        d,e = getListingsByp(i)
        # time.sleep(7)
        dataList.append(d)
        df = pd.DataFrame(dataList)    
        df.to_csv('test.csv', sep='\t')

