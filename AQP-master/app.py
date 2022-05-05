import base64
from turtle import hideturtle
from flask import Flask, render_template, request, g, request, redirect, url_for, session
from ml_test import *
import pickle
import pandas as pd
import psycopg2

app = Flask(__name__)

links=()
ch=""
# global links
links = ["home","about","team","work","query","contact"]


@app.route("/")
def hello_world():
    global links
   # links = ["home","about","team","work","query","contact"]
    return render_template("index.html", anchor=links)

@app.route("/queries")
def queries():
   # l=["query"]
    return render_template("index.html", anchor=links, c=len(links) )


"""
@app.route("/choose",methods=['POST','GET'])
def choose():
    global ch
    ch=request.form["Choose"]
    print("ch value ",ch)
    #return render_template()

"""
@app.route("/choose",methods=['POST','GET'])
def choose():
    global ch
    ch=request.form["Choose"]
    print("var",ch)
    return render_template("index.html",anchor=links)
    

#Query1
@app.route("/query1",methods=['POST','GET'])
def query1():
    print("database choosen is:",ch)
    from ast import literal_eval
    import ast
    
    #db_name="Cervical_Cancer"
    #db_name="Fetal_health_Classification"
    if ch=="fetal":
        db_name="Fetal_health_Classification"
    elif ch=="cervical":
        db_name="Cervical_Cancer"


    conn = psycopg2.connect(database=db_name,
                        user='postgres', password='parpsql', 
                        host='localhost', port='5432')
    

  
    conn.autocommit = True
    cur = conn.cursor()
    
    cur.execute('select * from Table1;')
    df = pd.read_sql_query("SELECT * from Table1", conn)
    cur.execute('select * from Table2')
    coeff_dataset = pd.read_sql_query("SELECT * from Table2", conn)
    conn.commit()
    

    # print(coeff_dataset['features'])
    cf_features = coeff_dataset['features']  #model data features
    global val
    cf_coffs=coeff_dataset['coefficient'] #model data coefficients
    cf_target=coeff_dataset['target']
    dfeatures=request.form['features']
    dfeatures=list(dfeatures.split(','))  #user input
    val=request.form['values'] #values of the inputed features
    x=df.loc[:, dfeatures] 
    t=request.form['target']
    t=list(t.split(" "))
    y= df.loc[:, t]
    lngth=len(cf_features)
    pos=0
    cnt=0
    pos=0
    count=0

    for i in range(0,lngth):
        if (set(eval(cf_features[i])) == set(dfeatures)) and (set(eval(cf_target[i])) == set(t)):
            print("DontGenerate model")
            out1 = existingModel(i,dfeatures,val,cf_coffs)
            pos=i
            break
        else:
            cnt+=1
            
    if(cnt==lngth): 
        print("Generate model")
        out1=generateModel(dfeatures,t,val,x,y,cur,conn)
        
    
    return render_template("query1.html",features=dfeatures,values=val,target=t,fet=out1)



@app.route("/query2",methods=['POST','GET'])
def query2():
    from ast import literal_eval
    import ast
    #db_name="Cervical_Cancer"
    #db_name="Fetal_health_Classification"
    if ch=="fetal":
        db_name="Fetal_health_Classification"
    elif ch=="cervical":
        db_name="Cervical_Cancer"

    conn = psycopg2.connect(database=db_name,
                        user='postgres', password='parpsql', 
                        host='localhost', port='5432')
    
    if db_name=="Cervical_Cancer":
        flag=1
    else:
        flag=0

    conn.autocommit = True
    cur = conn.cursor()
    cur.execute('select * from Table1;')
    df = pd.read_sql_query("SELECT * from Table1", conn)
    cur.execute('select * from Table2')
    coeff_dataset = pd.read_sql_query("SELECT * from Table2", conn)
    conn.commit()
    # print(coeff_dataset['features'])

    cf_features = coeff_dataset['features']  
    # print(cf_features)
    #cf_features
    global val
    cf_coffs=coeff_dataset['coefficient']
    dfeatures=request.form['features']
    #val=request.form['values']
    target=request.form['target']
    dfeatures=list(dfeatures.split(','))
    target=list(target.split(" "))
    l=len(dfeatures)
    x=df.loc[:, dfeatures]
    y= df.loc[:, target]
    
    from scipy.stats import pearsonr
    out1={}
    for i in range(0,l):
        cor,_=pearsonr(x[dfeatures[i]],y)
        out1[dfeatures[i]]=str(cor)
        print(dfeatures[i]," ",cor)
    print(out1)
    
    return render_template("query2.html",features=dfeatures,t=target,out=out1)


@app.route("/query3",methods=['POST','GET'])
def query3():
    from ast import literal_eval
    import ast
    #db_name="Cervical_Cancer"
    #db_name="Fetal_health_Classification"

    if ch=="fetal":
        db_name="Fetal_health_Classification"
    elif ch=="cervical":
        db_name="Cervical_Cancer"

    conn = psycopg2.connect(database=db_name,
                        user='postgres', password='parpsql', 
                        host='localhost', port='5432')
    
    if db_name=="Cervical_Cancer":
        flag=1
    else:
        flag=0  
  
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute('select * from Table1;')
    df = pd.read_sql_query("SELECT * from Table1", conn)
    cur.execute('select * from Table3')
    coeff_dataset = pd.read_sql_query("SELECT * from Table3", conn)
    conn.commit()
    # print(coeff_dataset['features'])
    cf_features = coeff_dataset['features']  
    global val
    if flag==0:
        cf_coffs1=coeff_dataset['coefficient_1']
        cf_coffs2=coeff_dataset['coefficient_2']
        cf_coffs3=coeff_dataset['coefficient_3']
    else:
        cf_coffs=coeff_dataset['coefficient']


    dfeatures=request.form['features']
    dfeatures=list(dfeatures.split(','))
    val=request.form['values']
    x=df.loc[:, dfeatures]
    y= df.iloc[:, -1:]
    lngth=len(cf_features)
    pos=0
    cnt=0
    pos=0
    for i in range(0,lngth):
        if set(eval(cf_features[i])) == set(dfeatures):
            print("DontGenerate model")
            if flag==0:
                out1 = existingModel3(i,dfeatures,val,cf_coffs1,cf_coffs2,cf_coffs3)
                pos=i
                break
            else:
                out1=existingModel3_1(i,dfeatures,val,cf_coffs)
                pos=i
                break
        else:
            cnt+=1
            
    if(cnt==lngth):
        print("Generate model")
        out1=generateModel3(dfeatures,val,x,y,cur,conn,flag)  

    if flag==0:
        if(out1==1):
            c="normal"     
        elif(out1==2):
            c="suspect"
        else:
            c="pathological"
    else:
        if(out1==0):
            c="Not Detected"
        else:
            c="Detected"

   
    return render_template("query3.html",features=dfeatures,values=val,fet=c)



if __name__ =="__main__":
    app.run(debug=True)