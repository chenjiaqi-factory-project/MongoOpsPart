import os
import requests

if __name__ == '__main__':

    record = {
        "location": "地点A",
        "datetime": "2019-8-25 18:23:22",
        "boiler_no": "1号锅炉",
        "gas_consumption": "233.233",
        "elec_consumption": "666.666",
        "water_consumption": "41.1",
        "water_out_temperature": "89.2",
        "water_in_temperature": "32.4",
        "employee_no": "0136 号员工"
    }

    result = requests.post("http://127.0.0.1:5000/api/document",
                           data=record)

    print(result)

    pass


