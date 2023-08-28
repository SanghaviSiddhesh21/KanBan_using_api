from datetime import datetime,date,timedelta
import os
import base64
from flask import Flask, redirect,render_template, request, session,url_for,Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from flask_bcrypt import Bcrypt
from flask_mail import Mail,Message
from sqlalchemy import func,desc
from flask_restful import Resource,Api,reqparse
from flask_cors import CORS
from celery import Celery
from celery.schedules import crontab

import pandas as pd
import matplotlib.pyplot as plt
import re
import math
import random
import io,csv
import time

current_dir=os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)
bcrypt=Bcrypt(app)
mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(current_dir,"main.sqlite3")
app.config['SECRET_KEY']='thisismysecretkey'
db=SQLAlchemy(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME']='Your Email id'
app.config['MAIL_PASSWORD']='Email id password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER']='Your Email id'
mail = Mail(app)
api=Api(app)
CORS(app)


app.config['CELERY_BROKER_URL'] ='redis://localhost:6379'
app.config['CELERY_RESULT_BACKEND'] ='redis://localhost:6379'
app.config['TIMEZONE']='Asia/Calcutta'
def make_celery(app):
    celery = Celery(
        "app",
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
celery = make_celery(app)



def checkemail(email):
  regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
  if(re.fullmatch(regex, email)):
      return 'true'
  else:
      return 'false'

reg_otp={}
def send_otp(email):
  #print('Inside emailfunction')
  digits = "0123456789"
  OTP = ""
  for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
  message_to_send=f"<b>{OTP}</b>"

  msg = Message("Your Registeration OTP")
  msg.recipients=[email]
  msg.html=message_to_send
  mail.send(msg)
  reg_otp[email]=OTP
  return 'true'

def standardizingListWithCardsAPI(userid):
  alllistid=List_table.query.with_entities(List_table.id,List_table.status).filter_by(uid=userid).all()
  new_alllistid=[]
  newdict_alllistid={}
  #print(alllistid) # => [(1,), (2,)]
  for i in alllistid:
    new_alllistid.append(i[0])
    newdict_alllistid[i[0]]=i[1]
  #print(new_alllistid) # => [1, 2]
  #print(newdict_alllistid) # => {1:'Active'}
  for i in new_alllistid:
    #print(i)
    total_cards=Card_table.query.with_entities(Card_table.id).filter_by(lid=i).all()
    #print(total_cards)
    #print(len(total_cards))
    status=Card_table.query.with_entities(Card_table.status).filter_by(lid=i).all()
    #print(status) #=> [('Active',), ('Completed',)]
    newstatus=[]
    for j in status:
      newstatus.append(j[0])
    newstatus=set(newstatus)
    #print(newstatus,len(newstatus)) # = > {'Completed', 'Active'} 2
    newstatus=list(newstatus)
    if((len(newstatus)==1) and (newstatus[0]=='Completed') and newdict_alllistid[i]!=newstatus):
      updated_list=List_table.query.filter_by(id=i).first()
      updated_list.status='Completed'
    elif((len(newstatus)==1) and (newstatus[0]=='Active') and newdict_alllistid[i]!=newstatus):
      updated_list=List_table.query.filter_by(id=i).first()
      updated_list.status='Active'
    elif((len(newstatus)==2) and (newdict_alllistid[i]=='Completed')):
      updated_list=List_table.query.filter_by(id=i).first()
      updated_list.status='Active'
    elif(len(total_cards)==0):
      updated_list=List_table.query.filter_by(id=i).first()
      updated_list.status='Completed'
    try:
      #print('Hey')
      db.session.add(updated_list)
      db.session.flush()        
    except Exception as error:
      #print('except 1 done')
      db.session.rollback()
    db.session.commit()
  return True

def standardizingListWithCards():
  alllistid=List_table.query.with_entities(List_table.id,List_table.status).filter_by(uid=current_user.id).all()
  new_alllistid=[]
  newdict_alllistid={}
  #print(alllistid) # => [(1,), (2,)]
  for i in alllistid:
    new_alllistid.append(i[0])
    newdict_alllistid[i[0]]=i[1]
  #print(new_alllistid) # => [1, 2]
  #print(newdict_alllistid) # => {1:'Active'}
  for i in new_alllistid:
    #print(i)
    total_cards=Card_table.query.with_entities(Card_table.id).filter_by(lid=i).all()
    #print(total_cards)
    #print(len(total_cards))
    status=Card_table.query.with_entities(Card_table.status).filter_by(lid=i).all()
    #print(status) #=> [('Active',), ('Completed',)]
    newstatus=[]
    for j in status:
      newstatus.append(j[0])
    newstatus=set(newstatus)
    #print(newstatus,len(newstatus)) # = > {'Completed', 'Active'} 2
    newstatus=list(newstatus)
    if((len(newstatus)==1) and (newstatus[0]=='Completed') and newdict_alllistid[i]!=newstatus):
      updated_list=List_table.query.filter_by(id=i).first()
      updated_list.status='Completed'
    elif((len(newstatus)==1) and (newstatus[0]=='Active') and newdict_alllistid[i]!=newstatus):
      updated_list=List_table.query.filter_by(id=i).first()
      updated_list.status='Active'
    elif((len(newstatus)==2) and (newdict_alllistid[i]=='Completed')):
      updated_list=List_table.query.filter_by(id=i).first()
      updated_list.status='Active'
    elif(len(total_cards)==0):
      updated_list=List_table.query.filter_by(id=i).first()
      updated_list.status='Completed'
    try:
      #print('Hey')
      db.session.add(updated_list)
      db.session.flush()        
    except Exception as error:
      #print('except 1 done')
      db.session.rollback()
    db.session.commit()
  return True



login_manager=LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
  return User_registeration.query.get(int(id))

class User_registeration(db.Model,UserMixin):
  __tablename__='user_registeration'
  id=db.Column(db.Integer,primary_key=True,autoincrement=True)
  firstname=db.Column(db.String,nullable=False)
  lastname=db.Column(db.String,nullable=False)
  dateofbirth=db.Column(db.Date,nullable=False)
  emailid=db.Column(db.String,nullable=False)
  username=db.Column(db.String(20),nullable=False,unique=True)
  password=db.Column(db.String(80),nullable=False)
  lists=db.relationship('List_table',backref='user')
  cards=db.relationship('Card_table',backref='user')
class List_table(db.Model):
  __tablename__="list_table"
  id=db.Column(db.Integer,primary_key=True,autoincrement=True)
  name=db.Column(db.String,nullable=False)
  description=db.Column(db.String,nullable=False)
  uid=db.Column(db.Integer,db.ForeignKey('user_registeration.id'))
  status=db.Column(db.String,nullable=False,default='Active')
  cards=db.relationship('Card_table',backref='list')
class Card_table(db.Model):
  __tablename__="card_table"
  id=db.Column(db.Integer,primary_key=True,autoincrement=True)
  title=db.Column(db.String,nullable=False)
  description=db.Column(db.String,nullable=False)
  created_on=db.Column(db.Date)
  due=db.Column(db.Date,nullable=False)
  completed_on=db.Column(db.Date)
  status=db.Column(db.String,nullable=False,default='Active')
  uid=db.Column(db.Integer,db.ForeignKey('user_registeration.id'))
  lid=db.Column(db.Integer,db.ForeignKey('list_table.id'))

  

@app.route('/',methods=['GET','POST'])
def login():
  if request.method=='GET':
    return render_template('Login.html')
  elif request.method=='POST':
    (username,password)=(request.form['login-username'],request.form['login-password'])
    logindata=[{'login-username':username,'login-password':password}]
    #print(username,password)
    if username:
      if password:
        user=User_registeration.query.filter_by(username=username).first()
        if user is None:
          return render_template('Login.html',datapassed='true',usernotfound='true',data=logindata)
        else:
          #hashedpassword=bcrypt.generate_password_hash(password)
          if bcrypt.check_password_hash(user.password,password):
            login_user(user)
            return redirect(url_for('dashboard'))
          else:
            return render_template('Login.html',datapassed='true',incorrectpassword='true',data=logindata)
      else:
        return render_template('Login.html',datapassed='true',passwordnotentered='true',data=logindata)
    else:
      return render_template('Login.html',datapassed='true',usernotentered='true',data=logindata)



@app.route('/Registeration',methods=['GET','POST'])
def registeration():
  if request.method=='GET':
    return render_template('Registeration.html')
  elif request.method=='POST':
    (fname,lname,dob,email,username,password,repass,otp)=(request.form['firstname'],request.form['lastname'],request.form['dob'],request.form['emailid'],request.form['registeration-username'],request.form['registeration-password'],request.form['registeration-repassword'],request.form['OTP'])
    #print(fname,lname,dob,email,username,password,repass)
    userdata=[{'firstname':fname,'lastname':lname,'dob':dob,'emailid':email,'registeration-username':username,'registeration-password':password,'registeration-repassword':repass}]
    if fname:
      if lname:
        if dob:
          if email:
            if username:
              if password:
                if repass:
                  if checkemail(email)!='true':
                    return render_template('Registeration.html',datapassed='true',invalidEmailid='true',data=userdata)
                  if password!=repass:
                    return render_template('Registeration.html',datapassed='true',incorrectPassword='true',data=userdata)
                  userexist=User_registeration.query.filter_by(username=username).first()
                  #print("Pass 1 done")
                  if userexist:
                    return render_template('Registeration.html',datapassed='true',invalidUsername='true',data=userdata)
                  emailexists=User_registeration.query.filter_by(emailid=email).first()
                  if emailexists:
                    return render_template('Registeration.html',datapassed='true',mailAlreadyExists='true',data=userdata)
                  else:
                    if otp=="******":
                      if(send_otp(email)=='true'):
                        return render_template('Registeration.html',datapassed='true',otpsend='true',data=userdata)
                      else:
                        return render_template('Registeration.html',datapassed='true',generalerror="Error in sendgin OTP",data=userdata)
                    else:
                      if(otp.isnumeric() and len(otp)==6):
                        #print(reg_otp[email])
                        if(reg_otp[email]==otp):
                          #print('OTP Validation Successful')
                          del reg_otp[email]
                          hashedpassword=bcrypt.generate_password_hash(password)
                          dob=datetime.strptime(dob,'%Y-%m-%d')
                          new_user=User_registeration(firstname=fname,lastname=lname,dateofbirth=dob,emailid=email,username=username,password=hashedpassword)
                          try:
                            db.session.add(new_user)
                            db.session.flush()        
                          except Exception as error:
                            #print('except 1 done')
                            db.session.rollback()
                            return render_template('Registeration.html',datapassed='true',generalerror="Cannot login at this point please try again later",data=userdata)
                          db.session.commit()
                          db.session.close()
                          return redirect(url_for('login'))
                        else:
                          #print('OTP Validation unuccessful')
                          return render_template('Registeration.html',datapassed='true',otpsend='true',otperror='true',data=userdata)
                      else:
                        return render_template('Registeration.html',datapassed='true',otpsend='true',otperror='true',data=userdata)
                else:
                  return render_template('Registeration.html',datapassed='true',repasswordnotfound='true',data=userdata)
              else:
                return render_template('Registeration.html',datapassed='true',passwordnotfound='true',data=userdata)
            else:
              return render_template('Registeration.html',datapassed='true',usernamenotfound='true',data=userdata)
          else:
            return render_template('Registeration.html',datapassed='true',emailnotfound='true',data=userdata)
        else:
          return render_template('Registeration.html',datapassed='true',dobnotfound='true',data=userdata)
      else:
        return render_template('Registeration.html',datapassed='true',lnamenotfound='true',data=userdata)
    else:
      return render_template('Registeration.html',datapassed='true',fnamenotfound='true',data=userdata)

@app.route('/Dashboard',methods=['GET','POST'])
@login_required
def dashboard():
  if request.method=='GET':
    print(current_user.id)
    return render_template("Dashboard.html",userid=current_user.id)

@app.route('/ListReport',methods=['GET'])
@login_required
def listreport():
  totallistsofuser=List_table.query.with_entities(List_table.id,List_table.name,List_table.description).filter(List_table.uid==current_user.id).all()
  #print(totallistsofuser,len(totallistsofuser))
  totallistofuserstandardized=[]
  for i in totallistsofuser:
    totalcardsoflist=Card_table.query.with_entities(Card_table.id,Card_table.due,Card_table.completed_on).filter(Card_table.lid==i[0]).all()
    completedcardsoflist=Card_table.query.with_entities(Card_table.id,Card_table.title,Card_table.completed_on).filter(Card_table.lid==i[0],Card_table.status=='Completed').all()
    remainingcardsoflist=len(totalcardsoflist)-len(completedcardsoflist)
    #print(totallistofuserstandardized,totalcardsoflist,completedcardsoflist,remainingcardsoflist) # => [] [(4,)] [(4,)] 0
    totallistofuserstandardized.append([i[0],i[1],i[2],len(totalcardsoflist),len(completedcardsoflist),remainingcardsoflist])
    #print(totallistofuserstandardized)
    ontime=0
    defaulter=0
    for j in totalcardsoflist:
      #print(j[1]-j[2])
      if((j[1]-j[2]).days>=0):
        ontime=ontime+1
      else:
        defaulter=defaulter+1
    df = pd.DataFrame({'assignments': [ontime,defaulter]},index=['Ontime', 'Defaulter',])
    plot=df.plot.pie(y='assignments', figsize=(2.7, 2.7))
    fig=plot.get_figure()
    fig.savefig(f'static/my_pie_{i[0]}.jpg')
    completedondict={}
    for j in completedcardsoflist:
      if j[2] in completedondict.keys():
        completedondict[j[2]]=completedondict[j[2]]+1
      else:
        completedondict[j[2]]=1
    df=pd.DataFrame({'frequency': completedondict.values()}, index=completedondict.keys())
    ax=df.plot.bar(rot=0,figsize=(2.7, 2.7))
    fig=ax.get_figure()
    fig.savefig(f'static/bar_{i[0]}.jpg')
    #print(i[0])
    #print(totallistofuserstandardized)
  return render_template('ListReport.html',data=totallistofuserstandardized)

@app.route('/ExportList',methods=['POST'])
@login_required
def exportlist():
  listid=request.form['listid']
  Listdata=List_table.query.with_entities(List_table.name,List_table.description).filter_by(id=listid).first()
  #print(Listdata) # =>("Today's List", 'Exporting List into CSV format')
  Carddata=Card_table.query.with_entities(Card_table.title,Card_table.description,Card_table.created_on,Card_table.due,Card_table.status).filter(Card_table.lid==listid,Card_table.status=='Active').order_by(Card_table.created_on).all()
  #print(Carddata) # => [('Task1', 'Checking input on the terminal of the List', datetime.date(2022, 11, 9), datetime.date(2022, 11, 9)), ('Task2', 'Getting Card input on the terminal', datetime.date(2022, 11, 9), datetime.date(2022, 11, 9))]
  data=[]
  if(Carddata):
    for i in range(len(Carddata)):
      data.append([Listdata[0],Listdata[1]])
    for i in range(len(Carddata)):
      for j in Carddata[i]:
        data[i].append(j)
  #print(data) # => [["Today's List", 'Exporting List into CSV format', 'Task1', 'Checking input on the terminal of the List', datetime.date(2022, 11, 9), datetime.date(2022, 11, 9), 'Active'], ["Today's List", 'Exporting List into CSV format', 'Task2', 'Getting Card input on the terminal', datetime.date(2022, 11, 9), datetime.date(2022, 11, 9), 'Active'], ["Today's List", 'Exporting List into CSV format', 'Task3', 'Getting data on the terminal before adding into csv', datetime.date(2022, 11, 9), datetime.date(2022, 11, 9), 'Active']]
  Carddata2=Card_table.query.with_entities(Card_table.title,Card_table.description,Card_table.created_on,Card_table.due,Card_table.status).filter(Card_table.lid==listid,Card_table.status=='Completed').order_by(Card_table.created_on).all()
  #print(Carddata) # => [('Task1', 'Checking input on the terminal of the List', datetime.date(2022, 11, 9), datetime.date(2022, 11, 9)), ('Task2', 'Getting Card input on the terminal', datetime.date(2022, 11, 9), datetime.date(2022, 11, 9))]
  if(Carddata2):
    for i in range(len(Carddata2)):
      data.append([Listdata[0],Listdata[1]])
    for i in range(len(Carddata2)):
      for j in Carddata2[i]:
        data[len(Carddata)+i].append(j)
  output=io.StringIO()
  writer=csv.writer(output)
  writer.writerow(['List Name','List Description','Card Title','Card Description','Created On','Due by','Card Status'])
  if(data):
    for i in data:
      writer.writerow(i)
    output.seek(0)
  return Response(output,mimetype="text/csv",headers={"Content-Disposition":f"attachment;filename={Listdata[0]}.csv"})

@app.route('/Logout',methods=['GET','POST'])
@login_required
def logout():
  if request.method=='GET':
    logout_user()
    return redirect(url_for('login'))



class ActiveListsAPI(Resource):
  def get(self,userid):
    #print(userid)
    if(userid.isnumeric()):
      #print(userid)
      user=User_registeration.query.filter_by(id=userid).first()
      if(user):
        #print(userid)
        userid=int(userid)
        if(standardizingListWithCardsAPI(userid)):
          allactivelistid=List_table.query.with_entities(List_table.id,List_table.name).filter_by(uid=userid,status='Active').all()
          #print(allactivelistid)#=>[(17, "Today's List")]
          final=[]
          for i in allactivelistid:
            activecardsforid=Card_table.query.with_entities(Card_table.id).filter_by(lid=i[0],status='Active').all()
            completecardsforid=Card_table.query.with_entities(Card_table.id).filter_by(lid=i[0],status='Completed').all()
            allcardsforid=Card_table.query.with_entities(Card_table.id,Card_table.title,Card_table.description,Card_table.due,Card_table.status).filter_by(lid=i[0]).order_by(desc(Card_table.created_on)).all()
            #print(allcardsforid)#=>[(8, 'Task1', 'Adding Vue component wherever required', datetime.date(2022, 11, 25), 'Active')]
            cards=[]
            for j in allcardsforid:
              carddict={'cardid':j[0],'cardtitle':j[1],'carddescription':j[2],'dueby':str(j[3]),'status':j[4]}
              cards.append(carddict)
              newdict={'Listid':i[0],'listname':i[1],'totalcards':len(activecardsforid)+len(completecardsforid),'activecards':len(activecardsforid),'completedcards':len(completecardsforid),'Cards':cards}
            final.append(newdict)
          return(final)
        else:
          pass
      else:
        return({'E002':'True'})
    else:
      return ({'EOO1':'True'})

class CompletedListsAPI(Resource):
  def get(self,userid):
    #print(userid)
    if(userid.isnumeric()):
      #print(userid)
      user=User_registeration.query.filter_by(id=userid).first()
      if(user):
        #print(userid)
        userid=int(userid)
        if(standardizingListWithCardsAPI(userid)):
          allactivelistid=List_table.query.with_entities(List_table.id,List_table.name).filter_by(uid=userid,status='Completed').all()
          #print(allactivelistid)#=>[(17, "Today's List")]
          final=[]
          for i in allactivelistid:
            activecardsforid=Card_table.query.with_entities(Card_table.id).filter_by(lid=i[0],status='Active').all()
            completecardsforid=Card_table.query.with_entities(Card_table.id).filter_by(lid=i[0],status='Completed').all()
            allcardsforid=Card_table.query.with_entities(Card_table.id,Card_table.title,Card_table.description,Card_table.due,Card_table.status).filter_by(lid=i[0]).order_by(desc(Card_table.created_on)).all()
            #print(allcardsforid)#=>[(8, 'Task1', 'Adding Vue component wherever required', datetime.date(2022, 11, 25), 'Active')]
            cards=[]
            for j in allcardsforid:
              carddict={'cardid':j[0],'cardtitle':j[1],'carddescription':j[2],'dueby':str(j[3]),'status':j[4]}
              cards.append(carddict)
            newdict={'Listid':i[0],'listname':i[1],'totalcards':len(activecardsforid)+len(completecardsforid),'activecards':len(activecardsforid),'completedcards':len(completecardsforid),'Cards':cards}
            final.append(newdict)
          return(final)
        else:
          pass
      else:
        return({'E002':'True'})
    else:
      return ({'EOO1':'True'})

class Getallactivecardslist(Resource):
  def get(self,userid):
    if(userid.isnumeric()):
      user=User_registeration.query.filter_by(id=userid).first()
      if(user):
        userid=int(userid)
        if(standardizingListWithCardsAPI(userid)):
          allactivecardslist=List_table.query.with_entities(List_table.id,List_table.name).filter(List_table.uid==userid).all()
          final=[]
          for i in allactivecardslist:
            activecards=Card_table.query.with_entities(Card_table.id,Card_table.title,Card_table.created_on,Card_table.due,Card_table.description).filter(Card_table.lid==i[0],Card_table.uid==userid,Card_table.status=='Active').all()
            cards=[]
            for j in activecards:
              carddict={'cardid':j[0],'cardtitle':j[1],'cardcreatedon':str(j[2]),'carddueby':str(j[3]),'carddescription':j[4]}
              cards.append(carddict)
            newdict={'listid':i[0],'listtitle':i[1],'activecards':cards}
            final.append(newdict)
          return final
        else:
          pass
      else:
        return({'E002':'True'})
    else:
      return ({'EOO1':'True'})


create_list_parser=reqparse.RequestParser()
create_list_parser.add_argument('user_id')
create_list_parser.add_argument('list_name')
create_list_parser.add_argument('list_description')
class AddList(Resource):
  def post(self):
    args=create_list_parser.parse_args()
    user_id=args.get('user_id',None)
    list_name=args.get('list_name',None)
    list_description=args.get('list_description',None)
    #print(user_id,list_name,list_description)
    if(user_id!=None and user_id.isnumeric()):
      if(list_name!=None):
        if(list_description!=None):
          user_id=int(user_id)
          new_list=List_table(name=list_name,description=list_description,uid=user_id)
          try:
            db.session.add(new_list)
            db.session.flush()        
          except Exception as error:
            #print('except 1 done')
            db.session.rollback()
            return ({'E003':True})
          db.session.commit()
          db.session.close()
          return ({'Status':'Successful'})
        else:
          return ({'E001':True})
      else:
        return ({'E001':True})
    else:
      return ({'E001':True})

class CreateCardTabList(Resource):
  def get(self,userid):
    if(userid.isnumeric()):
      user=User_registeration.query.filter_by(id=userid).first()
      if(user):
        userid=int(userid)
        lists=List_table.query.with_entities(List_table.id,List_table.name).filter(List_table.uid==userid).all()
        #print(lists) #=> [(23, 'List Name'), (24, 'New List')]
        finallists=[]
        for i in lists:
          finallists.append({'listid':str(i[0]),'listname':i[1]})
        #print(finallists) #=>[{'listid': 23, 'listname': 'List Name'}, {'listid': 24, 'listname': 'New List'}]
        return finallists
      else:
        return({'E002':'True'})
    else:
      return ({'EOO1':'True'})

create_card_parser=reqparse.RequestParser()
create_card_parser.add_argument('user_id')
create_card_parser.add_argument('card_name')
create_card_parser.add_argument('card_description')
create_card_parser.add_argument('due')
create_card_parser.add_argument('status')
create_card_parser.add_argument('lists_to_add')

class AddCard(Resource):
  def post(self):
    args=create_card_parser.parse_args()
    userid=args.get('user_id',None)
    card_name=args.get('card_name',None)
    card_description=args.get('card_description',None)
    due=args.get('due',None)
    status=args.get('status',None)
    lists_to_add=args.get('lists_to_add',None)
    print(userid,card_name,card_description,due,status,lists_to_add) #=>7 rwv wdv 2022-12-23 yes ["23","28"]
    print(userid)
    if(userid.isnumeric()):
      user=User_registeration.query.filter_by(id=userid).first()
      if(user):
        userid=int(userid)
        if(card_name!=None and card_description!=None):
          if(status!='yes' or status!='no'):
            #print(lists_to_add)
            string=''
            for i in lists_to_add:
              if(i=="\"" or i=="[" or i=="]"):
                pass
              else:
                string=string+i
            #print(string)
            lists_to_add_array=string.split(',')
            #print(lists_to_add_array)
            if(len(lists_to_add)>=1):
              for i in lists_to_add_array:
                #print(i)
                if status=='no':
                  new_list=Card_table(title=card_name,description=card_description,created_on=date.today(),due=datetime.strptime(due,'%Y-%m-%d').date(),completed_on=date.today(),uid=int(userid),lid=int(i))
                else:
                  new_list=Card_table(title=card_name,description=card_description,created_on=date.today(),due=datetime.strptime(due,'%Y-%m-%d').date(),completed_on=date.today(),status='Completed',uid=int(userid),lid=int(i))
                try:
                  db.session.add(new_list)
                  db.session.flush()        
                except Exception as error:
                  db.session.rollback()
                  return ({'E003':True})
              db.session.commit()
              db.session.close()
              return ({'Status':'Successful'})
            else:
              return ({'EOO1':'True'})  
          else:
            return ({'EOO1':'True'})
        else:
          return ({'EOO1':'True'})
      else:
        return({'E002':'True'})
    else:
      return ({'EOO1':'True'})

class Getactivelist(Resource):
  def get(self,userid):
    if(userid.isnumeric()):
      user=User_registeration.query.filter_by(id=userid).first()
      if(user):
        userid=int(userid)
        if(standardizingListWithCardsAPI(userid)):
          allactivelistid=List_table.query.with_entities(List_table.id,List_table.name).filter_by(uid=userid,status='Active').all()
          #print(allactivelistid)#=>[(17, "Today's List")]
          final=[]
          for i in allactivelistid:
            activecardsforid=Card_table.query.with_entities(Card_table.id).filter_by(lid=i[0],status='Active').all()
            completecardsforid=Card_table.query.with_entities(Card_table.id).filter_by(lid=i[0],status='Completed').all()
            allcardsforid=Card_table.query.with_entities(Card_table.id,Card_table.title,Card_table.description,Card_table.due,Card_table.status).filter_by(lid=i[0]).order_by(desc(Card_table.created_on)).all()
            #print(allcardsforid)#=>[(8, 'Task1', 'Adding Vue component wherever required', datetime.date(2022, 11, 25), 'Active')]
            cards=[]
            for j in allcardsforid:
              carddict={'cardid':j[0],'cardtitle':j[1],'carddescription':j[2],'dueby':str(j[3]),'status':j[4]}
              cards.append(carddict)
              newdict={'Listid':i[0],'listname':i[1],'totalcards':len(activecardsforid)+len(completecardsforid),'activecards':len(activecardsforid),'completedcards':len(completecardsforid),'Cards':cards}
            final.append(newdict)
            #print(final)
          return(final)
        else:
          pass
      else:
        return({'E002':'True'})
    else:
      return ({'EOO1':'True'})
  
class Getcompletedlist(Resource):
  def get(self,userid):
    if(userid.isnumeric()):
      user=User_registeration.query.filter_by(id=userid).first()
      if(user):
        userid=int(userid)
        if(standardizingListWithCardsAPI(userid)):
          allactivelistid=List_table.query.with_entities(List_table.id,List_table.name).filter_by(uid=userid,status='Completed').all()
          #print(allactivelistid)#=>[(17, "Today's List")]
          final=[]
          for i in allactivelistid:
            activecardsforid=Card_table.query.with_entities(Card_table.id).filter_by(lid=i[0],status='Active').all()
            completecardsforid=Card_table.query.with_entities(Card_table.id).filter_by(lid=i[0],status='Completed').all()
            allcardsforid=Card_table.query.with_entities(Card_table.id,Card_table.title,Card_table.description,Card_table.due,Card_table.status).filter_by(lid=i[0]).order_by(desc(Card_table.created_on)).all()
            #print(allcardsforid)#=>[(8, 'Task1', 'Adding Vue component wherever required', datetime.date(2022, 11, 25), 'Active')]
            cards=[]
            for j in allcardsforid:
              carddict={'cardid':j[0],'cardtitle':j[1],'carddescription':j[2],'dueby':str(j[3]),'status':j[4]}
              cards.append(carddict)
            newdict={'Listid':i[0],'listname':i[1],'totalcards':len(activecardsforid)+len(completecardsforid),'activecards':len(activecardsforid),'completedcards':len(completecardsforid),'Cards':cards}
            final.append(newdict)
            #print(final)
          return(final)
        else:
          pass
      else:
        return({'E002':'True'})
    else:
      return ({'EOO1':'True'})

class EditingCardDetails(Resource):
  def get(self,cardid):
    if(cardid.isnumeric()):
      carddetails=Card_table.query.with_entities(Card_table.title,Card_table.description,Card_table.due).filter_by(id=cardid).first()
      if(carddetails):
        # print(carddetails) =>('8i7um6yntber', 'tnhbrtvfedc', datetime.date(2022, 12, 30))
        final={'cardtitle':carddetails[0],'carddescription':carddetails[1],'carddue':str(carddetails[2])}
        #print(final)
        finallist=[]
        finallist.append(final)
        return finallist
      else:
        return({'E002':'True'})
    else:
      return ({'EOO1':'True'})

edit_card_parser=reqparse.RequestParser()
edit_card_parser.add_argument('user_id')
edit_card_parser.add_argument('card_id')
edit_card_parser.add_argument('card_name')
edit_card_parser.add_argument('card_description')
edit_card_parser.add_argument('due')
edit_card_parser.add_argument('status')
edit_card_parser.add_argument('lists_to_add')

class EditedCardDetails(Resource):
  def post(self):
    args=edit_card_parser.parse_args()
    cardid=args.get('card_id',None)
    userid=args.get('user_id',None)
    card_name=args.get('card_name',None)
    card_description=args.get('card_description',None)
    due=args.get('due',None)
    status=args.get('status',None)
    lists_to_add=args.get('lists_to_add',None)
    #print(userid,card_name,card_description,due,status,lists_to_add) #=>7 rwv wdv 2022-12-23 yes ["23","28"]
    if(userid.isnumeric()):
      user=User_registeration.query.filter_by(id=userid).first()
      if(user):
        userid=int(userid)
        if(card_name!=None and card_description!=None):
          if(status!='yes' or status!='no'):
            #print(lists_to_add)
            string=''
            for i in lists_to_add:
              if(i=="\"" or i=="[" or i=="]"):
                pass
              else:
                string=string+i
            #print(string)
            lists_to_add_array=string.split(',')
            #print(lists_to_add_array)
            if(cardid.isnumeric()):
              card=Card_table.query.filter_by(id=cardid).first()
              db.session.delete(card)
              db.session.commit()
              ##############################################################################################################
              if(len(lists_to_add)>=1):
                for i in lists_to_add_array:
                  #print(i)
                  if status=='no':
                    new_list=Card_table(title=card_name,description=card_description,created_on=date.today(),due=datetime.strptime(due,'%Y-%m-%d').date(),completed_on=date.today(),uid=int(userid),lid=int(i))
                  else:
                    new_list=Card_table(title=card_name,description=card_description,created_on=date.today(),due=datetime.strptime(due,'%Y-%m-%d').date(),completed_on=date.today(),status='Completed',uid=int(userid),lid=int(i))
                  try:
                    db.session.add(new_list)
                    db.session.flush()        
                  except Exception as error:
                    db.session.rollback()
                    return ({'E003':True})
                db.session.commit()
                db.session.close()
                return ({'Status':'Successful'})
              else:
                return ({'EOO1':'True'})
            else:
              return ({'EOO1':'True'})
          else:
            return ({'EOO1':'True'})
        else:
          return ({'EOO1':'True'})
      else:
        return({'E002':'True'})
    else:
      return ({'EOO1':'True'})

delete_card_parser=reqparse.RequestParser()
delete_card_parser.add_argument('card_id')
class DeleteCard(Resource):
  def post(self):
    args=delete_card_parser.parse_args()
    cardid=args.get('card_id',None)
    if(cardid.isnumeric()):
      card=Card_table.query.filter_by(id=cardid).first()
      if(card):
        db.session.delete(card)
        db.session.commit()
        db.session.close()
      else:
        return({'E002':'True'})
    else:
      return ({'EOO1':'True'})
    
class Dashboarddata(Resource):
  def get(self,userid):
    if(userid.isnumeric()):
      user=User_registeration.query.filter_by(id=userid).first()
      if(user):
        userid=int(userid)
        if(standardizingListWithCardsAPI(userid)):
          allactivecardslist=List_table.query.with_entities(List_table.id,List_table.name).filter(List_table.uid==userid,List_table.status=='Active').all()
          final=[]
          for i in allactivecardslist:
            activecards=Card_table.query.with_entities(Card_table.id,Card_table.title,Card_table.created_on,Card_table.due,Card_table.description).filter(Card_table.lid==i[0],Card_table.uid==userid,Card_table.status=='Active').all()
            cards=[]
            for j in activecards:
              carddict={'cardid':j[0],'cardtitle':j[1],'cardcreatedon':str(j[2]),'carddueby':str(j[3]),'carddescription':j[4]}
              cards.append(carddict)
            newdict={'listid':i[0],'listtitle':i[1],'activecards':cards}
            final.append(newdict)
          return final
        else:
          pass
      else:
        return({'E002':'True'})
    else:
      return ({'EOO1':'True'})

class EditListdata(Resource):
  def get(self,listid):
    if(listid.isnumeric()):
      listdetails=List_table.query.with_entities(List_table.name,List_table.description).filter_by(id=listid).first()
      if(listdetails):
        # print(carddetails) =>('8i7um6yntber', 'tnhbrtvfedc', datetime.date(2022, 12, 30))
        final={'listtitle':listdetails[0],'listdescription':listdetails[1]}
        #print(final)
        finallist=[]
        finallist.append(final)
        return finallist
      else:
        return({'E002':'True'})
    else:
      return ({'EOO1':'True'})

edit_list_parser=reqparse.RequestParser()
edit_list_parser.add_argument('list_id')
edit_list_parser.add_argument('user_id')
edit_list_parser.add_argument('list_name')
edit_list_parser.add_argument('list_description')
class EditedListdata(Resource):
  def post(self):
    args=edit_list_parser.parse_args()
    list_id=args.get('list_id',None)
    user_id=args.get('user_id',None)
    list_name=args.get('list_name',None)
    list_description=args.get('list_description',None)
    #print(user_id,list_name,list_description)
    if(user_id!=None and user_id.isnumeric()):
      if(list_name!=None):
        if(list_description!=None):
          if(list_id):
            user_id=int(user_id)
            new_list=List_table.query.filter(List_table.id==list_id,List_table.uid==user_id).first()
            if(new_list):
              new_list.name=list_name
              new_list.description=list_description
              try:
                db.session.flush()        
              except Exception as error:
                #print('except 1 done')
                db.session.rollback()
                return ({'E003':True})
              db.session.commit()
              db.session.close()
              return ({'Status':'Successful'})
            else:
              return ({'E002':True})
          else:
            return ({'E001':True})
        else:
          return ({'E001':True})
      else:
        return ({'E001':True})
    else:
      return ({'E001':True})

delete_list_parser=reqparse.RequestParser()
delete_list_parser.add_argument('list_id')
class DeleteList(Resource):
  def post(self):
    args=delete_list_parser.parse_args()
    listid=args.get('list_id',None)
    #print(listid)
    if(listid.isnumeric()):
      allcards=Card_table.query.filter(Card_table.lid==listid).all()
      if(len(allcards)>0):
        #print(allcards)
        try:
          for i in allcards:
            db.session.delete(i)
            db.session.commit()
            lists=List_table.query.filter(List_table.id==listid).first()
            try:
              db.session.delete(lists)
              db.session.commit()
            except Exception as error:
              db.session.rollback()
              return ({'Status':'Unsuccessful'})
        except Exception as error:
          db.session.rollback()
          return ({'Status':'Unsuccessful'})
        db.session.close()
        return ({'Status':'Successful'})
      else:
        return ({'E002':'True'})
    else:
      return ({'EOO1':'True'})

class ListReport(Resource):
  def get(self,user_id):
    if(user_id.isnumeric()):
      userid=user_id
      user=User_registeration.query.filter_by(id=userid).first()
      if(user):
        userid=int(userid)
        if(standardizingListWithCardsAPI(userid)):
          totallistsofuser=List_table.query.with_entities(List_table.id,List_table.name,List_table.description).filter(List_table.uid==userid).all()
          #print(totallistsofuser,len(totallistsofuser))
          totallistofuserstandardized=[]
          final=[]
          for i in totallistsofuser:
            totalcardsoflist=Card_table.query.with_entities(Card_table.id,Card_table.due,Card_table.completed_on).filter(Card_table.lid==i[0]).all()
            completedcardsoflist=Card_table.query.with_entities(Card_table.id,Card_table.title,Card_table.completed_on).filter(Card_table.lid==i[0],Card_table.status=='Completed').all()
            remainingcardsoflist=len(totalcardsoflist)-len(completedcardsoflist)
            #print(totallistofuserstandardized,totalcardsoflist,completedcardsoflist,remainingcardsoflist) # => [] [(4,)] [(4,)] 0
            totallistofuserstandardized.append([i[0],i[1],i[2],len(totalcardsoflist),len(completedcardsoflist),remainingcardsoflist])
            # print(totallistofuserstandardized)
            # print('###################')
            totalcards=totallistofuserstandardized[-1][3]
            completedcards=totallistofuserstandardized[-1][4]
            remainingcards=totallistofuserstandardized[-1][5]
            ontime=0
            defaulter=0
            for j in totalcardsoflist:
              # print('###################')
              #print(j[1]-j[2])
              if((j[1]-j[2]).days>=0):
                ontime=ontime+1
              else:
                defaulter=defaulter+1
            # print(defaulter,ontime)
            if(defaulter!=0 and ontime!=0):
              df = pd.DataFrame({'assignments': [ontime,defaulter]},index=['Ontime', 'Defaulter',])
              plot=df.plot.pie(y='assignments', figsize=(2.7, 2.7))
              fig=plot.get_figure()
              fig.savefig(f'static/my_pie.jpg')
              completedondict={}
              for j in completedcardsoflist:
                if j[2] in completedondict.keys():
                  completedondict[j[2]]=completedondict[j[2]]+1
                else:
                  completedondict[j[2]]=1
              df=pd.DataFrame({'frequency': completedondict.values()}, index=completedondict.keys())
              ax=df.plot.bar(rot=0,figsize=(2.7, 2.7))
              fig=ax.get_figure()
              fig.savefig(f'static/bar.jpg')
              #print(i[0])
              #print(totallistofuserstandardized)
              with open("static/my_pie.jpg", "rb") as img_file:
                pie64= base64.b64encode(img_file.read()).decode('utf8')
              with open("static/bar.jpg", "rb") as img_file:
                bar64= base64.b64encode(img_file.read()).decode('utf8')
              # print('###################')
              final.append({'listid':i[0],'listname':i[1],'totalcards':totalcards,'completedcards':completedcards,'remainingcards':remainingcards,'pie':pie64,'bar':bar64})
          return final
        else:
          pass
      else:
        return({'E002':'True'})
    else:
      return ({'EOO1':'True'})


api.add_resource(ActiveListsAPI,'/api/getallactivelists/<string:userid>')
api.add_resource(CompletedListsAPI,'/api/getallcompletelists/<string:userid>')
api.add_resource(Getallactivecardslist,'/api/getallactivecardsfromlists/<string:userid>')
api.add_resource(AddList,'/api/createlist')
api.add_resource(CreateCardTabList,'/api/createcardtablist/<string:userid>')
api.add_resource(AddCard,'/api/createcard')
api.add_resource(Getactivelist,'/api/getactivelist/<string:userid>')
api.add_resource(Getcompletedlist,'/api/getcompletedlist/<string:userid>')
api.add_resource(EditingCardDetails,'/api/geteditcarddetails/<string:cardid>')
api.add_resource(EditedCardDetails,'/api/posteditedcarddetails')
api.add_resource(DeleteCard,'/api/deletecard')
api.add_resource(Dashboarddata,'/api/dashboarddata/<string:userid>')
api.add_resource(EditListdata,'/api/editlistdata/<string:listid>')
api.add_resource(EditedListdata,'/api/edittedlist')
api.add_resource(DeleteList,'/api/deletelist')
# api.add_resource(ListReport,'/api/userlistreport/<string:user_id>')


@celery.task()
def return_random():
    time.sleep(5)
    return random.random()

@celery.task()
def dailyemails():
    users=User_registeration.query.with_entities(User_registeration.id,User_registeration.emailid).all()
    print('Checkpoint 01')
    print(users)# => [(4,), (5,)]
    finalusers=[]
    for i in users:
      allcardsforid=Card_table.query.with_entities(Card_table.title,Card_table.description,Card_table.due).filter_by(uid=i[0],status='Active').order_by(Card_table.due).all()
      print(allcardsforid)# => [('Task1', "Today's List new", datetime.date(2022, 11, 29)), ('Task1', "Today's List new", datetime.date(2022, 11, 28))]
      if(allcardsforid):
        finalusers.append([i[1],allcardsforid])
    print(finalusers)# = > [[4//emailIdInPlaceOfThis, [('Task1', "Today's List new", datetime.date(2022, 11, 30)), ('Task2', "Today's List new", datetime.date(2022, 11, 30))]], [5//emailIdInPlaceOfThis, [('Task1', "Today's List new", datetime.date(2022, 11, 28)), ('Task1', "Today's List new", datetime.date(2022, 11, 29))]]]
    print('Checkpoint 02')
    for i in finalusers:
      msg = Message("Good Morning!")
      msg.recipients=[i[0]]
      msg.html=render_template('Dailyreminder.html',data=i[1])
      mail.send(msg)
      print('True')

@celery.task()
def montlyemails():
  users=User_registeration.query.with_entities(User_registeration.id,User_registeration.emailid).all()
  finalusers=[]
  for i in users:
    totalactivecards=len(Card_table.query.with_entities(Card_table.id).filter(Card_table.created_on.between(datetime.now()-timedelta(days=37),datetime.now()-timedelta(days=7)),Card_table.uid==i[0],Card_table.status=='Active').all())
    totalcompletedcards=len(Card_table.query.with_entities(Card_table.id).filter(Card_table.created_on.between(datetime.now()-timedelta(days=37),datetime.now()-timedelta(days=7)),Card_table.uid==i[0],Card_table.status=='Completed').all())
    totalcards=totalactivecards+totalcompletedcards
    totaldefaultedcards_butcompleted=len(Card_table.query.with_entities(Card_table.id).filter(Card_table.created_on.between(datetime.now()-timedelta(days=37),datetime.now()-timedelta(days=7)),Card_table.uid==i[0],Card_table.status=='Complete',Card_table.completed_on>Card_table.due).all())
    totaldefaultedcards_andactive=len(Card_table.query.with_entities(Card_table.id).filter(Card_table.created_on.between(datetime.now()-timedelta(days=37),datetime.now()-timedelta(days=7)),Card_table.uid==i[0],Card_table.status=='Active',(datetime.now()-timedelta(days=7))>Card_table.due).all())
    totaldefaulted=totaldefaultedcards_butcompleted+totaldefaultedcards_andactive
    # print(totalcards)
    # print(totalactivecards)
    # print(totalcompletedcards)
    # print(totaldefaultedcards)
    # images=[]
    # df1=pd.DataFrame({'Status': [totalactivecards,totalcompletedcards]},index=['Active','Completed'])
    # plot1=df1.plot.pie(`y='Status', figsize=(5, 5))
    # fig=plot1.get_figure()
    # fig.savefig(f'static/piechart1.jpg')
    # with open("static/piechart1.jpg", "rb") as img_file:
    #   my_string = base64.b64encode(img_file.read()).decode('utf8')
    #   images.append(my_string)
    # df2=pd.DataFrame({'Defaulting':[totalcards,totaldefaultedcards]},index=['Total Tasks','Defaulted Tasks'])
    # plot2=df2.plot.pie(y='Defaulting', figsize=(5, 5))
    # fig=plot2.get_figure()
    # fig.savefig(f'static/piechart2.jpg')
    # with open("static/piechart2.jpg", "rb") as img_file:
    #   my_string = base64.b64encode(img_file.read()).decode('utf8')
    #   images.append(my_string)
    # #print(images)
    # finalusers.append([i[1],images])
    secondelement=[]
    if(totalcards==0):
      Completion_percentage='N/A'
      Active_precentage='N/A'
    else:
      Completion_percentage=str((totalcompletedcards/totalcards)*100)+' %'
      Active_precentage=str((totalactivecards/totalcards)*100)+' %'
    if(totaldefaulted==0):
      Completed_butdefaulted='N/A'
      Active_anddefauted='N/A'
    else:
      Completed_butdefaulted=str((totaldefaultedcards_butcompleted/totaldefaulted)*100)+' %'
      Active_anddefauted=str((totaldefaultedcards_andactive/totaldefaulted)*100)+' %'
    secondelement.append(totalcards)
    secondelement.append(Completion_percentage)
    secondelement.append(Active_precentage)
    secondelement.append(Completed_butdefaulted)
    secondelement.append(Active_anddefauted)
    finalusers.append([i[1],secondelement])
  # print(finalusers)
  # print('Done1')
  for i in finalusers:
    msg = Message("Monthly Progress!")
    msg.recipients=[i[0]]
    #print(len(i[1]))
    #print(render_template('Monthlyreport.html',data=i[1]))
    msg.html=render_template('Monthlyreport.html',data=i[1])
    mail.send(msg)
    # print('True')


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(10.0, return_random.s(), name='add every 10')

    # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    
    sender.add_periodic_task(
        10.0,
        # crontab(minute=0, hour=8),
        dailyemails.s()
    )

    sender.add_periodic_task(
        10.0,
        # crontab(minute=0, hour=8,day_of_month='1'),
        montlyemails.s()
    )

if __name__=='__main__':
  #print(os.environ.get('flask_email'))
  app.run(host='0.0.0.0',port=8080)