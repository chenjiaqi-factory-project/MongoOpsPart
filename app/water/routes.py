from app import app, mongo
from app.water import bp
from flask import jsonify
from flask import request, url_for, redirect
from werkzeug.http import HTTP_STATUS_CODES
from bson.objectid import ObjectId
from func_pack import create_rec_hash, get_api_info, get_api_info_first
from config import Config
import requests


# Get all water document infos
@bp.route("/document/all-documents", methods=['GET'])
def get_all_water_documents():
    data = list()
    # the name of collection is called 'Collection'
    for record in mongo.db.Water_Collection.find():
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get water one document info by its _id
@bp.route("/document/rid/<string:rid>", methods=['GET'])
def get_water_document_by__id(rid):
    data = list()
    # Type 'ObjectId' in Pymongo come from bson.objectid.ObjectId
    oid = ObjectId(rid)
    # the _id is unique
    record = mongo.db.Water_Collection.find_one_or_404({"_id": oid})
    record['_id'] = str(record['_id'])
    data.append(record)
    return jsonify(data)


# Insert new document infos
@bp.route("/document", methods=['POST'])
def insert_water_new_document():
    # assemble a dict
    new_document = dict()
    new_document['document_hash'] = create_rec_hash()
    new_document['factory_no'] = request.form.get('factory_no')
    new_document['date'] = request.form.get('date')
    new_document['time'] = request.form.get('time')
    new_document['datetime'] = request.form.get('datetime')
    new_document['water_indicator'] = request.form.get('water_indicator')
    # new_document['water_out_temperature'] = request.form.get('water_out_temperature')
    # new_document['water_in_temperature'] = request.form.get('water_in_temperature')
    new_document['employee_no'] = request.form.get('employee_no')

    oid = mongo.db.Water_Collection.insert_one(new_document).inserted_id
    rid = str(oid)

    # return redirect(url_for('get_competition_by__id', rid=rid))
    # return the success info
    return get_water_document_by__id(rid=rid)


# Mention that all items are list type in this way
# # Insert new competition infos
# @app.route("/api/competition", methods=['POST'])
# def insert_new_competition():
#     # Here are the right way to write NoSQL receiver
#     new_competition = dict(request.form)
#
#     oid = mongo.db.Competition.insert_one(new_competition).inserted_id
#     rid = str(oid)
#
#     # return redirect(url_for('get_competition_by__id', rid=rid))
#     # return the success info
#     return get_competition_by__id(rid=rid)


# Modify an existed document info
@bp.route("/document/<string:rid>", methods=['PUT'])
def update_water_document(rid):
    # assemble a dict
    mod_document = dict()
    mod_document['document_hash'] = request.form.get('document_hash')
    mod_document['factory_no'] = request.form.get('factory_no')
    mod_document['date'] = request.form.get('date')
    mod_document['time'] = request.form.get('time')
    mod_document['datetime'] = request.form.get('datetime')
    mod_document['water_indicator'] = request.form.get('water_indicator')
    # mod_document['water_out_temperature'] = request.form.get('water_out_temperature')
    # mod_document['water_in_temperature'] = request.form.get('water_in_temperature')
    mod_document['employee_no'] = request.form.get('employee_no')

    # pymongo update dict structure
    set_dict = {"$set": mod_document}

    oid = ObjectId(rid)
    mongo.db.Water_Collection.update_one({"_id": oid}, set_dict)

    # return the success info
    return get_water_document_by__id(rid=rid)


# Delete an existed water document info
@bp.route("/document/<string:rid>", methods=['DELETE'])
def delete_water_document(rid):
    set_dict = dict()
    oid = ObjectId(rid)
    set_dict['_id'] = oid
    mongo.db.Water_Collection.delete_one(set_dict)
    data = [{'_id': rid, 'deleted status': 'success'}]
    return jsonify(data)


# Get document info by its name in fuzzy mode
@bp.route("/document/factory-no/fuzzy/<string:factory_no>", methods=['GET'])
def get_water_document_by_factory_no_fuzzy(factory_no):
    data = list()
    # using fuzzy mode with regex
    for record in mongo.db.Water_Collection.find({"factory_no": {'$regex': factory_no}}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get water document by its employee_no in fuzzy mode
@bp.route("/document/employee-no/fuzzy/<string:employee_no>", methods=['GET'])
def get_water_document_by_employee_no_fuzzy(employee_no):
    data = list()
    # maybe the employee_no in different items are same
    for record in mongo.db.Water_Collection.find({"employee_no": {'$regex': employee_no}}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get document by its datetime in fuzzy mode
@bp.route("/document/datetime/fuzzy/<string:datetime>", methods=['GET'])
def get_water_document_by_datetime_fuzzy(datetime):
    data = list()
    # maybe the datetime in different items are same
    for record in mongo.db.Water_Collection.find({"datetime": {'$regex': datetime}}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get document by its date in fuzzy mode
@bp.route("/document/date/fuzzy/<string:date>", methods=['GET'])
def get_water_document_by_date_fuzzy(date):
    data = list()
    # maybe the data_feature in different items are same
    for record in mongo.db.Water_Collection.find({"date": {'$regex': date}}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get document by its factory_no and date
# Mention! There is no 'fuzzy mode' in this function
@bp.route("/document/factory-no-and-datetime"
          "/<string:factory_no>/<string:date>", methods=['GET'])
def get_water_document_by_factory_no_and_date(factory_no, date):
    data = list()
    data_search = list()
    # 'date' field may contain many records
    for record in mongo.db.Water_Collection.find({"date": {'$regex': date}}):
        record['_id'] = str(record['_id'])
        data_search.append(record)
    # search the factory_no field in the 'data_search' list
    for document in data_search:
        if factory_no == document['factory_no']:
            data.append(document)
    return jsonify(data)


# Water Calculating Functions by a exact given date
@bp.route("/calculating/water-consumption/exact-date/<string:factory_no>"
          "/<string:first_date>/<string:last_date>", methods=['GET'])
def calculate_water_consumption_by_given_date(first_date, last_date, factory_no):
    data = list()
    result_dict = {}
    # assemble url
    search_first_url = 'http://' + Config.LOCALHOST_IP_PORT + \
                       url_for('water.get_water_document_by_factory_no_and_date', factory_no=factory_no,
                               date=first_date)
    search_last_url = 'http://' + Config.LOCALHOST_IP_PORT + \
                      url_for('water.get_water_document_by_factory_no_and_date', factory_no=factory_no,
                              date=last_date)
    first_date_doc_list = get_api_info(requests.get(search_first_url))
    last_date_doc_list = get_api_info(requests.get(search_last_url))
    # if all things are correct
    if len(first_date_doc_list) >= 1 and len(last_date_doc_list) >= 1:
        first_doc = first_date_doc_list[0]
        last_doc = last_date_doc_list[0]
        water_consumption = round(float(first_doc['water_indicator']) - float(last_doc['water_indicator']), 3)
        if water_consumption > 0:
            water_consumption_type = '减少'
        elif water_consumption == 0:
            water_consumption_type = '持平'
        else:
            water_consumption_type = '增加'
        result_dict['water_consumption'] = abs(water_consumption)
        result_dict['water_consumption_type'] = water_consumption_type
        result_dict['first_document'] = first_doc
        result_dict['last_document'] = last_doc
    # else Cannot find all relative document
    elif len(first_date_doc_list) < 1 and len(last_date_doc_list) < 1:
        result_dict['water_consumption'] = 0
        result_dict['water_consumption_type'] = '错误'
        result_dict['first_document'] = None
        result_dict['last_document'] = None
    # else Cannot find first relative document
    elif len(first_date_doc_list) < 1:
        last_doc = last_date_doc_list[0]
        result_dict['water_consumption'] = 0
        result_dict['water_consumption_type'] = '错误'
        result_dict['first_document'] = None
        result_dict['last_document'] = last_doc
    # else Cannot find last relative document
    elif len(last_date_doc_list) < 1:
        first_doc = first_date_doc_list[0]
        result_dict['water_consumption'] = 0
        result_dict['water_consumption_type'] = '错误'
        result_dict['first_document'] = first_doc
        result_dict['last_document'] = None
    # return result
    data.append(result_dict)
    return jsonify(data)


# Water Calculating by given factory_no successively
@bp.route("/calculating/water-consumption/successive/<string:factory_no>", methods=['GET'])
def calculate_water_consumption_successive_by_factory_no(factory_no):
    data = list()
    # assemble url
    search_url = 'http://' + Config.LOCALHOST_IP_PORT + \
                 url_for('water.get_water_document_by_factory_no_fuzzy', factory_no=factory_no)
    search_list = get_api_info(requests.get(search_url))

    # if there are at least 2 docs, that's mean it can be calculated
    if len(search_list) >= 2:
        # sorted by date
        search_list = sorted(search_list, key=lambda doc: doc['datetime'])
        flag = 1
        while flag < len(search_list):
            result_dict = {}
            consumption = round(float(search_list[flag - 1]['water_indicator'])
                                    - float(search_list[flag]['water_indicator']), 3)
            if consumption > 0:
                consumption_type = '减少'
            elif consumption == 0:
                consumption_type = '持平'
            else:
                consumption_type = '增加'
            result_dict['water_consumption'] = abs(consumption)
            result_dict['water_consumption_type'] = consumption_type
            result_dict['first_document'] = search_list[flag - 1]
            result_dict['last_document'] = search_list[flag]
            data.append(result_dict)
            # flag add 1
            flag += 1
    elif len(search_list) == 1:
        error_dict = {}
        error_dict['water_consumption'] = 0
        error_dict['water_consumption_type'] = '只有一条数据'
        error_dict['first_document'] = search_list[0]
        error_dict['last_document'] = search_list[0]
        data.append(error_dict)
    else:
        error_dict = {}
        error_dict['water_consumption'] = 0
        error_dict['water_consumption_type'] = '错误'
        error_dict['first_document'] = None
        error_dict['last_document'] = None
        data.append(error_dict)
    # return result
    return jsonify(data)


# Water Calculating Functions by a inexact given date
@bp.route("/calculating/water-consumption/inexact-date/<string:factory_no>"
          "/<string:first_date>/<string:last_date>", methods=['GET'])
def calculate_water_consumption_by_inexact_date(first_date, last_date, factory_no):
    data = list()
    # assemble url
    search_url = 'http://' + Config.LOCALHOST_IP_PORT + \
                 url_for('water.calculate_water_consumption_successive_by_factory_no', factory_no=factory_no)
    # search list has been sorted!!
    search_list = get_api_info(requests.get(search_url))
    if len(search_list) >= 1:
        if search_list[0]['water_consumption_type'] != '错误':
            doc_list = list()
            for consumption_dict in search_list:
                doc_list.append(consumption_dict['first_document'])
                doc_list.append(consumption_dict['last_document'])
            # scale date
            successive_list = list()
            for doc in doc_list:
                # pop item
                if doc['date'] >= first_date and doc['date'] <= last_date:
                    successive_list.append(doc)
            print(successive_list)
            # this list only include gas_doc whose date in the scale you given
            if len(successive_list) >= 1:
                result_dict = {}
                consumption = round(float(successive_list[0]['water_indicator'])
                                        - float(successive_list[-1]['water_indicator']), 3)
                if consumption > 0:
                    consumption_type = '减少'
                elif consumption == 0:
                    consumption_type = '持平'
                else:
                    consumption_type = '增加'
                result_dict['water_consumption'] = abs(consumption)
                result_dict['water_consumption_type'] = consumption_type
                result_dict['first_document'] = successive_list[0]
                result_dict['last_document'] = successive_list[-1]
                data.append(result_dict)
            else:
                error_dict = {}
                error_dict['water_consumption'] = 0
                error_dict['water_consumption_type'] = '日期区间错误'
                error_dict['first_document'] = None
                error_dict['last_document'] = None
                data.append(error_dict)
        else:
            data = search_list
    return jsonify(data)


# Water Calculating by given factory_no successively
@bp.route("/calculating/water-consumption/successive/<string:factory_no>"
          "/<string:first_date>/<string:last_date>", methods=['GET'])
def calculate_water_consumption_successive_by_factory_no_and_date(factory_no, first_date, last_date):
    data = list()
    # assemble url
    search_url = 'http://' + Config.LOCALHOST_IP_PORT + \
                 url_for('water.calculate_water_consumption_successive_by_factory_no', factory_no=factory_no)
    # search list has been sorted!!
    search_list = get_api_info(requests.get(search_url))
    if len(search_list) > 1:
        for doc_dict in search_list:
            if doc_dict['first_document']['date'] >= first_date and doc_dict['last_document']['date'] <= last_date:
                data.append(doc_dict)
    else:
        error_dict = {}
        error_dict['water_consumption'] = 0
        error_dict['water_consumption_type'] = '错误'
        error_dict['first_document'] = None
        error_dict['last_document'] = None
        data.append(error_dict)
        # return search result
    return jsonify(data)


# Fuzzy Search by factory_no, employee_no, boiler_room or datetime
@bp.route("/document/doc-search/fuzzy/<string:keyword>", methods=['GET'])
def search_water_document_fuzzy_single_keyword(keyword):
    data = list()
    search_list = list()
    search_list.append({'factory_no': {'$regex': keyword}})
    search_list.append({'employee_no': {'$regex': keyword}})
    search_list.append({'datetime': {'$regex': keyword}})

    # # 'and' search
    # for record in mongo.db.Competition.find({'$and': search_list}):
    #     record['_id'] = str(record['_id'])
    #     data.append(record)

    # 'or' search (using unique _id to make sure no duplication)
    for record in mongo.db.Water_Collection.find({'$or': search_list}):
        record['_id'] = str(record['_id'])
        data.append(record)

    # Dedup no more
    # data_dedup = list(set(data))
    # data_dedup.sort(key=data.index)
    # return jsonify(data_dedup)
    return jsonify(data)


# bad requests holder
def bad_request(message):
    return error_response(400, message)


# error response
def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response
