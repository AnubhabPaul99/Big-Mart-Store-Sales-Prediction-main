from flask import Flask, render_template, request
import jsonify
import requests
import pickle

app = Flask(__name__, template_folder='templates')
model = pickle.load(open('catboost_model.pkl', 'rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        item_type = float(request.form['item_type'])
        
        item_fat_content = float(request.form['item_fat_content'])
            
        item_weight = float(request.form['item_weight'])
        
        item_visibilty = (float(request.form['item_visibilty'])/100)**(1/5)
        
        item_mrp = float(request.form['item_mrp'])
        
        outlet_size = float(request.form['outlet_size'])
            
        outlet_type = float(request.form['outlet_type'])
            
        outlet_location_type = float(request.form['outlet_location_type'])
        
        outlet_age = 2020 - int(request.form['outlet_est_year'])
        
        prediction = (model.predict([[item_weight, item_fat_content, item_visibilty, item_type, item_mrp, outlet_size, outlet_location_type, outlet_type, outlet_age]]))**4
    
        output = round(prediction[0],2)
           
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this item!")
        else:
            return render_template('index.html',prediction_text="Item-Outlet Sales will be around: ₹{} per day".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)