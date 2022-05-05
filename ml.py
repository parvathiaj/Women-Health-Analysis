
import sqlite3
import pandas as pd
dbname = 'FetalClassificatiopnDb'
conn = sqlite3.connect(dbname + '.sqlite')
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
db_df = pd.read_csv('fetal_health.csv')
db_df.to_sql(name='Table1', con=conn)
cur.execute('SELECT * FROM Table1')
model_df = pd.read_csv('Modeldata.csv')
model_df.to_sql(name='Table2', con=conn)
cur.execute('SELECT * FROM Table2')
names = list(map(lambda x: x[0], cur.description)) #Returns the column names
print(names)
#cur.close()
df = pd.read_sql_query("SELECT * from Table1", conn)
print(df)
df_new = pd.read_sql_query("SELECT * from Table2", conn)
print(df_new)

# importing libraries  
import numpy as np
import matplotlib.pyplot as plt
#importing datasets  
data_set=pd.read_sql_query("SELECT * from Table1", conn)

print(data_set.head())

#data_set

#Taking parameters as user input
inp_string=input("Enter Features:")
lst=inp_string.split(",")

t=input("Enter Target:")

#lst

#Extracting Independent and dependent Variable  
#x= data_set.iloc[:, :-1].values  
#lst=['baseline value','fetal_movement','prolongued_decelerations','histogram_max']
x=data_set.loc[:, lst]
y= data_set.loc[:, t]
#y= data_set.iloc[:, 21].values

#x

#y

"""**GENERATE MODEL OR NOT**"""

dfeatures=input("Enter features:")
dfeatures=dfeatures.split(',')
#dfeatures

#Reading the csv file with coeff and features
from ast import literal_eval
coeff_dataset=  pd.read_sql_query("SELECT * from Table2", conn)
print(coeff_dataset)
 
#
#above code "converters=" is used to convert the features which was initially stored as string to a list

#converting string of list to list
import ast
coeff_dataset['Coefficient'] = coeff_dataset['Coefficient'].apply(ast.literal_eval)

print(coeff_dataset['Features'])

print(coeff_dataset['Coefficient'])

cf_features = coeff_dataset['Features']  
print(cf_features)
#cf_features

cf_coffs=coeff_dataset['Coefficient']
#cf_coffs

lngth=len(cf_features)
pos=0
for i in range(0,lngth):
  if set(cf_features[i]) == set(dfeatures):
    print("Dont generate model")
    pos=i
  else:
    print("Generate model")

"""**Use existing model:**"""

def existingModel():
  cfdt=cf_coffs[pos]
  val=input("Enter values:")
  val=val.split(',')
  out=0.0
  for i in range (0,len(cfdt)): #cfdt inside len
    out=out+float(val[i])*(cfdt[i])
  print("Target value:",out)
  if (out<=1):
    out=1
  elif (out>1) & (out<=2):
    out=2
  elif (out>2) & (out<=3):
    out=3
  print("Fetal health = ", out)
  return out

def generateModel():

  cfdt=cf_coffs[pos] #pos is the position of the existing coefficients list
#cfdt

#coeff_dataset.iloc[:, 0].values #not needed

#cf_coffs

  val=input("Enter values:")
  val=val.split(',')
  out=0.0
  for i in range (0,len(cfdt)): #cfdt inside len
    out=out+float(val[i])*(cfdt[i])
  print("Target value:",out)
  if (out<=1):
    out=1
  elif (out>1) & (out<=2):
    out=2
  elif (out>2) & (out<=3):
    out=3
  print("Fetal health = ", out)

"""**Training the model and Accuracy**"""

# Splitting the dataset into training and test set.  
from sklearn.model_selection import train_test_split  
x_train, x_test, y_train, y_test= train_test_split(x, y, test_size= 0.2, random_state=0)

#Fitting the MLR model to the training set:  
from sklearn.linear_model import LinearRegression  
regressor= LinearRegression()  
regressor.fit(x_train, y_train)

#coefficients values
cf=regressor.coef_
print(cf)

#Converting those coefficient array to list
cf=cf.tolist()
print(cf)
type(cf)

type(cf[0])

#Predicting fetal health
fnew=input("Enter features:")
fcolname=fnew.split(',')
fval=input("Enter value:")
fval=fval.split(',')
yfh=0.0
for i in range(0, len(cf)):
  yfh+=cf[i]*(float(fval[i]))
if (yfh<=1):  #<1 normal coz v are getting neg values
  yfh=1
elif (yfh>1) & (yfh<=2):
  yfh=2
elif (yfh>2) & (yfh<=3):
  yfh=3
print("Fetal health = ", yfh)

#fcolname
#fcoeff=regressor.coef_

#type(fcoeff)

print(fcolname)
#cf #fcoeff

#Use only while creating a new file to store the features and coefficients
import csv
from csv import writer
fieldnames = ['Features', 'Coefficient']
with open('Modeldata.csv', 'w', encoding='UTF8', newline='') as f:
  writer = csv.DictWriter(f, fieldnames=fieldnames)
  writer.writeheader()

import csv
from csv import writer

row=[fcolname,cf]
with open('Modeldata.csv', 'a', encoding='UTF8', newline='') as f_object:  
    # Pass the CSV  file object to the writer() function
    writer_object = writer(f_object)
    # Result - a writer object
    # Pass the data in the list as an argument into the writerow() function
    writer_object.writerow(row)  
    # Close the file object
    f_object.close()

# from google.colab import files
# files.download('Modeldata.csv')

#Predicting the Test set result  
y_pred= regressor.predict(x_test)

#x_test

#y_pred

#y_test

print('Train Score: ', regressor.score(x_train, y_train))  
print('Test Score: ', regressor.score(x_test, y_test))