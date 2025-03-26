from flask import Flask, jsonify
import subprocess
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/get_emails', methods=['POST'])
def get_emails():
    try:
        subprocess.run(['python', 'scripts/get_emails.py'], check=True)
        return jsonify({"status": "success", "message": "Email retrieved!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/identify_relations', methods=['POST'])
def identify_relations():
    try:
        subprocess.run(['python', 'scripts/identify_relations.py'], check=True)
        return jsonify({"status": "success", "message": "Relations identified!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/create_relations', methods=['POST'])
def create_relations():
    try:
        subprocess.run(['python', 'scripts/create_relations.py'], check=True)
        return jsonify({"status": "success", "message": "Relations modelization finished!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)