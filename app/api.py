from app import app, mongo
from flask import jsonify
from flask import request, url_for, redirect
from werkzeug.http import HTTP_STATUS_CODES
from bson.objectid import ObjectId
from func_pack import create_rec_hash


# Get all document infos
@app.route("/api/document/all-documents", methods=['GET'])
def get_all_documents():
    data = list()
    # the name of collection is called 'Collection'
    for record in mongo.db.Collection.find():
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get one document info by its _id
@app.route("/api/document/rid/<string:rid>", methods=['GET'])
def get_document_by__id(rid):
    data = list()
    # Type 'ObjectId' in Pymongo come from bson.objectid.ObjectId
    oid = ObjectId(rid)
    # the _id is unique
    record = mongo.db.Collection.find_one_or_404({"_id": oid})
    record['_id'] = str(record['_id'])
    data.append(record)
    return jsonify(data)


# Insert new document infos
@app.route("/api/document", methods=['POST'])
def insert_new_document():
    # assemble a dict
    new_document = dict()
    new_document['document_hash'] = create_rec_hash()
    new_document['location'] = request.form.get('location')
    new_document['datetime'] = request.form.get('datetime')
    new_document['boiler_no'] = request.form.get('boiler_no')
    new_document['gas_consumption'] = request.form.get('gas_consumption')
    new_document['elec_consumption'] = request.form.get('elec_consumption')
    new_document['water_consumption'] = request.form.get('water_consumption')
    new_document['water_out_temperature'] = request.form.get('water_out_temperature')
    new_document['water_in_temperature'] = request.form.get('water_in_temperature')
    new_document['employee_no'] = request.form.get('employee_no')

    oid = mongo.db.Collection.insert_one(new_document).inserted_id
    rid = str(oid)

    # return redirect(url_for('get_competition_by__id', rid=rid))
    # return the success info
    return get_document_by__id(rid=rid)


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
@app.route("/api/document/<string:rid>", methods=['PUT'])
def update_document(rid):
    # assemble a dict
    mod_document = dict()
    mod_document['document_hash'] = create_rec_hash()
    mod_document['location'] = request.form.get('location')
    mod_document['datetime'] = request.form.get('datetime')
    mod_document['boiler_no'] = request.form.get('boiler_no')
    mod_document['gas_consumption'] = request.form.get('gas_consumption')
    mod_document['elec_consumption'] = request.form.get('elec_consumption')
    mod_document['water_consumption'] = request.form.get('water_consumption')
    mod_document['water_out_temperature'] = request.form.get('water_out_temperature')
    mod_document['water_in_temperature'] = request.form.get('water_in_temperature')
    mod_document['employee_no'] = request.form.get('employee_no')

    # pymongo update dict structure
    set_dict = {"$set": mod_document}

    oid = ObjectId(rid)
    mongo.db.Collection.update_one({"_id": oid}, set_dict)

    # return the success info
    return get_document_by__id(rid=rid)


# Delete an existed document info
@app.route("/api/document/<string:rid>", methods=['DELETE'])
def delete_document(rid):
    set_dict = dict()
    oid = ObjectId(rid)
    set_dict['_id'] = oid
    mongo.db.Collection.delete_one(set_dict)
    data = [{'_id': rid, 'deleted status': 'success'}]
    return jsonify(data)


# Get document info by its name in fuzzy mode
@app.route("/api/document/boiler-no/fuzzy/<string:boiler_no>", methods=['GET'])
def get_document_by_boiler_no_fuzzy(boiler_no):
    data = list()
    # using fuzzy mode with regex
    for record in mongo.db.Collection.find({"boiler_no": {'$regex': boiler_no}}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get document by its employee_no in fuzzy mode
@app.route("/api/document/employee-no/fuzzy/<string:employee_no>", methods=['GET'])
def get_document_by_employee_no_fuzzy(employee_no):
    data = list()
    # maybe the hostname in different items are same
    for record in mongo.db.Collection.find({"employee_no": {'$regex': employee_no}}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get document by its location in fuzzy mode
@app.route("/api/document/location/fuzzy/<string:location>", methods=['GET'])
def get_document_by_location_fuzzy(location):
    data = list()
    # maybe the location in different items are same
    for record in mongo.db.Collection.find({"location": {'$regex': location}}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get document by its datetime in fuzzy mode
@app.route("/api/document/datetime/fuzzy/<string:datetime>", methods=['GET'])
def get_document_by_datetime_fuzzy(datetime):
    data = list()
    # maybe the data_feature in different items are same
    for record in mongo.db.Collection.find({"datetime": {'$regex': datetime}}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Fuzzy Search by boiler_no, employee_no, location or datetime
@app.route("/api/document/doc-search/fuzzy/<string:keyword>", methods=['GET'])
def search_document_fuzzy_single_keyword(keyword):
    data = list()
    search_list = list()
    search_list.append({'boiler_no': {'$regex': keyword}})
    search_list.append({'employee_no': {'$regex': keyword}})
    search_list.append({'location': {'$regex': keyword}})
    search_list.append({'datetime': {'$regex': keyword}})

    # # 'and' search
    # for record in mongo.db.Competition.find({'$and': search_list}):
    #     record['_id'] = str(record['_id'])
    #     data.append(record)

    # 'or' search (using unique _id to make sure no duplication)
    for record in mongo.db.Collection.find({'$or': search_list}):
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
