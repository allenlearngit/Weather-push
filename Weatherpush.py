import requests as req
import schedule
import time

def grt_weather():
#取得資料
    params ={
        "Authorization":"CWA-BE008C4E-DC34-4ABB-BDAE-FE897CB1AB90",
        "locationName":"新北市",
    }
    res = req.get("https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001", params=params)

    weather = {}
    for i in range(0, 5):
      name = (res.json()["records"]["location"][0]["weatherElement"][i]["elementName"])
      vaule = (res.json()["records"]["location"][0]["weatherElement"][i]["time"][0]["parameter"]["parameterName"])
      weather[name] = vaule
      # print(name, vaule)

    #設定成整數，做以下判斷
    weather["PoP"] = int(weather["PoP"])
    weather["MinT"] = int(weather["MinT"])

    if weather["PoP"] >= 50:
      vehicle = "超過50%會下雨喔"
    else:
      vehicle = "高機率不下雨 不帶傘了"

    if weather["MinT"] <= 15:
      cloth = "超冷 一定要厚外套"
    elif weather["MinT"] <= 20:
      cloth = "還行 薄外套即可"
    elif weather["MinT"] <= 25:
      cloth = "不穿外套"
    else:
      cloth = "短袖出發"

    text = f"今日天氣為{weather["CI"]}\n{cloth}\n{vehicle}"
    return text

#line推播
def lineNotify():
    url = "https://notify-api.line.me/api/notify"
    token = "填入在lineNotify取得的token"
    headers = {
      "Authorization":"Bearer " + token #設定權杖
    }
    data ={
      "message": grt_weather()
    }
    r=req.post(url, headers=headers, data=data)

schedule.every().day.at("07:00:00").do(lineNotify)

while True:
    schedule.run_pending()
    time.sleep(1)