# webcam_stream.py
from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Initialize the webcam
camera = cv2.VideoCapture(1)  # 0 for the first connected camera (usually the USB webcam)

def generate_frames():
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Use yield to send the frame as a byte stream
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    # Return the HTML template
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # Return the camera frames as a multipart response
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
