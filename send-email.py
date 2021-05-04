import yagmail, requests, datetime, time
print("Enter your pincode : ",end="")
p = input()
p = str(p)
while(1):
    today = datetime.date.today()
    result = []
    for i in range(5): 
        today += datetime.timedelta(days=1)
        s = str(today)
        arr = s.split("-")
        actual_date = arr[2]+"-"+arr[1]+"-"+arr[0]
        response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="+p+"&date="+actual_date)
        result.append(response.json())
    flag = 0
    stations = []
    for day in result:
        for session in day:
            if len(day[session]) != 0 :
                centers = day[session]
                for i in centers:
                    if i['min_age_limit'] == 18:
                        detail = i['name']+"  |  Address : "+i['address']+"  |  Free/Paid : "+i['fee_type']
                        print(detail)
                        stations.append(detail)
                        flag = 1
    receiver = "your_email.com"
    if flag == 1:
        print("Sending email")
        body = ""
        for i in stations:
            body = body + i +"\n"
        yag = yagmail.SMTP("yag_email@gmail.com")
        yag.send(
            to=receiver,
            subject="Slots available",
            contents=body,
        )
    else:
        print("No slots available")
    time.sleep(600)
