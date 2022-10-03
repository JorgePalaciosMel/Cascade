from flask import Flask,render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = '3306'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'x65wpxMr'
app.config['MYSQL_DB'] = 'db_practicas'
 
mysql = MySQL(app)

app.secret_key = 'mysecretkey'




@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("""
    SELECT ID_venta, fecha_venta, p.producto, z.zona, v.venta, ve.nombre, c.nombre
    FROM ventas v
    JOIN producto p
        USING(ID_producto)
    JOIN zona z 
        USING(ID_zona)
    JOIN vendedor ve 
        USING(ID_vendedor)
    JOIN clientes c
        USING(ID_cliente)
    """)
    data = cur.fetchall()
    cols=["ID_venta", "fecha_venta", "producto", "zona", "venta", "vendedor", "cliente"]
    df_data=pd.DataFrame(data, columns= cols)
    df_data.to_csv("static/csv/data.csv")

    curYr = mysql.connection.cursor()
    curYr.execute("""
    SELECT DISTINCT YEAR(fecha_venta)
    FROM ventas v
    JOIN producto p
        USING(ID_producto)
    JOIN zona z 
        USING(ID_zona)
    JOIN vendedor ve 
        USING(ID_vendedor)
    JOIN clientes c
        USING(ID_cliente)
    """)
    dataYr = curYr.fetchall()

    curProd = mysql.connection.cursor()
    curProd.execute("""
    SELECT DISTINCT p.producto, id_producto
    FROM ventas v
    JOIN producto p
        USING(ID_producto)
    JOIN zona z 
        USING(ID_zona)
    JOIN vendedor ve 
        USING(ID_vendedor)
    JOIN clientes c
        USING(ID_cliente)
    """)
    dataProd = curProd.fetchall()
    return render_template('index.html', contacts = data, Yr = dataYr, Prod = dataProd)


 
@app.route('/filter', methods=["GET","POST"])
def filter():
    if request.method == "POST":
        yr = request.form.getlist("year")
        prod = request.form.getlist("product")
        print(yr)
        print(prod)

        if len(yr)==0 and len(prod)==0: 
            cur = mysql.connection.cursor()
            cur.execute("""
            SELECT ID_venta, fecha_venta, p.producto, z.zona, v.venta, ve.nombre, c.nombre
            FROM ventas v
            JOIN producto p
                USING(ID_producto)
            JOIN zona z 
                USING(ID_zona)
            JOIN vendedor ve 
                USING(ID_vendedor)
            JOIN clientes c
                USING(ID_cliente)
                """)
            data = cur.fetchall()

            curYr = mysql.connection.cursor()
            curYr.execute("""
            SELECT DISTINCT YEAR(fecha_venta)
            FROM ventas v
            JOIN producto p
                USING(ID_producto)
            JOIN zona z 
                USING(ID_zona)
            JOIN vendedor ve 
                USING(ID_vendedor)
            JOIN clientes c
                USING(ID_cliente)
            """)
            dataYr = curYr.fetchall()

            curProd = mysql.connection.cursor()
            curProd.execute("""
            SELECT DISTINCT p.producto, id_producto
            FROM ventas v
            JOIN producto p
                USING(ID_producto)
            JOIN zona z 
                USING(ID_zona)
            JOIN vendedor ve 
                USING(ID_vendedor)
            JOIN clientes c
                USING(ID_cliente)
            """)
            dataProd = curProd.fetchall()
        
        elif len(prod) == 0: 
            cur = mysql.connection.cursor()
            cur.execute("""
            SELECT ID_venta, fecha_venta, p.producto, z.zona, v.venta, ve.nombre, c.nombre
            FROM ventas v
            JOIN producto p
                USING(ID_producto)
            JOIN zona z 
                USING(ID_zona)
            JOIN vendedor ve 
                USING(ID_vendedor)
            JOIN clientes c
                USING(ID_cliente)
            WHERE YEAR(Fecha_venta) IN %s
                """, ([yr]))
            data = cur.fetchall()

            curYr = mysql.connection.cursor()
            curYr.execute("""
            SELECT DISTINCT YEAR(fecha_venta)
            FROM ventas v
            JOIN producto p
                USING(ID_producto)
            JOIN zona z 
                USING(ID_zona)
            JOIN vendedor ve 
                USING(ID_vendedor)
            JOIN clientes c
                USING(ID_cliente)
            WHERE YEAR(Fecha_venta) IN %s
                """, ([yr]))
            dataYr = curYr.fetchall()

            curProd = mysql.connection.cursor()
            curProd.execute("""
            SELECT DISTINCT p.producto, id_producto
            FROM ventas v
            JOIN producto p
                USING(ID_producto)
            JOIN zona z 
                USING(ID_zona)
            JOIN vendedor ve 
                USING(ID_vendedor)
            JOIN clientes c
                USING(ID_cliente)
            WHERE YEAR(Fecha_venta) IN %s
                """, ([yr]))
            dataProd = curProd.fetchall()

        
        elif len(yr) == 0: 
            cur = mysql.connection.cursor()
            cur.execute("""
            SELECT ID_venta, fecha_venta, p.producto, z.zona, v.venta, ve.nombre, c.nombre
            FROM ventas v
            JOIN producto p
                USING(ID_producto)
            JOIN zona z 
                USING(ID_zona)
            JOIN vendedor ve 
                USING(ID_vendedor)
            JOIN clientes c
                USING(ID_cliente)
            WHERE id_producto IN %s 
                """, ([prod]))
            data = cur.fetchall()

            curYr = mysql.connection.cursor()
            curYr.execute("""
            SELECT DISTINCT YEAR(fecha_venta)
            FROM ventas v
            JOIN producto p
                USING(ID_producto)
            JOIN zona z 
                USING(ID_zona)
            JOIN vendedor ve 
                USING(ID_vendedor)
            JOIN clientes c
                USING(ID_cliente)
             WHERE id_producto IN %s 
                """, ([prod]))
            dataYr = curYr.fetchall()

            curProd = mysql.connection.cursor()
            curProd.execute("""
            SELECT DISTINCT p.producto, id_producto
            FROM ventas v
            JOIN producto p
                USING(ID_producto)
            JOIN zona z 
                USING(ID_zona)
            JOIN vendedor ve 
                USING(ID_vendedor)
            JOIN clientes c
                USING(ID_cliente)
            WHERE id_producto IN %s 
                """, ([prod]))
            dataProd = curProd.fetchall()
        
        else:
            cur = mysql.connection.cursor()
            cur.execute("""
            SELECT ID_venta, fecha_venta, p.producto, z.zona, v.venta, ve.nombre, c.nombre
            FROM ventas v
            JOIN producto p
                USING(ID_producto)
            JOIN zona z 
                USING(ID_zona)
            JOIN vendedor ve 
                USING(ID_vendedor)
            JOIN clientes c
                USING(ID_cliente)
            WHERE YEAR(Fecha_venta) IN %s AND Id_producto IN %s
                """, (yr,prod))
            data = cur.fetchall()

            curYr = mysql.connection.cursor()
            curYr.execute("""
            SELECT DISTINCT YEAR(fecha_venta)
            FROM ventas v
            JOIN producto p
                USING(ID_producto)
            JOIN zona z 
                USING(ID_zona)
            JOIN vendedor ve 
                USING(ID_vendedor)
            JOIN clientes c
                USING(ID_cliente)
            WHERE YEAR(Fecha_venta) IN %s AND Id_producto IN %s
                """, (yr,prod))
            dataYr = curYr.fetchall()

            curProd = mysql.connection.cursor()
            curProd.execute("""
            SELECT DISTINCT p.producto, id_producto
            FROM ventas v
            JOIN producto p
                USING(ID_producto)
            JOIN zona z 
                USING(ID_zona)
            JOIN vendedor ve 
                USING(ID_vendedor)
            JOIN clientes c
                USING(ID_cliente)
            WHERE YEAR(Fecha_venta) IN %s AND Id_producto IN %s
                """, (yr,prod))
            dataProd = curProd.fetchall()
    return render_template('index.html', contacts = data, Yr = dataYr, Prod = dataProd)

app.run(host='localhost', port=5000)