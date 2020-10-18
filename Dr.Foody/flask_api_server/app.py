from flask import Flask, render_template, url_for, request
from flask_restful import reqparse, Api, Resource
import pandas as pd 
import joblib

app = Flask(__name__)
api = Api(app)

def gender_features(word):
    return {'last_letter': word[-1]}
gender_features("나경")

# pickled binary file 형태로 저장된 객체를 로딩한다 
file_name = 'data.pickle' 
obj = joblib.load(file_name) 

class FlaskApi(Resource):        
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str)
            args = parser.parse_args()

            data = args['name']
            #vect = cv.transform(data).toarray()
            my_prediction = obj.classify(gender_features(data))
            print(my_prediction)

            return {'Gender': my_prediction}
        except Exception as e:
            return {'error': str(e)}


api.add_resource(FlaskApi, '/predict')

def on_json_loading_failed_return(e):
    return {}


# @app.route('/')
# def home():
#     return 
# #    return render_template('home.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     request.on_json_loading_failed = on_json_loading_failed_return
#     print(request.get_json())
#     if request.method == 'POST':
#         message = request.form['message']
#         #왜 이렇게 쓴 걸까?
#         data = message
#         #vect = cv.transform(data).toarray()
#         my_prediction = obj.classify(gender_features(data))
#         print(my_prediction)
#     return 
# #    return render_template('result.html', prediction = my_prediction)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)