import requests
import xml.etree.ElementTree as ET
import sqlite3

print("법정동 코드를 찾기 위해 시도명과 시군구명, 읍면동을 입력해주세요(읍면동이 없다면 null을 적어주세요)")

si_do=input()
si_gun_gu=input()
eup_myeon_dong=input()


conn = sqlite3.connect("C:\\Users\\jin\\Desktop\\project_db\\houseprice.db")
cursor = conn.cursor()
conn.commit()


Query_String = ("SELECT 법정동코드,시도명, 시군구명,읍면동명, 리명 "
                "FROM houseprice "
                "WHERE 시도명=? and 시군구명=? AND 읍면동명=?")
result = conn.execute(Query_String, (si_do, si_gun_gu, eup_myeon_dong))


rows = result.fetchall()
for row in rows[:30] :
        print(row)

conn.close()



region_code=int(input("지역의 법정동코드를 입력하세요")) 
main_address=int(input("주택의 본번을 입력하세요"))
sub_address=int(input("주택의 부번를 입력하세요(부번이 없다면 0을 입력하세요)"))

PNU=region_code*1000000000+1000000000+main_address*10000+sub_address

print(PNU)

url = 'http://apis.data.go.kr/1611000/nsdi/ApartHousingPriceService/attr/getApartHousingPriceAttr'
params = {
    'serviceKey': '5SiDUErdPC83iL38EVuWg9axGc84BA2kGpUEZZScZNga1qVd3+RXXZ8KhZ7dxUp4dZkZRe8ZpKUxTMGQkpSJVw==',
    'pnu': PNU,
    'stdrYear': '2023',
    'format': 'XML',
    'numOfRows': '10',
    'pageNo': '1'
}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raises HTTPError for bad responses
    xml_text = response.text

    # XML 파싱
    root = ET.fromstring(xml_text)

    # 필요한 정보 추출
    for field in root.findall('.//field'):
        ldCodeNm = field.find('ldCodeNm').text
        aphusNm = field.find('aphusNm').text
        prvuseAr = field.find('prvuseAr').text
        pblntfPc = field.find('pblntfPc').text

        print(f"지역명: {ldCodeNm}, 공동주택명: {aphusNm}, 전용면적: {prvuseAr}, 공시가격: {pblntfPc}")

except requests.exceptions.RequestException as e:
    print(f"Error in request: {e}")
except ET.ParseError as e:
    print(f"Error in XML parsing: {e}")