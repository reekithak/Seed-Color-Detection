from flask import Flask ,render_template , request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_cors import CORS, cross_origin
from model import predict
from tensorflow.keras.preprocessing.image import load_img


app = Flask(__name__)
cors = CORS(app,resources={r"/upload/*": {"origins":"*"}})

app.config['CORS_HEADERS'] = 'Content-Type'
photos = UploadSet('photos',IMAGES)


app.config['UPLOADED_PHOTOS_DEST'] = './static/img'
configure_uploads(app,photos)

@app.route('/home',methods=['GET','POST'])
def home():
    welcome = "Hey People!"
    return welcome


@app.route('/upload',methods=['GET','POST'])
@cross_origin()
def upload():
    if request.method == 'POST' and  'photo' in request.files:
        filename = photos.save(request.files['photo'])
        print(list(request.files.lists()))
        
            
        image = load_img('./static/img/'+filename,target_size=(224,224))

        prediction = predict(image)
        answer = "Colored Seed:{},Good Seed:{}".format(prediction[0][0],
        prediction[0][1]
       )

        return answer

    return render_template('upload.html')


if __name__ == "__main__":
    app.run(port=5000,debug=True)