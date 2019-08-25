from app import app
from flask import jsonify, render_template


@app.route('/')
@app.route('/tutorial')
def usage():
    usages = [
        {'api_format': '/api/document/all-documents', 'method': 'GET',
         'description': 'Get all document infos'},
        {'api_format': '/api/document/rid/<string:rid>', 'method': 'GET',
         'description': 'Get one document info by its _id'},
        {'api_format': '/api/document', 'method': 'POST',
         'description': 'Insert new document infos'},
        {'api_format': '/api/document/<string:rid>', 'method': 'PUT',
         'description': 'Modify an existed document info'},
        {'api_format': '/api/document/<string:rid>', 'method': 'DELETE',
         'description': 'Delete an existed document info'},
        {'api_format': '/api/document/doc-search/fuzzy/<string:keyword>', 'method': 'GET',
         'description': 'Fuzzy Search by boiler_no, employee_no, location or datetime'},
    ]

    return render_template('frontPage.html', usage_infos=usages)

