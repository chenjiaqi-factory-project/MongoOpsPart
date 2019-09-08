import os
import requests

if __name__ == '__main__':

    # record = {
    #     "boiler_room": "地点A",
    #     "boiler_no": "1号锅炉",
    #     "datetime": "2019-09-05 19:24:22",
    #     "date": "2019-09-05",
    #     "time": "19:24:22",
    #     "gas_indicator": "7688607.827",
    #     "employee_no": "EN0136"
    # }
    #
    # result = requests.post("http://127.0.0.1:5000/api/gas/document",
    #                        data=record)

    j = '2019-09-04' < '2019-09-05' or '2019-09-04' > '2019-09-05'
    print(j)

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

    # gas_dict_1 = {'date': '2019-08-23'}
    # gas_dict_2 = {'date': '2019-08-21'}
    # gas_dict_3 = {'date': '2019-08-22'}
    # test_list = list()
    # test_list.append(gas_dict_1)
    # test_list.append(gas_dict_2)
    # test_list.append(gas_dict_3)
    # # Way Of sorting list of dict
    # sorted_list = sorted(test_list, key=lambda doc: doc['date'])
    #
    # print(sorted_list)

    pass


