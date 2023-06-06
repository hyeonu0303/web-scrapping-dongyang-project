# 정규식(re)
import re
# 동적크롤링(스크래핑)
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import webbrowser

# url연결
url = "https://www.weather.go.kr/w/index.do"
# Chrome브라우저 및 get요청
browser = webdriver.Chrome()
browser.implicitly_wait(15) # 최대 15초 동안 대기
browser.get(url)
time.sleep(15)

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
# 갱신시간
realTime = browser.find_element(
    By.CSS_SELECTOR, '#current-weather > div.cmp-cmn-para.odam-updated > a > span'
).text

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
print(f"시간:{realTime}")
print(f"온도:{temp}")
print(f"{maxTemp}")
print(f"{minTemp}"  )
print(f"체감온도:{actualTemp}")
print(f"{temp_diff}")
print(f"습도: {humidity} ")
print(f"바람: {wind} m/s")
print(f"강수량: {rainfall} mm")
print(f"초미세먼지:{ultraDust}㎍/m³")
print(f"미세먼지:{dust}㎍/m³") 
def totalWeather(temp,humidity,wind,rainfall,dust,ultraDust):
    #온도
    if temp > 0 and temp <= 4.0:
        temp_output = "❤️추천 옷: 울 코트, 히트텍, 가죽 옷, 기모 옷을 입는 것을 추천해요."
    elif temp <= 8.0:
        temp_output = "❤️추천 옷: 트렌치코트, 야상, 점퍼, 기모 바지를 입는 것을 추천해요.!"
    elif temp <= 12.0:
        temp_output = "❤️추천 옷: 일교차가 커지는 시기예요. 자켓, 가디건, 청자켓, 니트, 청바지를 입는 것을 추천해요."
    elif temp <= 16.0:
        temp_output = "❤️추천 옷: 따듯한 날씨에는 얇은 가디건이나 니트, 맨투맨, 후드, 긴 바지를 입는 것을 추천해요. "
    elif temp <= 20.0:
        temp_output = "❤️추천 옷: 블라우스, 긴팔 티, 면바지, 슬랙스를 입는 것을 추천해요."
    elif temp <= 24.0:
        temp_output = "❤️추천 옷: 반팔, 얇은 셔츠, 반바지, 면바지를 입는 것을 추천해요. "
    elif temp <= 28.0:
        temp_output = "❤️추천 옷: 더위가 매우 심하니 민소매, 반팔, 반바지, 린넨 옷을 입는 것을 추천합니다."
    elif temp <= 40.0:
        temp_output = "❤️추천 옷: 매우덥습니다! 반팔,반바지,샌들을 추천합니다. (실외활동주의)"
    else:
        return "추천 옷: 패딩, 두꺼운 코트, 누빔 옷, 기모, 목도리를 입는 것을 추천해요."
    #습도
    if humidity <= 30:
        humidity_output = "🧡습도: 습도낮음! 물과보습 필수!"
    elif humidity <= 60:
        humidity_output = "🧡습도: 습도적당! 쾌적!!"
    elif humidity <= 100:
        humidity_output ="🧡습도: 습도높음! 불쾌지수 UP!!"
    else:
        humidity_output = "🧡습도: 자료없음"
    #바람
    if wind <= 0.3:
        wind_output = "💛바람: 바람이 거의안불어요! 앞머리 안날리는날!"
    elif wind <= 1.5:
        wind_output = "💛바람: 바람이 조금불어요! 앞머리 지킬수있어요!"
    elif wind <= 3.3:
        wind_output = "💛바람: 조금강한 바람이 불어요.앞머리 주의!!"
    elif wind <= 5.4:
        wind_output = "💛바람: 강한바람이 불어요! 앞머리주의!!"
    else:
        wind_output = "💛바람: 태풍인가..!? 외출자제해주세요!!"
    #강수량
    if rainfall == 0:
        rainfall_output = "💚강수량: 오늘은 비가 안와요!"
    elif rainfall <= 3.0:
        rainfall_output = "💚강수량: 약한 비가 와요! 혹시모르니 우산챙기세요!"
    elif rainfall <= 15.0:
        rainfall_output = "💚강수량: 우산 꼭 챙기기!!"
    elif rainfall < 30.0:
        rainfall_output = "💚강수량: 비가많이오네요!! 우산 꼭 챙기기!!"
    elif rainfall >= 30.0:
        rainfall_output = "💚강수량: 비가 너무많이와요!! 우산과 샌들은 필수!!"
    else:
        rainfall_output = "💚강수량: 자료없음"
    #미세먼지
    if dust <=30:
        dust_output =  "💙미세먼지: 좋음!"
    elif dust <= 80:
        dust_output =  "💙미세먼지: 보통!"
    elif dust <= 150:
        dust_output =  "💙미세먼지: 나쁨! 외출주의"
    elif dust > 150:
        dust_output =  "💙미세먼지: 매우나쁨 KF94필수.."
    else:
        dust_output =  "💙미세먼지: 자료없음"
    #초미세먼지
    if ultraDust <= 15:
        ultraDust_output = "💜초미세먼지: 좋음! "
    elif ultraDust <= 35:
        ultraDust_output = "💜초미세먼지: 보통! 피크닉하기에 좋은날!!"
    elif ultraDust <= 75:
        ultraDust_output = "💜초미세먼지: 나쁨! 마스크 꼭 착용!"
    elif ultraDust > 75:
        ultraDust_output = "💜초미세먼지: 매우 나쁨! 창문닫고외출하시고 마스크 꼭 착용!!"
    else:
        ultraDust_output = "💜초미세먼지: 자료없음"
    output = [temp_output, humidity_output, wind_output, rainfall_output, dust_output,ultraDust_output]
    #한칸씩 띄어주기위한코드
    output_str = "\n".join(output)
    return output_str
browser.quit() 

data = {
    'area': area,
    'realTime':realTime,
    'temp_diff':temp_diff,
    'temp': temp,
    'maxTemp': maxTemp,
    'minTemp': minTemp,
    'actualTemp': actualTemp,
    'temp_diff': temp_diff,
    'humidity': humidity,
    'wind': wind,
    'rainfall': rainfall,
    'ultraDust': ultraDust,
    'dust': dust,
}

output_str = totalWeather(data['temp'], data['humidity'], data['wind'], data['rainfall'], data['dust'], data['ultraDust'])
css_file="./main.css"
html_template = '''
<!DOCTYPE html>
<html lang="kr">
<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
	<!-- CSS only -->
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet"
	integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
	<link rel="stylesheet" href="main.css">
	<title>Weather</title>

</head>
<body>
	<div>
		<h1>
			<span class="material-icons">nights_stay</span>
			오늘의 날씨 정보
			<span class="material-icons" style="margin-left: 8px">nights_stay</span>
		</h1>

	</div>
	<div class="data container">
		<div class="databox container">
			<div class="totalWeather container">
                <h1 style="margin:0">총평</h1>
                <pre class="totalText"><p>{output_str}</p></pre>
            </div>
            <div class="row">
				<div class="col-12">
					<div class="card">
						<h2>지역: {area}</h2>
                        <h4>{realTime}</h4><br>
						<h2>{temp_diff}</h2><br>
					</div>
				</div>
			</div>
			<div class="row">
				<div class="col-3">
					<div class="card">
						<span class="material-icons">thermostat</span>
						<h3>현재기온</h3>
						<p class="temp">{temp}℃</p>
					</div>
				</div>
				<div class="col-3">
					<div class="card">
						<span class="material-icons">self_improvement</span>
						<h3>체감온도</h3>
						<p class="actualTemp">{actualTemp}</p>
					</div>
				</div>
				<div class="col-3">
					<div class="card">
						<span class="material-icons">south</span>
						<h3>최저온도</h3>
						<p class="minTemp">{minTemp}</p>
					</div>
				</div>
				<div class="col-3">
					<div class="card">
						<span class="material-icons">north</span>
						<h3>최고온도</h3>
						<p class="maxTemp">{maxTemp}</p>
					</div>
				</div>
			</div>
			<div class="row">
				<div class="col-4">
					<div class="card ">
						<span class="material-icons">
							thunderstorm
						</span>
						<h3>강수량</h3>
						<p class="rainfall">{rainfall}mm</p>
					</div>
				</div>
				<div class="col-4">
					<div class="card ">
						<span class="material-icons">
							water_drop
						</span>
						<h3>습도</h3>
						<p class="humidity">{humidity}</p>
					</div>
				</div>
				<div class="col-4">
					<div class="card">
						<span class="material-icons">
							air
						</span>
						<h3>바람</h3>
						<p class="wind">{wind}m/s</p>
					</div>
				</div>
			</div>
			<div class="row">
				<div class="col-4">
					<div class="card ">
						<span class="material-icons">
							masks
						</span>
						<h3>미세먼지</h3>
						<p class="dust">{dust}㎍/m³</p>
					</div>
				</div>
				<div class="col-4">
					<span id="cloud" class="material-icons">wb_sunny</span>
				</div>
				<div class="col-4">
					<div class="card ">
						<span class="material-icons" style="color: red;">
							masks
						</span>
						<h3>초미세먼지</h3>
						<p class="ultraDust">{ultraDust}㎍/m³</p>
					</div>
				</div>
			</div>
		</div>

	</div>
	<p class="copyright">Copyright 2023. DongYang Univ, Project Team <b>tmp</b> all rights reserved.</p>
</body>

</html> 
'''

# 데이터를 HTML 템플릿에 적용
html_output = html_template.format(
    area=data['area'],
    realTime=data['realTime'],
    temp_diff=data['temp_diff'],
    temp=data['temp'],
    actualTemp=data['actualTemp'],
    minTemp=data['minTemp'],
    maxTemp=data['maxTemp'],
    rainfall=data['rainfall'],
    humidity=data['humidity'],
    wind=data['wind'],
    dust=data['dust'],
    ultraDust=data['ultraDust'],
    output_str=output_str,
    css_file="./main.css"
)

# HTML 파일로 저장
with open('weather.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

webbrowser.open('weather.html')
