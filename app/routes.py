from app import app
from flask import jsonify, render_template


@app.route('/')
@app.route('/tutorial')
def usage():
    usages = [
        {'api_format': '/api/gas/document/all-documents', 'method': 'GET',
         'description': 'Get gas all document infos'},
        {'api_format': '/api/gas/document/rid/<string:rid>', 'method': 'GET',
         'description': 'Get gas one document info by its _id'},
        {'api_format': '/api/gas/document', 'method': 'POST',
         'description': 'Insert new gas document infos'},
        {'api_format': '/api/gas/document/<string:rid>', 'method': 'PUT',
         'description': 'Modify an gas existed document info'},
        {'api_format': '/api/gas/document/<string:rid>', 'method': 'DELETE',
         'description': 'Delete an gas existed document info'},
        {'api_format': '/api/gas/document/boiler-room-and-no-and-datetime'
                       '/<string:boiler_room>/<string:boiler_no>/<string:date>', 'method': 'GET',
         'description': 'Integration Search by boiler_room, boiler_no, date'},
    ]

    return render_template('frontPage.html', usage_infos=usages)

