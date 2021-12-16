import os
import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

#import testcv
# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set([ 'png', 'jpg', 'jpeg', 'JPG'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        
        
        # Move the file to the upload folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        folder='uploads'
        filename = file.filename
        green = np.uint8([[[0,255,0]]])
        hsv_color = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
        h_c = hsv_color[0][0][0]

        lowerColor = np.array([130,137,10])
        upperColor = np.array([220,235,130])
        print(hsv_color)

        image = cv2.imread(os.path.join(folder,file.filename))
        hsv_image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        mask_image = cv2.inRange(hsv_image, lowerColor,upperColor)
        final_image = cv2.bitwise_and(image,image,mask=mask_image)

        cv2.imwrite(os.path.join(folder,filename),hsv_image)
        #cv2.imwrite(os.path.join(folder,filename),mask_image)
        #cv2.imwrite(os.path.join(folder,filename),final_image)

        return redirect(url_for('uploaded_file',filename=filename))
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=int("5000"),
        debug=True
    )
