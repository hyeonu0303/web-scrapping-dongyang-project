# 정규식(regular expression) 쉽게 문자열에서 패턴에 해당하는 부분을 추출
import re
# 동적크롤링(스크래핑)
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys

# url연결
url = "https://www.weather.go.kr/w/index.do"
# Chrome브라우저 및 get요청
browser = webdriver.Chrome()
browser.implicitly_wait(15) # 최대 15초 동안 대기
browser.get(url)

#'-'문자를 숫자0으로 반환하는함수
def float_extract_number(string):
    # 정규식 패턴으로 숫자 추출
    numbers = re.findall(r'\d+', string)
    if numbers:
        # 추출된 숫자가 있다면 첫 번째 숫자 반환
        return float(numbers[0])
    else:
        # 추출된 숫자가 없다면 0 반환
        return 0

def int_extract_number(string):
    # 정규식 패턴으로 숫자 추출
    numbers = re.findall(r'\d+', string)
    if numbers:
        # 추출된 숫자가 있다면 첫 번째 숫자 반환
        return int(numbers[0])
    else:
        # 추출된 숫자가 없다면 0 반환
        return 0

# 지역
area = browser.find_element(
    By.CSS_SELECTOR, 'a.serch-area-btn.accordionsecond-tit').text
# 온도
temp = browser.find_element(By.CSS_SELECTOR, "span.tmp").text
temp = float(temp[:-1])

# 최저온도
minTemp = browser.find_element(By.CSS_SELECTOR, 'span.tmin').text.replace(
    "최저", "")
def fMinTemp(minTemp):
    if minTemp == "-":
        return "자료가없습니다."
    else:
        return minTemp
    
# 최고온도
maxTemp = browser.find_element(By.CSS_SELECTOR, 'span.tmax').text.replace("최고", "")

# 체감온도
actualTemp = browser.find_element(By.CLASS_NAME, 'chill').text.replace(
    "체감", "").replace("(", "").replace(")", "")
# 어제보다 몇도높은지 부분 스크래핑
temp_diff = browser.find_element(By.CSS_SELECTOR, '.wrap-1>.w-txt').text

# wrap-2>li>val이 3개여서 items에담음
items = browser.find_elements(By.CSS_SELECTOR, '.wrap-2.no-underline li')

# 습도
humidity_str = items[0].find_element(By.CLASS_NAME, 'val').text
humidity = int(re.findall('\d+', humidity_str)[0])

# 바람
wind_str = browser.find_element(By.CSS_SELECTOR,
                            'div.cmp-cur-weather.wbg.wbg-type2 > '
                            ' ul > li:nth-child(2) > span.val').text
wind = float(re.findall(r'\d+(?:\.\d+)?', wind_str)[0])

# 강수량
rainfall_str = items[2].find_element(By.CLASS_NAME, 'val').text
rainfall = float_extract_number(rainfall_str)

# 초미세먼지
ultraDust = browser.find_element(By.CSS_SELECTOR,
                'span.air-lvv').get_attribute('textContent')
ultraDust = int_extract_number(ultraDust)
# 미세먼지
dust_str = browser.find_element(By.CSS_SELECTOR,
        'ul.wrap-2.air-wrap.no-underline > li:nth-child(2) > strong.air-level.val > span > span.air-lvv').get_attribute('textContent')
dust = int_extract_number(dust_str)
print(f"선택지역:{area}")
print(f"온도:{temp}")
print(f"{maxTemp}")
print(f"{minTemp}")
print(f"체감온도:{actualTemp}")
print(f"{temp_diff}")
print(f"습도: {humidity} ")
print(f"바람: {wind} m/s", end=' / ')
print(f"강수량: {rainfall} mm", end=' / ')
print(f"초미세먼지:{ultraDust}㎍/m³", end=' / ')
print(f"미세먼지:{dust}㎍/m³", end=' / ') 

# 현재 습도 정보에 따른 출력
def fHumidity(humidity):
    # if humidity >= 30 and humidity <= 60:
    if humidity <= 30:
        return ["습도낮음! 물과보습 필수!", "슬픈표정.png"]
    elif humidity <= 60:
        return ["습도적당! 쾌적~~", "기쁜표정.png"]
    elif humidity <= 100:
        return ["습도높음! 불쾌지수업!!", "놀란표정.png"]
    else:
        return ["자료없음"]

# 현재 바람 정보에 따른 출력
def fWind(wind):
    if wind <= 0.3:
        return ["이정도면 바람이 안부네요!", "기쁜표정.png"]
    elif wind <= 1.5:
        return ["실바람이 불어요!", "기쁜표정.png"]
    elif wind <= 3.3:
        return ["남실바람이 불어요!", "슬픈표정.png"]
    elif wind <= 5.4:
        return ["산들바람이 불어요!", "놀란표정.png"]
    else:
        return ["바람이 강하니 외출을 자제해주세요!", "놀란표정.png"]
# 현재 강수량 정보에 따른 출력
def fRainfall(rainfall):
    if rainfall == 0.0:
        return ["오늘은 비가 안와요!", "기쁜표정.png"]
    elif rainfall <= 3.0:
        return ["적은 비가 와요!", "슬픈표정.png"]
    elif rainfall <= 15.0:
        return ["적당한 비가 내려요!", "슬픈표정.png"]
    elif rainfall <= 30.0:
        return ["강한 비가 내리니 외출을 자제하세요!", "놀란표정.png"]
    elif rainfall >= 31.0:
        return ["매우 강한 비가 내리니 외출하지마세요!", "놀란표정.png"]
    else:
        print("자료없음")

# 현재 초미세먼지 정보에 따른 출력
def fUltra(ultraDust):
    if ultraDust <= 15:
        return ["초미세먼지 좋음!", "기쁜표정.png"]
    elif ultraDust <=35:
        return ["초미세먼지 보통!", "./해맑은표정.jpg"]
    elif ultraDust <= 75:
        return ["초미세먼지 나쁨!", "슬픈표정.png"]
    elif ultraDust <= 250:
        return ["초미세먼지 매우 나쁨!", "놀란표정.png"]
    else:
        return ["자료없음"]

# 현재 미세먼지 정보에 따라 출력
def fDust(dust):
    if dust <= 30:
        return ["미세먼지 좋음!", "기쁜표정.png"]
    elif dust <= 80:
        return ["미세먼지 보통!", "기쁜표정.png"]
    elif dust <= 150:
        return ["미세먼지 나쁨!", "슬픈표정.png"]
    elif dust >= 151:
        return ["미세먼지 매우나쁨 KF94필수..", "놀란표정.png"]
    else:
        return ["자료없음"]

def totalWeather(temp,humidity,wind,rainfall,dust,ultraDust):
    #온도
    if temp > 0 and temp <= 4.0:
        temp_output = "울 코트, 히트텍, 가죽 옷, 기모 옷을 입는 것을 추천해요."
    elif temp <= 8.0:
        temp_output = "트렌치코트, 야상, 점퍼, 기모 바지를 입는 것을 추천해요.!"
    elif temp <= 12.0:
        temp_output = "일교차가 커지는 시기예요. 자켓, 가디건, 청자켓, 니트, 청바지를 입는 것을 추천해요."
    elif temp <= 16.0:
        temp_output = "따듯한 날씨에는 얇은 가디건이나 니트, 맨투맨, 후드, 긴 바지를 입는 것을 추천해요. "
    elif temp <= 20.0:
        temp_output = "블라우스, 긴팔 티, 면바지, 슬랙스를 입는 것을 추천해요."
    elif temp <= 24.0:
        temp_output = "반팔, 얇은 셔츠, 반바지, 면바지를 입는 것을 추천해요. "
    elif temp <= 28.0:
        temp_output = "더위가 매우 심하니 민소매, 반팔, 반바지, 린넨 옷을 입는 것을 추천합니다."
    elif temp <= 40.0:
        temp_output = "매우덥습니다! 반팔,반바지,샌들을 추천합니다. (실외활동주의)"
    else:
        return "패딩, 두꺼운 코트, 누빔 옷, 기모, 목도리를 입는 것을 추천해요."
    #습도
    if humidity <= 30:
        humidity_output = "습도: 습도낮음! 물과보습 필수!"
    elif humidity <= 60:
        humidity_output = "습도: 습도적당! 쾌적~~"
    elif humidity <= 100:
        humidity_output ="습도: 습도높음! 불쾌지수업!!"
    else:
        humidity_output = "습도: 자료없음"
    #바람
    if wind <= 0.3:
        wind_output = "바람: 바람이 거의안불어요! 앞머리 안날리는날!"
    elif wind <= 1.5:
        wind_output = "바람: 바람이 조금불어요! 앞머리 지킬수있어요!"
    elif wind <= 3.3:
        wind_output = "바람: 조금강한 바람이 불어요.앞머리 주의!!"
    elif wind <= 5.4:
        wind_output = "바람: 강한바람이 불어요! 앞머리주의!!"
    else:
        wind_output = "바람: 태풍인가..!? 외출자제해주세요!!"
    #강수량
    if rainfall == 0:
        rainfall_output = "강수량: 오늘은 비가 안와요!"
    elif rainfall <= 3.0:
        rainfall_output = "강수량: 약한 비가 와요! 혹시모르니 우산챙기세요!"
    elif rainfall <= 15.0:
        rainfall_output = "강수량: 우산 꼭 챙기기!!"
    elif rainfall < 30.0:
        rainfall_output = "강수량: 비가많이오네요!! 우산 꼭 챙기기!!"
    elif rainfall >= 30.0:
        rainfall_output = "강수량: 비가 너무많이와요!! 우산과 샌들은 필수!!"
    else:
        rainfall_output = "자료없음"
    #미세먼지
    if dust <=30:
        dust_output =  "미세먼지: 미세먼지 좋음!"
    elif dust <= 80:
        dust_output =  "미세먼지: 미세먼지 보통!"
    elif dust <= 150:
        dust_output =  "미세먼지: 미세먼지 나쁨! 외출주의"
    elif dust > 150:
        dust_output =  "미세먼지: 미세먼지 매우나쁨 KF94필수.."
    else:
        dust_output =  "자료없음"
    #초미세먼지
    if ultraDust <= 15:
        ultraDust_output = "초미세먼지 좋음! 오랜만에 이런날씨가"
    elif ultraDust <= 35:
        ultraDust_output = "초미세먼지 보통! 피크닉하기에 좋은날!!"
    elif ultraDust <= 75:
        ultraDust_output = "초미세먼지 나쁨! 마스크 꼭 착용!"
    elif ultraDust > 75:
        ultraDust_output = "초미세먼지 매우 나쁨! 창문닫고외출하시고 마스크 꼭 착용!!"
    else:
        ultraDust_output = "자료없음"
    output = [temp_output, humidity_output, wind_output, rainfall_output, ultraDust_output, dust_output]
    #한칸씩 띄어주기위한코드
    output_str = "\n".join(output)
    return output_str
browser.quit()

data = {
    'area': area,
    'temp': temp,
    'maxTemp': maxTemp,
    'minTemp': minTemp,
    'actualTemp': actualTemp,
    'temp_diff': temp_diff,
    'humidity': humidity,
    'wind': wind,
    'rainfall': rainfall,
    'ultraDust': ultraDust,
    'dust': dust
}

html_template = '''
<!DOCTYPE html>
<html lang="kr">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Data</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
        }}
        h1 {{
            color: #333;
        }}
        table {{
            border-collapse: collapse;
            margin-top: 20px;
        }}
        table td, table th {{
            border: 1px solid #333;
            padding: 8px;
        }}
    </style>
</head>
<body>
    <h1>Weather Data</h1>
    <table>
        <tr>
            <th>지역</th>
            <td>{area}</td>
        </tr>
        <tr>
            <th>온도</th>
            <td>{temp}</td>
        </tr>
        <tr>
            <th>최고온도</th>
            <td>{maxTemp}</td>
        </tr>
        <tr>
            <th>최저온도</th>
            <td>{minTemp}</td>
        </tr>
        <tr>
            <th>체감온도</th>
            <td>{actualTemp}</td>
        </tr>
        <tr>
            <th>어제보다 온도차</th>
            <td>{temp_diff}</td>
        </tr>
        <tr>
            <th>습도</th>
            <td>{humidity}</td>
        </tr>
        <tr>
            <th>바람</th>
            <td>{wind}</td>
        </tr>
        <tr>
            <th>강수량</th>
            <td>{rainfall}</td>
        </tr>
        <tr>
            <th>초미세먼지</th>
            <td>{ultraDust}</td>
        </tr>
        <tr>
            <th>미세먼지</th>
            <td>{dust}</td>
        </tr>
    </table>
</body>
<style>

</style>
</html>
'''

# 데이터를 HTML 템플릿에 적용
html_output = html_template.format(**data)

# HTML 파일로 저장
with open('weather_data.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

