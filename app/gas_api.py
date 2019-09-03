from app import app, mongo
from flask import jsonify
from flask import request, url_for, redirect
from werkzeug.http import HTTP_STATUS_CODES
from bson.objectid import ObjectId
from func_pack import create_rec_hash


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


# Get document info by its name in fuzzy mode
@app.route("/api/gas/document/boiler-no/fuzzy/<string:boiler_no>", methods=['GET'])
def get_gas_document_by_boiler_no_fuzzy(boiler_no):
    data = list()
    # using fuzzy mode with regex
    for record in mongo.db.Gas_Collection.find({"boiler_no": {'$regex': boiler_no}}):
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
