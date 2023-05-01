import requests
import json
from datetime import date
from dateutil.relativedelta import relativedelta

# 일반 인증키 (Encoding)	
encodingKey = 'W1iiVMT%2B2sbZ8H8eb9jveDYqYWAqshpCwnNk8XWZJUU%2BFq%2B6bNUcpEM5XpBudzcaXNe2oTGbok2HcX58UyH6ng%3D%3D'
# 일반 인증키 (Decoding)	
decodingKey = 'W1iiVMT+2sbZ8H8eb9jveDYqYWAqshpCwnNk8XWZJUU+Fq+6bNUcpEM5XpBudzcaXNe2oTGbok2HcX58UyH6ng=='

services = [
#   'getDataSetOpnStdBidPblancInfo'     # 데이터셋 개방표준에 따른 입찰공고정보
# , 'getDataSetOpnStdScsbidInfo'      # 데이터셋 개방표준에 따른 낙찰정보
 'getDataSetOpnStdCntrctInfo']     # 데이터셋 개방표준에 따른 계약정보

# urls = []
# for svc in services:
#       urls.append(f'http://apis.data.go.kr/1230000/PubDataOpnStdService/{svc}')

# print(response.content)
# j = json.loads(response.text)
# print(j['response']['header'])
# print(j['response']['body']['items'][0])

if __name__ == "__main__":
    # for all url
    for svc in services:
        url = f'http://apis.data.go.kr/1230000/PubDataOpnStdService/{svc}'
        # file open
        with open(f'{svc}.jl', "w") as f:
            # for date from 20200101 to 20221231 step 1 month
            start_dt = date(2022, 1, 1)
            end_dt = start_dt + relativedelta(day=31)

            # get 10 rows while reachs j['response']['header']['totalCount']
            
            bidNtceBgnDt = f'{start_dt.year}{start_dt.month:02}{start_dt.day:02}0000'
            bidNtceEndDt = f'{end_dt.year}{end_dt.month:02}{end_dt.day}2359'
            while start_dt < date(2022, 12, 1):
                pageNo = 1
                NUM_OF_ROWS = 10
                while True:
                    print(f'{svc}: start_dt={start_dt}, pageNo={pageNo}')
                    params ={'serviceKey' : decodingKey, 'pageNo' : pageNo, 'numOfRows' : NUM_OF_ROWS, 'type' : 'json', 'bidNtceBgnDt' : bidNtceBgnDt, 'bidNtceEndDt' : bidNtceEndDt}
                    response = requests.get(url, params=params)
                    try:
                        j = json.loads(response.text)
                        # print(j['response']['header'])
                        # print(j['response']['body']['items'][0])

                        # write to file
                        for item in j['response']['body']['items']:
                            f.write(str(item) + '\n')
                        totalCount = j['response']['body']['totalCount']
                        if pageNo * NUM_OF_ROWS > totalCount:
                            break
                    except Exception as e:
                        print(e)
                    finally:
                        pageNo += 1

                # steps 1 month 
                start_dt = start_dt + relativedelta(month=1)
                bidNtceBgnDt = f'{start_dt.year}{start_dt.month:02}{start_dt.day:02}0000'
                bidNtceEndDt = f'{end_dt.year}{end_dt.month:02}{end_dt.day}2359'
                
        # close file
