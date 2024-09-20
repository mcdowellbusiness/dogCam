from flask import Flask, render_template, Response
import cv2
import os  # To read the PORT environment variable

app = Flask(__name__)

# Initialize the webcam (1 for the first connected USB camera, adjust if necessary)
camera = cv2.VideoCapture(1)

if not camera.isOpened():
    raise RuntimeError("Could not open USB webcam. Make sure it's connected and recognized.")

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

# Release the camera when the app stops
@app.teardown_appcontext
def cleanup(resp_or_exc):
    camera.release()

if __name__ == '__main__':
    # Use the PORT environment variable if available, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
