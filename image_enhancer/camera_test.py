from flask import Flask, render_template_string, Response, request, jsonify
import base64
import cv2

app = Flask(__name__)
cap = cv2.VideoCapture(0)

@app.route('/capture', methods=['POST'])
def capture_image():
    data = request.json['image']
    image_data = base64.b64decode(data.split(',')[1])  # 이미지 데이터 파싱 및 디코딩

    with open('captured_image.jpg', 'wb') as f:
        f.write(image_data)

    return jsonify({'status': 'success', 'message': 'Image captured successfully'})


def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/')
def index():
    # HTML 페이지에 비디오 스트림과 캡처 버튼을 포함시키는 템플릿
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Camera Capture</title>
    </head>
    <body>
        <h1>Camera Capture</h1>
        <img src="{{ url_for('video_feed') }}" id="video_feed">
        <button id="capture_btn">Capture Image</button>

        <script>
        document.getElementById('capture_btn').addEventListener('click', function() {
            var video = document.getElementById('video_feed');
            var canvas = document.createElement('canvas');
            canvas.width = video.width;
            canvas.height = video.height;
            var ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            var dataURL = canvas.toDataURL('image/jpeg');

            // 서버에 캡처된 이미지를 보내거나 저장하는 로직을 추가
            // dataURL 서버의 API로 POST 요청을 보내 처리 가능 
        });
        </script>
        <script src="{{ url_for('static', filename='js/capture.js') }}"></script>

    </body>
    </html>
    ''')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)

