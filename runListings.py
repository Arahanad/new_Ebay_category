
from helper_class import *
from getListingsByItm import getListingsByItm


class Runner():

    def __init__(self):

        self.MAX_TRIALS = 3
        self.data = []

        with open('modified_file21.json', encoding='utf-8') as json_data:
            self.data += json.load(json_data)

        self.done = []

        with open('done.json', encoding='utf-8') as json_data:
            self.done += json.load(json_data)

        

        print(len(self.data))
        self.data = list(set(set(self.data)- set(self.done)))
        print(len(self.data))
        self.output = []
        with open('output.json', encoding='utf-8') as json_data:
            self.output += json.load(json_data)


        self.statuses = []
        # with open('statuses.json', encoding='utf-8') as json_data:
        #     self.statuses += json.load(json_data)

        self.flag = True

    def parse(self,url):
        try:
            if '/itm/' in url:
                print(url)
                out,status = getListingsByItm(url)
                # out,status = 1,200
                if out != -1:
                    self.output.append(out)
                    self.done.append(url)


                    if self.flag:
                        self.flag = False
                        with open('output.json', 'w', encoding='utf-8') as outfile:
                            json.dump(self.output, outfile, indent=4)
                    
                    
                        with open('done.json', 'w', encoding='utf-8') as outfile:
                                json.dump(self.done, outfile, indent=4)
                                
                        time.sleep(600)

                        self.flag = True



                # self.statuses.append({'url':url,'status':status})
                # with open('statuses.json', 'w', encoding='utf-8') as outfile:
                #         json.dump(self.statuses, outfile, indent=4)
                print(len(self.output))
        except Exception as e:
            print(e,url)

    def scrape(self):
        
        print('scrape')

        # for i in self.data[:20]:
        #      self.parse(i)


        self.run_multiThread(
            self.parse,
            100,
            self.data[:100000],
        )
        pass

        while True:
            if self.flag:
                break


    def run_multiThread(self, function, max_workers, args):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(function, args)

if __name__ == "__main__":
    Runner().scrape()