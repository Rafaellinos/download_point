from os import listdir, stat
from os.path import isfile, join
from datetime import datetime

from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

PATH_DOCUMENTS = './documents' # TODO GIVE THE FULL PATH
DATE_PATTERN = '%d/%m/%Y - %H:%M:%S'


def bytes_to_human(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def seconds_to_datetime(seconds):
    return datetime.fromtimestamp(seconds).strftime(DATE_PATTERN)


@app.route('/', methods=['GET'])
def main_page():
    files = [f for f in listdir(PATH_DOCUMENTS) if isfile(join(PATH_DOCUMENTS, f))]
    formatted_files = []
    for file in files:
        desc = stat(PATH_DOCUMENTS + '/' + file)
        file_description = {
            'name': file,
            # 'create_date': desc.st_birthtime,
            'last_modification': seconds_to_datetime(desc.st_mtime),
            'type': file.split('.')[-1] if '.' in file else "",
            'size': bytes_to_human(desc.st_size)
        }
        formatted_files.append(file_description)

    return jsonify(formatted_files)


@app.route('/download', methods=['GET'])
def download(**kw):
    file = PATH_DOCUMENTS + '/' + request.args.get('filename')
    if isfile(file):
        return send_file(file, as_attachment=True)
    return jsonify({'message': 'File not found :('}), 404

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000)
