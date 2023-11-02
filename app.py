from contextlib import redirect_stderr
from flask import Flask, render_template, request,session
import sqlite3 as sql
app = Flask(__name__)

#conn = sql.connect('database.db')
#print("Opened database successfully")

#conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
#print("Table created successfully")

# conn.close()

@app.route('/')
def home():
    name="Student management system"
    return render_template('home.html',name = name)

@app.route('/enternew')
def new_student():
   return render_template('student.html')

@app.route('/login')
def login():
   return render_template('login.html')



#========

@app.route('/log', methods =['GET', 'POST'])
def log():
    mesage = ''
    if request.method == 'POST':
       nm = request.form['nm']
       pin = request.form['pin']
       with sql.connect("database.db") as con:
          cur = con.cursor()
          #cur.execute("SELECT name,pin FROM students WHERE name = '" + name +"'AND pin = '" + pin + "'")
          cur.execute("SELECT name,pin FROM students WHERE name = '"+nm+"' and pin='"+ pin+ "'")
          user = cur.fetchall()
      
          if len(user) == 0:
            #session['loggedin'] = True
            #session['userid'] = user['userid']
            #session['nm'] = user['nm']
            #session['pin'] = user['pin']
            mesage = 'Invalid credentails supplied,Please enter correct name / pin !'
            return render_template('login.html', mesage = mesage)
          else:
            mesage = 'Logged in successfully !'
            return render_template('userplatform.html', mesage = mesage)
      
           
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('nm', None)
    session.pop('pin', None)
    #return redirect_stderr(url_for('login'))
    return render_template('login.html')






@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            
            cur = con.cursor()
            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            
            con.commit()
            msg = "Record successfully added"
            
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True)