"""
문제들
1.바람 소수점까지안나옴 0.7 -> 0.0 으로나옴
2.먼지 if루프 안돌음
"""

# 정규식(regular expression) 쉽게 문자열에서 패턴에 해당하는 부분을 추출
import re
# 동적크롤링(스크래핑)
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont
import sys

# url연결
url = "https://www.weather.go.kr/w/index.do"
# Edge브라우저 및 get요청
browser = webdriver.Chrome()
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
# 20초동안 창을 켜둬서 내가 원하는지역검색후에 가만히 두면 크롤링됨(시간변경가능)
time.sleep(5)

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
wind_str = browser.find_element(By.CSS_SELECTOR,'div.cmp-cur-weather.wbg.wbg-type2.BGDB00 > ul > li:nth-child(2) > span.val').text
wind = float(re.findall('\d+\.\d+', wind_str)[0])

# 강수량
rainfall_str = items[2].find_element(By.CLASS_NAME, 'val').text
# rainfall = float(re.findall('\d+', rainfall_str)[0])
rainfall = float_extract_number(rainfall_str)

# 초미세먼지
ultraDust = int(browser.find_element(By.CSS_SELECTOR,
                'span.air-lvv').get_attribute('textContent'))
# ultraDust = extract_number(ultraDust)
# 미세먼지
dust_str = browser.find_element(By.CSS_SELECTOR,
        'ul.wrap-2.air-wrap.no-underline > li:nth-child(2) > strong.air-level.val > span > span.air-lvv').get_attribute('textContent')
dust = int_extract_number(dust_str)
print(type(dust))
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
    if humidity >= 30 and humidity <= 60:
        return ["습도적당! 쾌적~~", "기쁜표정.png"]
    elif humidity < 30:
        return ["습도낮음! 물과보습 필수!", "슬픈표정.png"]
    elif humidity > 60:
        return ["습도높음! 불쾌지수업!!", "놀란표정.png"]
    else:
        return ["자료없음"]

# 현재 바람 정보에 따른 출력
def fWind(wind):
    if wind < 0.3:
        return ["이정도면 바람이 안부네요!", "기쁜표정.png"]
    elif wind >= 0.3 and wind <= 1.5:
        return ["실바람이 불어요!", "기쁜표정.png"]
    elif wind >= 1.6 and wind <= 3.3:
        return ["남실바람이 불어요!", "슬픈표정.png"]
    elif wind >= 3.4 and wind <= 5.4:
        return ["산들바람이 불어요!", "놀란표정.png"]
    else:
        return ["바람이 강하니 외출을 자제해주세요!", "놀란표정.png"]
# 현재 강수량 정보에 따른 출력
def fRainfall(rainfall):
    if rainfall == 0:
        return ["오늘은 비가 안와요!", "기쁜표정.png"]
    elif rainfall < 3.0:
        return ["약한 비가 와요!", "슬픈표정.png"]
    elif rainfall >= 3.0 and rainfall < 15.0:
        return ["적당한 비가 내려요!", "슬픈표정.png"]
    elif rainfall >= 15.0:
        return ["강한 비가 내리니 외출을 자제하세요!", "놀란표정.png"]
    elif rainfall >= 30.0:
        return ["매우 강한 비가 내리니 외출하지마세요!", "놀란표정.png"]
    else:
        print("자료없음")

# 현재 초미세먼지 정보에 따른 출력
def fUltra(ultraDust):
    if ultraDust >= 0:
        return ["초미세먼지 좋음!", "기쁜표정.png"]
    elif ultraDust >= 16:
        return ["초미세먼지 보통!", "기쁜표정.png"]
    elif ultraDust >= 36:
        return ["초미세먼지 나쁨!", "슬픈표정.png"]
    elif ultraDust >= 76:
        return ["초미세먼지 매우 나쁨!", "놀란표정.png"]
    else:
        return ["자료없음"]

# 현재 미세먼지 정보에 따라 출력
def fDust(dust):
    if dust >= 0:
        return ["미세먼지 좋음!", "기쁜표정.png"]
    elif dust >= 31:
        return ["미세먼지 보통!", "기쁜표정.png"]
    elif dust >= 81:
        return ["미세먼지 나쁨!", "슬픈표정.png"]
    elif dust >= 151:
        return ["미세먼지 매우나쁨 KF94필수..", "놀란표정.png"]
    else:
        return ["자료없음"]

# 총평
""" def fDress(temp):
    if temp >= 28:
        return "더위가 매우 심하니 민소매, 반팔, 반바지, 린넨 옷을 입는 것을 추천합니다. 외출활동을 자제하는 것을 권장해요."
    elif temp >= 23:
        return "더운 여름 날씨예요. 반팔, 얇은 셔츠, 반바지, 면바지를 입는 것을 추천해요. 주변 공원에서 피크닉을 즐기는 것은 어떨까요?"
    elif temp >= 20:
        return "블라우스, 긴팔 티, 면바지, 슬랙스를 입는 것을 추천해요. 조금 더운 여름 날씨예요. 낮 시간에도 그리 덥지 않으니 주변 공원에 피크닉을 다녀오는 것은 어떨까요?"
    elif temp >= 17:
        return "따듯한 날씨에는 얇은 가디건이나 니트, 맨투맨, 후드, 긴 바지를 입는 것을 추천해요. 다양한 스타일로 즐길 수 있는 날씨예요."
    elif temp >= 12:
        return "일교차가 커지는 시기예요. 자켓, 가디건, 청자켓, 니트, 청바지를 입는 것을 추천해요. 따듯한 겉옷을 챙겨 다니는 것은 어떨까요?"
    elif temp >= 9:
        return "트렌치코트, 야상, 점퍼, 기모 바지를 입는 것을 추천해요. 오늘같은 날씨가 아니면 입기 힘든 트렌치코트를 입어보는건 어떨까요?"
    elif temp >= 5:
        return "추위가 시작되거나 끝나가는 시기예요. 울 코트, 히트텍, 가죽 옷, 기모 옷을 입는 것을 추천해요. 이런 날씨엔 감기에 걸리기 쉬우니 따듯하게 입고 가는건 어떨까요?"
    else:
        return "한겨울이라 추우니 패딩, 두꺼운 코트, 누빔 옷, 기모, 목도리를 입는 것을 추천해요. 체온 유지를 위해 잠깐 패션을 포기하는 건 어떨까요?"
"""
def totalWeather(temp,humidity,wind,rainfall,dust,ultraDust):
    if temp >= 32.0:
        temp_output = "매우덥습니다! 반팔,반바지,샌들을 추천합니다."
    elif temp >= 28.0:
        temp_output = "더위가 매우 심하니 민소매, 반팔, 반바지, 린넨 옷을 입는 것을 추천합니다."
    elif temp >= 23.0:
        temp_output = "반팔, 얇은 셔츠, 반바지, 면바지를 입는 것을 추천해요. "
    elif temp >= 20.0:
        temp_output = "블라우스, 긴팔 티, 면바지, 슬랙스를 입는 것을 추천해요."
    elif temp >= 17.0:
        temp_output = "따듯한 날씨에는 얇은 가디건이나 니트, 맨투맨, 후드, 긴 바지를 입는 것을 추천해요. "
    elif temp >= 12.0:
        temp_output = "일교차가 커지는 시기예요. 자켓, 가디건, 청자켓, 니트, 청바지를 입는 것을 추천해요."
    elif temp >= 9.0:
        temp_output = "트렌치코트, 야상, 점퍼, 기모 바지를 입는 것을 추천해요.!"
    elif temp >= 5.0:
        temp_output = "울 코트, 히트텍, 가죽 옷, 기모 옷을 입는 것을 추천해요."
    else:
        return "패딩, 두꺼운 코트, 누빔 옷, 기모, 목도리를 입는 것을 추천해요."
    if humidity >= 30 and humidity <= 60:
        humidity_output = "습도적당! 쾌적~~"
    elif humidity < 30:
        humidity_output = "습도낮음! 물과보습 필수!"
    elif humidity > 60:
        humidity_output ="습도높음! 불쾌지수업!!"
    else:
        humidity_output = "자료없음"
    if wind < 0.3:
        wind_output = "바람이 거의안불어요! 앞머리 안날리는날!"
    elif wind >= 0.3 and wind <= 1.5:
        wind_output = "바람이 조금불어요! 앞머리 지킬수있어요!"
    elif wind >= 1.6 and wind <= 3.3:
        wind_output = "조금강한 바람이 불어요.앞머리 주의!!"
    elif wind >= 3.4 and wind <= 5.4:
        wind_output = "강한바람이 불어요! 앞머리주의!!"
    else:
        wind_output = "태풍인가..!? 외출자제해주세요!!"
# 현재 강수량 정보에 따른 출력
    if rainfall == 0:
        rainfall_output = "오늘은 비가 안와요!"
    elif rainfall < 3.0:
        rainfall_output = "약한 비가 와요! 혹시모르니 우산챙기세요!"
    elif rainfall >= 3.0 and rainfall < 15.0:
        rainfall_output = "우산 꼭 챙기기!!"
    elif rainfall >= 15.0:
        rainfall_output = "비가많이오네요!! 우산 꼭 챙기기!!"
    elif rainfall >= 30.0:
        rainfall_output = "비가 너무많이와요!! 우산과 샌들은 필수!!"
    else:
        rainfall_output = "자료없음"
    if dust >= 0:
        dust_output =  "미세먼지 좋음!"
    elif dust >= 31:
        dust_output =  "미세먼지 보통!"
    elif dust >= 81:
        dust_output =  "미세먼지 나쁨!"
    elif dust >= 151:
        dust_output =  "미세먼지 매우나쁨 KF94필수.."
    else:
        dust_output =  "자료없음"
    if ultraDust >= 0:
        ultraDust_output = "초미세먼지 좋음! 오랜만에 이런날씨가"
    elif ultraDust >= 16:
        ultraDust_output = "초미세먼지 보통! 피크닉하기에 좋은날!!"
    elif ultraDust >= 36:
        ultraDust_output = "초미세먼지 나쁨! 마스크 꼭 착용!"
    elif ultraDust >= 76:
        ultraDust_output = "초미세먼지 매우 나쁨! 창문닫고외출하시고 마스크 꼭 착용!!"
    else:
        ultraDust_output = "자료없음"

    output = [temp_output, humidity_output, wind_output, rainfall_output, ultraDust_output, dust_output]
    output_str = "\n".join(output)
    return output_str

browser.quit()
# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("UIdesign.ui")[0]

# 화면을 띄우는데 사용되는 Class 선언


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #폰트
        font = QFont('Arial', 12)
        font.setBold(True)
        self.area_data.setFont(font)
        self.temp_diff_data.setFont(font)
        self.currentTemp.setFont(font)
        self.maxTemp.setFont(font)
        self.minTemp.setFont(font)
        self.actTemp.setFont(font)
        self.fhumidity_data.setFont(font)
        self.fhumidity_comm.setFont(font)
        self.wind_data.setFont(font)
        self.wind_comm.setFont(font)
        self.rain_data.setFont(font)
        self.rain_comm.setFont(font)
        self.dust_data.setFont(font)
        self.dust_comm.setFont(font)
        self.udust_data.setFont(font)
        self.udust_comm.setFont(font)
        font2 = QFont('Arial',10)
        font2.setBold(True)
        self.dress_comm.setFont(font2)
        

        #이미지부분----------------
        self.image_data2 = self.findChild(QLabel, "label_2")
        self.image_data2.setPixmap(QPixmap(fHumidity(humidity)[1]))

        self.image_data3 = self.findChild(QLabel, "label_3")
        self.image_data3.setPixmap(QPixmap(fWind(wind)[1]))

        self.image_data5 = self.findChild(QLabel, "label_5")
        self.image_data5.setPixmap(QPixmap(fRainfall(rainfall)[1]))

        self.image_data6 = self.findChild(QLabel, "label_6")
        self.image_data6.setPixmap(QPixmap(fUltra(ultraDust)[1]))

        self.image_data7 = self.findChild(QLabel, "label_7")
        self.image_data7.setPixmap(QPixmap(fDust(dust)[1]))


        #------------------------------
        #지역명
        self.area_data = self.findChild(QLabel, "area_data")
        self.area_data.setText(area)
        #어제보다 몇도높은지부분
        self.temp_diff_data = self.findChild(QLabel, "temp_diff_data")
        self.temp_diff_data.setText(temp_diff)
        #현재온도
        self.currentTemp = self.findChild(QLabel, "currentTemp")
        self.currentTemp.setText(str(temp))
        #최고온도
        self.maxTemp = self.findChild(QLabel, "maxTemp")
        self.maxTemp.setText(maxTemp)
        #최저온도
        self.minTemp = self.findChild(QLabel, "minTemp")
        self.minTemp.setText(fMinTemp(minTemp))
        #체감온도
        self.actTemp = self.findChild(QLabel, "actTemp")
        self.actTemp.setText(actualTemp)
        #습도
        self.fhumidity_data = self.findChild(QLabel, "fhumidity_data")
        self.fhumidity_data.setText(str(humidity))
        #습도멘트
        self.fhumidity_comm = self.findChild(QLabel, "fhumidity_comm")
        self.fhumidity_comm.setText(fHumidity(humidity)[0])
        #바람
        self.wind_data = self.findChild(QLabel, "wind_data")
        self.wind_data.setText(str(wind))
        #바람멘트
        self.wind_comm = self.findChild(QLabel, "wind_comm")
        self.wind_comm.setText(fWind(wind)[0])
        #강수량
        self.rain_data = self.findChild(QLabel, "rain_data")
        self.rain_data.setText(str(rainfall))
        #강수량멘트
        self.rain_comm = self.findChild(QLabel, "rain_comm")
        self.rain_comm.setText(fRainfall(rainfall)[0])
        #미세먼지데이터
        self.dust_data = self.findChild(QLabel, "dust_data")
        self.dust_data.setText(str(dust))
        #미세먼지멘트
        self.dust_comm = self.findChild(QLabel, "dust_comm")
        self.dust_comm.setText(fDust(dust)[0])
        #초미세먼지데이터
        self.udust_data = self.findChild(QLabel, "udust_data")
        self.udust_data.setText(str(ultraDust))
        #초미세먼지멘트
        self.udust_comm = self.findChild(QLabel, "udust_comm")
        self.udust_comm.setText(fUltra(ultraDust)[0])
        #총데이터
        self.dress_comm = self.findChild(QLabel, "dress_comm")
        self.dress_comm.setText(totalWeather(temp,humidity,wind,rainfall,dust,ultraDust))

if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()