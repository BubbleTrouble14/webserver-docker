import requests
import psycopg2
import xml.etree.ElementTree as ET
from datetime import datetime

# def parse(data):

#     root = ET.fromstring(data)
#     data = []
#     date = datetime.today().date()
#     for child in root[2][0]:
#         data.append(
#             (
#                 date,
#                 child.attrib.get("currency"),
#                 float(child.attrib.get('rate'))
#             )
#         )
#     return data

def main():
    print("Hello")
    # pgdb_connection = psycopg2.connect(user="postgres",
    #                             password="postgres",
    #                             host="chia_pgdb",
    #                             port="5432",
    #                             database="chiadb")

    # cursor_1 = pgdb_connection.cursor()

    # response = requests.get("https://api.coingecko.com/api/v3/coins/chia?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false")
    # if(response.status_code == 200):
    #     data = response.json()
    #     usd_price = data['market_data']['current_price']['usd']
    #     # print(usd_price, datetime.today().date())
    #     cursor_1.execute(
    #         "INSERT INTO coin_price (p_date, price) VALUES(%s, %s)",
    #         (
    #             datetime.today().date(),
    #             usd_price
    #         )
    #     )

    # pgdb_connection.commit()
    # cursor_1.close()

    # cursor_2 = pgdb_connection.cursor()

    # xml_response = requests.get("http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml")
    # if(xml_response.status_code == 200):
    #     cursor_2.executemany(
    #         "INSERT INTO exchange_rate (x_date, currency, rate) VALUES(%s, %s, %s)",
    #         parse(xml_response.content),
    #     )

    # pgdb_connection.commit()
    # cursor_2.close()

    # pgdb_connection.close()

main()