from flask import Flask, render_template, Response, json
from recognizer import FaceRecognizer
import recognizer
import sqlite3
# from gesture.identify_gesuter import GestureRecognizer

app = Flask(__name__)
test = 'fefef'
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')
 
 
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

# @app.route('/gesture_feed')
# def gesture_feed():
#     return Response(gen(GestureRecognizer()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/first')
def gen_first():
    return render_template('first.html')

@app.route('/balance')
def get_balance():
    return render_template('balance.html')

@app.route('/withdrawal')
def get_withdrawal():
    return render_template('tq.html')

@app.route('/get_balance')
def get_db_balance():
    conn = sqlite3.connect('hl.db')
    try:
        if conn:
            print(recognizer.face_name)
            command = "SELECT * FROM Customer WHERE cust_name = 'Edwin'"
            #cursor = conn.execute(command, (recognizer.face_name,))
            cursor = conn.execute(command)
            profile = None
            
            for row in cursor:
                profile = row
            
            conn.close()
            response = app.response_class(
                response=json.dumps(profile[2]),
                status=200,
                mimetype='application/json'
            )

            return response
            
            
    except sqlite3.ProgrammingError as ex:
        print("Error: " + str(ex))
 
if __name__ == '__main__':
    app.run(debug=True, threaded=True)