import yagmail
import requests
import datetime
import time
p = ["110001","130001"]
receiver = ["emails@gmail.com","emails@gmail.com"]
while(1):
    for k in range(len(p)):    
        today = datetime.date.today()
        result = []
        for _ in range(5):
            today += datetime.timedelta(days=1)
            s = str(today)
            arr = s.split("-")
            actual_date = arr[2]+"-"+arr[1]+"-"+arr[0]
            while(1):
                response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="+p[k]+"&date="+actual_date)
                if(response.status_code!=200):
                    print("Trying to Connect...........")
                    time.sleep(90)
                else:
                    break            
            result.append(response.json())
        flag = 0
        stations = []
        dont_repeat_stations = []
        for day in result:
            for session in day:
                if len(day[session]) != 0:
                    centers = day[session]
                    for i in centers:
                        if i['min_age_limit'] == 18:
                            detail = i['name']+"  |  Address : " + \
                                i['address']+"  |  Free/Paid : "+i['fee_type']
                            print(detail)
                            stations.append(detail)
                            flag = 1
        if flag == 1:
            print("Sending email")
            body = ""
            for i in stations:
                body = body + i + "\n"
            yag = yagmail.SMTP("yag_email","Password")
            yag.send(
                to=receiver[k],
                subject="Slots available | Go vaccinate",
                contents=body,
            )
        else:
            print("No slots available")
    time.sleep(200)
