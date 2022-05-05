#from app import * ##1now
import time
import os
import ast
def existingModel(pos,dfeatures,val,cf_coffs):
  start=time.time()
  cfdt1=cf_coffs[pos]
  cfdt=eval(cfdt1)
  print("Type of cfdt",type(cfdt))
  print("Type of cfdt",cfdt)
  print("Type of cfdt",len(cfdt))
  val=val.split(',')
  out=0.0
  for i in range (0,len(cfdt)):
    out=out+float(val[i])*float(cfdt[i])
  end=time.time()
  print("\nTime taken to execute a query from ExistingModel",(end-start))
  return out

#------------------------------------------------------
def generateModel(dfeatures,t,fval,x,y,cur,conn):
  start=time.time()
  from sklearn.model_selection import train_test_split  
  x_train, x_test, y_train, y_test= train_test_split(x, y, test_size= 0.2, random_state=0) 
  #Fitting the MLR model to the training set:  
  from sklearn.linear_model import LinearRegression  
  regressor= LinearRegression()  
  regressor.fit(x_train, y_train) 
  cf=regressor.coef_
  
  # print(cf)
  cflngth=len(cf[0])
  cf=cf[0]
  # print("cf after creating list",cf)
  print("coefficient value is",cf)
  
  
  fval=fval.split(',')
  yfh=0.0
  out=0.0
  for i in range(0, cflngth):
    yfh=yfh+cf[i]*(float(fval[i]))
  
  # print("Fetal health = ", yfh)
  out=yfh 
  #output variable to return to main
  row=[dfeatures,cf]
  #query = ("""insert into Table2 (Features, Coefficient) 
        # values (?,?)""",(dfeatures,cf))
   #position to insert new list  #(index, Features, Coefficient) 
  
  #cur.execute("""insert into Table2 
   #      values (?,?,?)""",(i1,str(dfeatures),str(cf)))  #insert query portion
  cf1=list(cf)

  
  cur.execute('INSERT INTO Table2 VALUES (%s, %s, %s)',(str(dfeatures), str(t), str(cf1)))
  conn.commit()
  cur.execute('Select* from Table2')
  

  #till print is for printing the table2 it is printing but not saved in table or db.
  '''res=cur.fetchall() 
  print("Updated table")
  for ires in res:
      print(ires)
      print("\n")'''
  #conn.commit()
  end=time.time()
  print("\nTime taken to execute a query from GenerateModel",(end-start))
  return yfh
  

#--------------------------------------

    
    #---------------------------------------------------------
import math
import numpy as np
def generateModel3(dfeatures,fval,x,y,cur,conn,flag):
    start=time.time()
    o1=[]
    
    #o2=0.0
    #o3=0.0
    op1=[]
    from sklearn.model_selection import train_test_split  
    x_train, x_test, y_train, y_test= train_test_split(x, y, test_size= 0.2, random_state=0)    
    #Fitting the MLR model to the training set:  
    from sklearn.linear_model import LogisticRegression  
    regressor= LogisticRegression(multi_class='multinomial', solver='lbfgs', penalty='l2', C=1.0)
    regressor.fit(x_train,y_train)

    lg_cf=regressor.coef_
    l=len(lg_cf[0])
    
    fval=fval.split(',')
    if flag==0:
      ln2=3
    else:
      ln2=1
    o1 = [0]*ln2
    op1 = [0]*ln2
    lgcf1= [0]*ln2
    for i in range(0,ln2):
      for j in range(0,l):
        o1[i]=o1[i]+lg_cf[i][j]*float(fval[j])
      #o2=o2+lg_cf[1][i]*float(fval[i])
      #o3=o3+lg_cf[2][i]*float(fval[i])

    for k in range(0,ln2):
      op1[k]=1/(1+math.exp(o1[k]))
    
   # op1=1/(1+math.exp(o1))
    #op2=1/(1+math.exp(o2))
   # op3=1/(1+math.exp(o3))
    out=0.0
    out=max(op1)   
  
    if(flag==0):
      if(out==op1[0]):
        yfh=1
      elif(out==op1[1]):
        yfh=2
      elif(out==op1[2]):
        yfh=3
    else:
      if(out==op1[0]):
        yfh=0
      elif(out==op1[1]):
        yfh=1

   

    row=[dfeatures,lg_cf]

    for k in range(0,ln2):
      lgcf1[k]=list(lg_cf[k])
    #lgcf2=list(lg_cf[1])
    #lgcf3=list(lg_cf[2])

    if flag==0:
      cur.execute('INSERT INTO Table3 VALUES (%s, %s, %s, %s)',(str(dfeatures), str(lgcf1[0]), str(lgcf1[1]), str(lgcf1[2])))
      conn.commit()
      cur.execute('Select* from Table3')
    else:
      cur.execute('INSERT INTO Table3 VALUES (%s, %s)',(str(dfeatures), str(lgcf1[0])))
      conn.commit()
      cur.execute('Select* from Table3')


    end=time.time()
    print("\nTime taken to execute a query from GenerateModel",(end-start))
    print(out)
    return yfh

import numpy as np
def existingModel3(pos,dfeatures,val,cf_coffs1,cf_coffs2,cf_coffs3):
  start=time.time()
  cfdt1=cf_coffs1[pos]
  cfdt2=cf_coffs2[pos]
  cfdt3=cf_coffs3[pos]
  
  
  cfd_1=eval(cfdt1)
  cfd_2=eval(cfdt2)
  cfd_3=eval(cfdt3)

  o1=0.0
  o2=0.0
  o3=0.0
  ln=len(dfeatures)

  print("\nlen",ln)

  l=len(cfd_1)
  val=val.split(',')
  out=0.0
  yfh=0
  for i in range(0,l):
    o1=o1+(float(val[i]))*cfd_1[i]
    o2=o2+(float(val[i]))*cfd_2[i]
    o3=o3+(float(val[i]))*cfd_3[i]

    op1=1/(1+math.exp(o1))
    op2=1/(1+math.exp(o2))
    op3=1/(1+math.exp(o3))

  #check once this part
  out=max(op1,op2,op3)
  if(out==op1):
    yfh=1
  elif(out==op2):
    yfh=2
  elif(out==op3):
    yfh=3
 
  # print("target = ", out)
  end=time.time()
  print("\nTime taken to execute a query from ExistingModel",(end-start))

  return yfh

  ##################################################################


def existingModel3_1(pos,dfeatures,val,cf_coffs):
  start=time.time()
  cfdt1=cf_coffs[pos]
  
  cfd_1=eval(cfdt1)

  o1=0.0
  ln=len(dfeatures)

  print("\nlen",ln)

  l=len(cfd_1)
  val=val.split(',')
  out=0.0
  yfh=0
  for i in range(0,l):
    o1=o1+(float(val[i]))*cfd_1[i]

  op1=1/(1+math.exp(o1))

  if op1<0.5:
    yfh=0
  elif op1>=0.5:
    yfh=1

 
  # print("target = ", out)
  end=time.time()
  print("\nTime taken to execute a query from ExistingModel",(end-start))
  print(op1)
  return yfh