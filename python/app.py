from flask import Flask, render_template, Response
from recognizer import FaceRecognizer
from gesture.identify_gesuter import GestureRecognizer

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')
 
 
def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')
               
 
 
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(FaceRecognizer()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/gesture_feed')
def gesture_feed():
    return Response(gen(GestureRecognizer()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
 
if __name__ == '__main__':
    app.run(debug=True, threaded=True)