from app import app, mongo
from flask import jsonify
from flask import request, url_for, redirect
from werkzeug.http import HTTP_STATUS_CODES
from bson.objectid import ObjectId
from func_pack import create_rec_hash, get_api_info
from config import Config
import requests


# Get all gas document infos
@app.route("/api/gas/document/all-documents", methods=['GET'])
def get_all_gas_documents():
    data = list()
    # the name of collection is called 'Collection'
    for record in mongo.db.Gas_Collection.find():
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get gas one document info by its _id
@app.route("/api/gas/document/rid/<string:rid>", methods=['GET'])
def get_gas_document_by__id(rid):
    data = list()
    # Type 'ObjectId' in Pymongo come from bson.objectid.ObjectId
    oid = ObjectId(rid)
    # the _id is unique
    record = mongo.db.Gas_Collection.find_one_or_404({"_id": oid})
    record['_id'] = str(record['_id'])
    data.append(record)
    return jsonify(data)


# Insert new document infos
@app.route("/api/gas/document", methods=['POST'])
def insert_gas_new_document():
    # assemble a dict
    new_document = dict()
    new_document['document_hash'] = create_rec_hash()
    new_document['boiler_room'] = request.form.get('boiler_room')
    new_document['boiler_no'] = request.form.get('boiler_no')
    new_document['date'] = request.form.get('date')
    new_document['time'] = request.form.get('time')
    new_document['datetime'] = request.form.get('datetime')
    new_document['gas_indicator'] = request.form.get('gas_indicator')
    new_document['gas_consumption'] = request.form.get('gas_consumption')
    new_document['employee_no'] = request.form.get('employee_no')

    oid = mongo.db.Gas_Collection.insert_one(new_document).inserted_id
    rid = str(oid)

    # return redirect(url_for('get_competition_by__id', rid=rid))
    # return the success info
    return get_gas_document_by__id(rid=rid)


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
@app.route("/api/gas/document/<string:rid>", methods=['PUT'])
def update_gas_document(rid):
    # assemble a dict
    mod_document = dict()
    mod_document['document_hash'] = request.form.get('document_hash')
    mod_document['boiler_room'] = request.form.get('boiler_room')
    mod_document['boiler_no'] = request.form.get('boiler_no')
    mod_document['date'] = request.form.get('date')
    mod_document['time'] = request.form.get('time')
    mod_document['datetime'] = request.form.get('datetime')
    mod_document['gas_indicator'] = request.form.get('gas_indicator')
    mod_document['gas_consumption'] = request.form.get('gas_consumption')
    mod_document['employee_no'] = request.form.get('employee_no')

    # pymongo update dict structure
    set_dict = {"$set": mod_document}

    oid = ObjectId(rid)
    mongo.db.Gas_Collection.update_one({"_id": oid}, set_dict)

    # return the success info
    return get_gas_document_by__id(rid=rid)


# Delete an existed gas document info
@app.route("/api/gas/document/<string:rid>", methods=['DELETE'])
def delete_gas_document(rid):
    set_dict = dict()
    oid = ObjectId(rid)
    set_dict['_id'] = oid
    mongo.db.Gas_Collection.delete_one(set_dict)
    data = [{'_id': rid, 'deleted status': 'success'}]
    return jsonify(data)


# Get document by its boiler_room, boiler_no and date
# Mention! There is no 'fuzzy mode' in this function
@app.route("/api/gas/document/boiler-room-and-no-and-datetime"
           "/<string:boiler_room>/<string:boiler_no>/<string:date>", methods=['GET'])
def get_gas_document_by_boiler_room_and_no_and_date(boiler_room, boiler_no, date):
    data = list()
    data_search = list()
    # maybe the data_feature in different items are same
    for record in mongo.db.Gas_Collection.find({"date": {'$regex': date}}):
        record['_id'] = str(record['_id'])
        data_search.append(record)
    # search the boiler_room, boiler_no field in the 'data_search' list
    for document in data_search:
        if boiler_room == document['boiler_room'] and boiler_no == document['boiler_no']:
            data.append(document)
    return jsonify(data)


# Get document by its date
@app.route("/api/gas/document/date/<string:date>", methods=['GET'])
def get_gas_document_by_date(date):
    data = list()
    # maybe the data_feature in different items are same
    for record in mongo.db.Gas_Collection.find({"date": date}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get document info by its boiler_room in fuzzy mode
@app.route("/api/gas/document/boiler-room/fuzzy/<string:boiler_room>", methods=['GET'])
def get_gas_document_by_boiler_room_fuzzy(boiler_room):
    data = list()
    # using fuzzy mode with regex
    for record in mongo.db.Gas_Collection.find({"boiler_room": {'$regex': boiler_room}}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get document info by its boiler_no in fuzzy mode
@app.route("/api/gas/document/boiler-no/fuzzy/<string:boiler_no>", methods=['GET'])
def get_gas_document_by_boiler_no_fuzzy(boiler_no):
    data = list()
    # using fuzzy mode with regex
    for record in mongo.db.Gas_Collection.find({"boiler_no": {'$regex': boiler_no}}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get document info by its boiler_no and boiler_room in fuzzy mode
@app.route("/api/gas/document/boiler-room-and-no/fuzzy/<string:boiler_room>/<string:boiler_no>", methods=['GET'])
def get_gas_document_by_boiler_room_and_no_fuzzy(boiler_room, boiler_no):
    data = list()
    search_list = list()
    search_list.append({'boiler_room': {'$regex': boiler_room}})
    search_list.append({'boiler_no': {'$regex': boiler_no}})
    # using fuzzy mode with regex
    # 'and' search
    for record in mongo.db.Gas_Collection.find({'$and': search_list}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get gas document by its employee_no in fuzzy mode
@app.route("/api/gas/document/employee-no/fuzzy/<string:employee_no>", methods=['GET'])
def get_gas_document_by_employee_no_fuzzy(employee_no):
    data = list()
    # maybe the hostname in different items are same
    for record in mongo.db.Gas_Collection.find({"employee_no": {'$regex': employee_no}}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get gas document by its boiler_room in fuzzy mode
@app.route("/api/gas/document/location/fuzzy/<string:boiler_room>", methods=['GET'])
def get_gas_document_by_location_fuzzy(boiler_room):
    data = list()
    # maybe the location in different items are same
    for record in mongo.db.Gas_Collection.find({"boiler_room": {'$regex': boiler_room}}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get document by its datetime in fuzzy mode
@app.route("/api/gas/document/datetime/fuzzy/<string:datetime>", methods=['GET'])
def get_gas_document_by_datetime_fuzzy(datetime):
    data = list()
    # maybe the data_feature in different items are same
    for record in mongo.db.Gas_Collection.find({"datetime": {'$regex': datetime}}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get document by its date in fuzzy mode
@app.route("/api/gas/document/date/fuzzy/<string:date>", methods=['GET'])
def get_gas_document_by_date_fuzzy(date):
    data = list()
    # maybe the data_feature in different items are same
    for record in mongo.db.Gas_Collection.find({"date": {'$regex': date}}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Fuzzy Search by boiler_no, employee_no, boiler_room or datetime
@app.route("/api/gas/document/doc-search/fuzzy/<string:keyword>", methods=['GET'])
def search_gas_document_fuzzy_single_keyword(keyword):
    data = list()
    search_list = list()
    search_list.append({'boiler_no': {'$regex': keyword}})
    search_list.append({'employee_no': {'$regex': keyword}})
    search_list.append({'boiler_room': {'$regex': keyword}})
    search_list.append({'datetime': {'$regex': keyword}})

    # # 'and' search
    # for record in mongo.db.Competition.find({'$and': search_list}):
    #     record['_id'] = str(record['_id'])
    #     data.append(record)

    # 'or' search (using unique _id to make sure no duplication)
    for record in mongo.db.Gas_Collection.find({'$or': search_list}):
        record['_id'] = str(record['_id'])
        data.append(record)

    # Dedup no more
    # data_dedup = list(set(data))
    # data_dedup.sort(key=data.index)
    # return jsonify(data_dedup)
    return jsonify(data)


# Gas Calculating Functions
@app.route("/api/gas/calculating/gas-consumption/<string:first_date>/<string:last_date>"
           "/<string:boiler_room>/<string:boiler_no>", methods=['GET'])
def calculate_gas_consumption_by_given_date(first_date, last_date, boiler_room, boiler_no):
    data = list()
    result_dict = {}
    # assemble url
    search_first_url = 'http://' + Config.LOCALHOST_IP_PORT + \
                       url_for('get_gas_document_by_boiler_room_and_no_and_date', boiler_room=boiler_room,
                               boiler_no=boiler_no, date=first_date)
    search_last_url = 'http://' + Config.LOCALHOST_IP_PORT + \
                      url_for('get_gas_document_by_boiler_room_and_no_and_date', boiler_room=boiler_room,
                              boiler_no=boiler_no, date=last_date)
    first_date_doc_list = get_api_info(requests.get(search_first_url))
    last_date_doc_list = get_api_info(requests.get(search_last_url))
    # if all things are correct
    if len(first_date_doc_list) >= 1 and len(last_date_doc_list) >= 1:
        first_doc = first_date_doc_list[0]
        last_doc = last_date_doc_list[0]
        gas_consumption = round(float(first_doc['gas_indicator']) - float(last_doc['gas_indicator']), 3)
        if gas_consumption < 0:
            gas_consumption_type = 'decrease'
        elif gas_consumption == 0:
            gas_consumption_type = 'invariant'
        else:
            gas_consumption_type = 'increase'
        result_dict['gas_consumption'] = abs(gas_consumption)
        result_dict['gas_consumption_type'] = gas_consumption_type
        result_dict['first_document'] = first_doc
        result_dict['last_document'] = last_doc
    # else Cannot find all relative document
    elif len(first_date_doc_list) < 1 and len(last_date_doc_list) < 1:
        result_dict['gas_consumption'] = 0
        result_dict['gas_consumption_type'] = 'error'
        result_dict['first_document'] = None
        result_dict['last_document'] = None
    # else Cannot find first relative document
    elif len(first_date_doc_list) < 1:
        last_doc = last_date_doc_list[0]
        result_dict['gas_consumption'] = 0
        result_dict['gas_consumption_type'] = 'error'
        result_dict['first_document'] = None
        result_dict['last_document'] = last_doc
    # else Cannot find last relative document
    elif len(last_date_doc_list) < 1:
        first_doc = first_date_doc_list[0]
        result_dict['gas_consumption'] = 0
        result_dict['gas_consumption_type'] = 'error'
        result_dict['first_document'] = first_doc
        result_dict['last_document'] = None
    # return result
    data.append(result_dict)
    return jsonify(data)


# Gas Calculating by given boiler_room and boiler_no successively
@app.route("/api/gas/calculating/gas-consumption/successive/<string:boiler_room>/<string:boiler_no>", methods=['GET'])
def calculate_gas_consumption_successive_by_boiler_room_and_no(boiler_room, boiler_no):
    data = list()
    # assemble url
    search_url = 'http://' + Config.LOCALHOST_IP_PORT + \
                 url_for('get_gas_document_by_boiler_room_and_no_fuzzy', boiler_room=boiler_room,
                         boiler_no=boiler_no)
    search_list = get_api_info(requests.get(search_url))
    # if there are at least 2 docs, that's mean it can be calculated
    if len(search_list) >= 2:
        # sorted by date
        search_list = sorted(search_list, key=lambda doc: doc['date'])
        flag = 0
        while flag < len(search_list):
            result_dict = {}
            gas_consumption = round(float(search_list[flag]['gas_indicator'])
                                    - float(search_list[flag-1]['gas_indicator']), 3)
            if gas_consumption < 0:
                gas_consumption_type = 'decrease'
            elif gas_consumption == 0:
                gas_consumption_type = 'invariant'
            else:
                gas_consumption_type = 'increase'
            result_dict['gas_consumption'] = abs(gas_consumption)
            result_dict['gas_consumption_type'] = gas_consumption_type
            result_dict['first_document'] = search_list[flag]
            result_dict['last_document'] = search_list[flag-1]
            data.append(result_dict)
            # flag add 1
            flag += 1
    elif len(search_list) == 1:
        error_dict = {}
        error_dict['gas_consumption'] = 0
        error_dict['gas_consumption_type'] = 'error'
        error_dict['first_document'] = search_list[0]
        error_dict['last_document'] = None
        data.append(error_dict)
    else:
        error_dict = {}
        error_dict['gas_consumption'] = 0
        error_dict['gas_consumption_type'] = 'error'
        error_dict['first_document'] = None
        error_dict['last_document'] = None
        data.append(error_dict)
    # return result
    return jsonify(data)


# Gas Calculating by given boiler_room and boiler_no successively
@app.route("/api/gas/calculating/gas-consumption/successive/<string:boiler_room>/<string:boiler_no>"
           "/<<string:first_date>/<string:last_date>>", methods=['GET'])
def calculate_gas_consumption_successive_by_boiler_room_and_no_and_date(boiler_room, boiler_no, first_date, last_date):
    data = list()
    # assemble url
    search_url = 'http://' + Config.LOCALHOST_IP_PORT + \
                 url_for('calculate_gas_consumption_successive_by_boiler_room_and_no', boiler_room=boiler_room,
                         boiler_no=boiler_no)
    # search list has been sorted!!
    search_list = get_api_info(requests.get(search_url))
    for doc_dict in search_list:
        if doc_dict.first_document.date > first_date and doc_dict.last_document.date < last_date:
            data.append(doc_dict)
    # return search result
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
