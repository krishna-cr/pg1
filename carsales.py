from flask import Flask, render_template, request, redirect
import psycopg2

carsales = Flask(__name__)

def connection():
    s = 'ec2-52-20-166-21.compute-1.amazonaws.com' #Your server(host) name 
    d = 'd5boheh8jqv6r4' 
    u = 'egtxpvycvpssno' #Your login user
    p = '05b6b5956e5dd9abb22143ae9d03d5e0d77a6a4a2abca717de82a24435fd1069' #Your login password
    conn = psycopg2.connect(host=s, user=u, password=p, database=d)
    return conn

@carsales.route("/")
def main():
    cars = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TblCars")
    for row in cursor.fetchall():
        cars.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
    conn.close()
    return render_template("carslist.html", cars = cars)
@carsales.route("/addcar", methods = ['GET','POST'])
def addcar():
    if request.method == 'GET':
        return render_template("addcar.html", car = {})
    if request.method == 'POST':
        id = int(request.form["id"])
        name = request.form["name"]
        year = int(request.form["year"])
        price = float(request.form["price"])
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO TblCars (id, name, year, price) VALUES (%s, %s, %s, %s)", (id, name, year, price))
        conn.commit()
        conn.close()
        return redirect('/')
@carsales.route('/updatecar/<int:id>',methods = ['GET','POST'])
def updatecar(id):
    cr = []
    conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM TblCars WHERE id = %s", (str(id)))
        for row in cursor.fetchall():
            cr.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
        conn.close()
        return render_template("addcar.html", car = cr[0])
    if request.method == 'POST':
        name = str(request.form["name"])
        year = int(request.form["year"])
        price = float(request.form["price"])
        cursor.execute("UPDATE TblCars SET name = %s, year = %s, price = %s WHERE id = %s", (name, year, price, id))
        conn.commit()
        conn.close()
        return redirect('/')
@carsales.route('/deletecar/<int:id>')
def deletecar(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TblCars WHERE id = %s", (str(id)))
    conn.commit()
    conn.close()
    return redirect('/')

if(__name__ == "__main__"):
    carsales.run()
