import base64

from flask import Flask, request
from flask_cors import CORS
from synthesizer import Synthesizer

app = Flask(__name__)
cors = CORS(app, resources={
    r"/api/v1/synthesize/*": {"origin": "*"},
})
finalSynthesizer = Synthesizer()
oldSynthesizer = Synthesizer()

# 파일 업로드 처리
@app.route('/api/v1/synthesize', methods=['POST', 'OPTIONS'])
def synthesize():
    if request.method == 'POST':
        text = str(request.json['text'])
        text = text + text[-1:]
        speakerType = str(request.json['type'])
        source = str(request.json['source'])
        speakerID = '0'
        if speakerType == 'donam':
            speakerID = '1'
        if speakerType == 'miji':
            speakerID = '2'
        if speakerType == 'junhyung':
            speakerID = '3'

        if source == 'final':
            audio = finalSynthesizer.synthesize(
                texts=[text],
                base_path=None,
                speaker_ids=[speakerID],
                attention_trim=False,
                base_alignment_path=None,
                isKorean=True
            )[0]
        else:
            audio = oldSynthesizer.synthesize(
                texts=[text],
                base_path=None,
                speaker_ids=[speakerID],
                attention_trim=False,
                base_alignment_path=None,
                isKorean=True
            )[0]

        return {'data': base64.b64encode(audio).decode('ascii')}

    if request.method == 'OPTIONS':
        return 'success'


if __name__ == '__main__':
    numSpeakers = 4
    finalSynthesizer.load('logdir-tacotron2/final', numSpeakers, None, inference_prenet_dropout=False)
    oldSynthesizer.load('logdir-tacotron2/oldest', numSpeakers, None, inference_prenet_dropout=False)
    app.run(host='0.0.0.0', port=21377, debug=True)
