from flask import Flask, send_file, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Run your script to generate the XML file
        result = subprocess.run(['python3', 'generate-rekt-rss.py'], capture_output=True, text=True)
        
        # Check if the file was created
        if os.path.exists('public/rekt_news_rss.xml'):
            return jsonify({
                "message": "Script executed successfully",
                "output": result.stdout
            }), 200
        else:
            return jsonify({
                "message": "Script executed, but XML file not found.",
                "output": result.stdout
            }), 500
    except Exception as e:
        return jsonify({
            "message": "Script execution failed",
            "error": str(e)
        }), 500

@app.route('/rss-feed', methods=['GET'])
def get_rss_feed():
    try:
        # Serve the XML file
        return send_file('public/rekt_news_rss.xml', mimetype='application/rss+xml')
    except Exception as e:
        return jsonify({
            "message": "Could not retrieve XML file",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
