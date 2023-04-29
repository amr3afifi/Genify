from flask import Flask,request
import sys
import json
import pandas as pd
import numpy as np
import pickle
import sys
import xgboost as xgb
from generate_model import *


app = Flask(__name__)

global df
df= pd.read_csv("./datasets/model_results.csv")
#load the model from disk
model = pickle.load(open('model.pkl', 'rb'))

product_names = {"ind_ahor_fin_ult1" : "Saving Account","ind_aval_fin_ult1" : "Guarantees","ind_cco_fin_ult1" : "Current Accounts","ind_cder_fin_ult1" : "Derivada Account",
"ind_cno_fin_ult1" : "Payroll Account","ind_ctju_fin_ult1" : "Junior Account","ind_ctma_fin_ult1" : "Más particular Account","ind_ctop_fin_ult1" : "particular Account",
"ind_ctpp_fin_ult1" : "particular Plus Account","ind_deco_fin_ult1" : "Short-term deposits","ind_deme_fin_ult1" : "Medium-term deposits","ind_dela_fin_ult1" : "Long-term deposits",
"ind_ecue_fin_ult1" : "e-account","ind_fond_fin_ult1" : "Funds","ind_hip_fin_ult1" : "Mortgage","ind_plan_fin_ult1" : "Pensions","ind_pres_fin_ult1" : "Loans",
"ind_reca_fin_ult1" : "Taxes","ind_tjcr_fin_ult1" : "Credit Card","ind_valo_fin_ult1" : "Securities","ind_viv_fin_ult1" : "Home Account","ind_nomina_ult1" : "Payroll",
"ind_nom_pens_ult1" : "Pensions","ind_recibo_ult1" : "Direct Debit"}

cols={"gender":"sexo","segment":"segmento",
"relationship_type":"tiprel_1mes","activity_level": "ind_actividad_cliente",
"income":"renta","seniority":"antiguedad","age":"age"
}

activity_level = {"ACTIVE" : '1',"INACTIVE" :'0'}
segment = {"INDIVIDUAL" : '02 - PARTICULARES',"STUDENT" :'03 - UNIVERSITARIO',"VIP":'01 - TOP'}
gender = {"MALE" : 'H',"FEMALE" :'V'}
relationship = {"ACTIVE" : 'A',"INACTIVE" :'I',"POTENTIAL":'P',"FORMER CUSTOMER":'R',"FORMER CO-OWNER":'N'}



def map_values(col_names, map_products=product_names):
    '''
    Change column names (e.g."ind_recibo_ult1") to map names (e.g."Direct Debit").
    '''
    return list(map(lambda col_name: map_products[col_name], col_names))

def predictions(new_user):
    x_vars_list, y_vars_list, cust_dict = processData([new_user], {},False)
    test_X = np.array(x_vars_list)
    xgtest = xgb.DMatrix(test_X)
    predictions = model.predict(xgtest)
    predictions = np.argsort(predictions,axis=1)
    predictions = np.fliplr(predictions)[:,:7]
    final_preds = ["".join(list(target_cols[pred])) for pred in predictions[0]]

    return map_values(final_preds)

def check_choices(user,new_user,message,input,choices):
    if user.get(input):
        check= choices.get(user[input])
        if check:
            new_user[cols[input]] = check
        else:
            message+='Please enter a valid activity level from options: '+str(list(choices.keys()))+', '   
    else:
        message+="Input: '"+input+"' is missing, "
        
    return message
    
def check_number(user,new_user,message,input,min_val,max_val):
    num=user.get(input)
    if num:
        if num<min_val or num>max_val:
            message+='Please enter a valid '+input+', '
        else:
            new_user[cols[input]] = str(num)   
    else:
        message+="Input: '"+input+"' is missing, "
        
    return message




###################### ROUTES ######################

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h2>'

@app.route('/classification-error',methods=['POST'])
def classification_error():
    body=request.data.decode('utf8').replace("\'", "\"")
    json_body = json.loads(body)

    print('eeeeeeeeeeeeeeeeeeeeeeeee',json_body, file=sys.stderr)
    return json_body

@app.route('/recommend/<int:user_id>',methods=['GET'])
def recommend_for_user(user_id):
    print(request.data)
    result=df[df['ncodpers']==user_id]
    if not result.empty:
        product_codes=result['added_products'][0].split(" ")
        products=map_values(product_codes)
        return {"is_found":True, "products":products}

    return {"is_found":False,"message":"User ID not found,Please enter user details to be able to predict"}

@app.route('/predict',methods=['POST'])
def predict_new_user():
    body=request.data.decode('utf8').replace("\'", "\"")
    user = json.loads(body)
    
    new_user={
        "ncodpers": "15889",
        "fecha_dato": "2016-06-28",
        "fecha_alta":"1995-15-01",
        "indrel":"1",
        "indrel_1mes":"1",
        "tipodom":"1",
        "ind_nuevo":"0",
        "indrel":"1",
        "indresi":"S",
        "indext":"N",
        "conyuemp":"N",
        "indfall":"N",
        "ind_empleado": "F",
        'pais_residencia':None  ,
        "sexo":None ,
        'age': None,
        "ind_actividad_cliente":None,
        'renta':None,
        "segmento":None,
        "antiguedad":None,
        "tiprel_1mes":None ,
        "ult_fec_cli_1t":"",
        "cod_prov":"28",
        "nomprov":"MADRID",
        "canal_entrada":"KAT"
    }
    
    message=''
    response=None
    try:

        message=check_number(user,new_user,message,'age',min_val=0,max_val=110)
        message=check_number(user,new_user,message,'seniority',min_val=0,max_val=1000)
        message=check_number(user,new_user,message,'income',min_val=0,max_val=1000000)

        message=check_choices(user,new_user,message,'gender',gender)
        message=check_choices(user,new_user,message,'relationship_type',relationship)
        message=check_choices(user,new_user,message,'segment',segment)
        message=check_choices(user,new_user,message,'activity_level',activity_level)
        
        if user.get('nationality'):
            new_user['pais_residencia']  = user.get('nationality')[0:2]
        else:
            message+="Input: 'nationality' is missing, "        
        
            
    except Exception as e:  
        message+=str(e)
    
    print('FINAL NEW USER',new_user, file=sys.stderr)
    if len(message)==0:
        response=predictions(new_user)  
         
    return {"message":message,"products":response}

@app.route('/products',methods=['GET'])
def getProducts():
    return {"products":list(product_names.values())}



if __name__ == "__main__":
    app.run(debug=True)