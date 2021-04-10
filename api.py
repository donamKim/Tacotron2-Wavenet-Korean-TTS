# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
# from werkzeug import secure_filename
from flask_cors import CORS
from datetime import datetime
import subprocess
import json
import operator
import threading

app = Flask(__name__)
cors = CORS(app, resources={
    r"/api/v1/synthesize/*": {"origin": "*"},
})


# 파일 업로드 처리
@app.route('/api/v1/synthesize', methods=['POST', 'OPTIONS'])
def synthesize():
    if request.method == 'POST':
        text = str(request.json['text'])
        text = text + text[-1:]
        print('@@@@@@@@@@@@@ ' + text)
        res = subprocess.check_output([
            'python3', 'synthesizer.py',
            '--load_path', 'logdir-tacotron2/son_2021-02-23_02-08-50',
            '--num_speakers', '4',
            '--speaker_id', '1',
            '--text', text
        ])
        a = res.decode('utf-8').split('@@@@RESULT@@@@: ')
        b = a[1].split('\'')

        return {'data': b[1]}

    if request.method == 'OPTIONS':
        return 'success'


if __name__ == '__main__':
    # 서버 실행
    app.run(host='0.0.0.0', port=21377, debug=True)
