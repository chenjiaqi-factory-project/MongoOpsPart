import os
import requests

if __name__ == '__main__':

    record = {
        "boiler_room": "地点A",
        "boiler_no": "1号锅炉",
        "datetime": "2019-8-25 18:23:22",
        "date": "2019-09-03",
        "time": "18:23:22",
        "gas_indicator": "7662827.827",
        "gas_consumption": "233.233",
        "employee_no": "EN0136"
    }

    result = requests.post("http://127.0.0.1:4999/api/gas/document",
                           data=record)

    # record2 = {
    #     "factory_no": "工厂A",
    #     "datetime": "2019-09-02 18:23:22",
    #     "date": "2019-8-25",
    #     "time": "18:23:22",
    #     "elec_indicator": "762817.827",
    #     "elec_consumption": "233.233",
    #     "water_indicator": "762817.827",
    #     "water_consumption": "233.233",
    #     "water_out_temperature": "80",
    #     "water_in_temperature": "23",
    #     "employee_no": "EN0136"
    # }
    #
    # result = requests.post("http://127.0.0.1:4999/api/water-elec/document",
    #                        data=record2)

    print(result)

    pass


