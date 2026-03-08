from flask import Flask, render_template, request, jsonify, send_file, abort
import os
from services import PasswordService
from models import PasswordEntry, PasswordRule
from datetime import datetime
import uuid
import traceback
import random
import string

app = Flask(__name__, template_folder='templates', static_folder='.', static_url_path='')
service = PasswordService(storage_file='passwords.json')

# Call API call PasswordEntry , PasswordRule , PasswordService 
# backend and frontend communicate
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/passwords', methods=['GET'])
def get_passwords():
    entries = service.get_all_passwords()
    data = []
    for idx, e in enumerate(entries):
        data.append({
            'index':   idx,
            'site':    e.get_site(),
            'username': e.get_username(),
            'password': e.get_password(),
            'expiry':  e.get_expiry_date().strftime('%Y-%m-%d'),
            'file':    os.path.basename(e.get_file_path()) if e.get_file_path() else None,
            'file_path': e.get_file_path(),
            'expired': service.is_expired(e),
            'strong':  e.get_password() and service.is_strong_password(e.get_password()),
            'repeated': e.get_password() and service.is_repeated_password(e.get_password(), exclude_index=idx),
        })
    return jsonify(data)

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    try:
        max_len = int(data.get('max_length', 16))
        if max_len < 8:
            max_len = 16

        rule = PasswordRule(
            max_length     = max_len,
            require_special = data.get('require_special', True),
            numbers_only    = data.get('numbers_only', False)
        )

        pw = service.generate_password(rule)

        if data.get('first_letter', False) and pw and not pw[0].isalpha():
            first = random.choice(string.ascii_letters)
            pw = first + pw[1:]

        return jsonify({'password': pw})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/password', methods=['POST'])
def add_password():
    data = request.form
    files = request.files
    try:
        site       = data.get('site', '').strip()
        username   = data.get('username', '').strip()
        password   = data.get('password', '').strip()
        expiry_str = data.get('expiry', '').strip()
        edit_index = data.get('index', '').strip()

        if not site or not username:
            return jsonify({'error': 'Site and username are required'}), 400

        try:
            expiry = datetime.strptime(expiry_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid expiry date format'}), 400

        file_path = None
        if 'file' in files:
            uploaded_file = files['file']
            if uploaded_file and uploaded_file.filename.strip():
                file_path = service.upload_file(uploaded_file)
                if not file_path:
                    return jsonify({'error': 'Failed to save uploaded file'}), 500

        entry = PasswordEntry(
            site        = site,
            username    = username,
            password    = password,
            expiry_date = expiry,
            file_path   = file_path
        )

        dummy_rule = PasswordRule(16, True, False)

        if edit_index and edit_index.isdigit():
            idx = int(edit_index)
            service.update_password(idx, entry, dummy_rule)
            message = 'Entry updated'
        else:
            service.add_password(entry, dummy_rule)
            message = 'Entry saved'

        return jsonify({'status': 'ok', 'message': message})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400

@app.route('/api/password/<int:index>', methods=['DELETE'])
def delete_password(index):
    try:
        service.delete_password(index)
        return jsonify({'status': 'ok'})
    except:
        return jsonify({'error': 'Delete failed'}), 400

@app.route('/files/<path:filename>')
def serve_file(filename):
    path = os.path.join('files', filename)
    if os.path.isfile(path):
        return send_file(path, as_attachment=True)
    abort(404)

if __name__ == '__main__':
    os.makedirs('files', exist_ok=True)
    app.run(debug=True, port=5001)