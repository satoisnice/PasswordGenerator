from flask import Flask, render_template, send_file
import io
import os
import zipfile

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/download')
def download():
    zip_path = '../pwtool.zip'
    return send_file(
        zip_path,
        as_attachment=True,
        download_name='PWtool.zip',
        mimetype='application/zip'
    )

if __name__ == "__main__":
    app.run(debug=True, port=3000)