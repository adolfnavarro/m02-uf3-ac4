# -*- coding: utf-8 -*-
"""
Created on February 2023

@author: Albert ETPX  and modified by Adolf Navarro
"""

# Importación de módulos externos
import mysql.connector
from flask import Flask,render_template,request;

# Funciones de backend #############################################################################

# connectBD: conecta a la base de datos users en MySQL
def connectBD():
    db = mysql.connector.connect(
        # host = "localhost",
        host="127.0.0.1",
        user = "root",
        passwd = "holamundo1984",
        database = "users"
    )
    return db

# initBD: crea una tabla en la BD users, con un registro, si está vacía
def initBD():
    bd=connectBD()
    cursor=bd.cursor()
    
    # cursor.execute("DROP TABLE IF EXISTS users;")
    # Operación de creación de la tabla users (si no existe en BD)
    query="CREATE TABLE IF NOT EXISTS users(\
            user varchar(30) primary key,\
            password varchar(30),\
            name varchar(30), \
            surname1 varchar(30), \
            surname2 varchar(30), \
            age integer, \
            genre enum('H','D','NS/NC')); "
    cursor.execute(query)
            
    # Operación de inicialización de la tabla users (si está vacía)
    query="SELECT count(*) FROM users;"
    cursor.execute(query)
    count = cursor.fetchall()[0][0]
    if(count == 0):
        query = "INSERT INTO users \
            VALUES('user01','admin','Ramón','Sigüenza','López',35,'H');"
        cursor.execute(query)

    bd.commit()
    bd.close()
    return

# checkUser: comprueba si el par usuario-contraseña existe en la BD
def checkUser(user,password):
    bd=connectBD()
    cursor=bd.cursor()

    query=f"SELECT user,name,surname1,surname2,age,genre FROM users WHERE user=%s\
            AND password=%s"
    values=(user,password)
    print(query,values)
    cursor.execute(query,values)
    userData = cursor.fetchall()
    bd.close()
    
    if userData == []:
        return False
    else:
        return userData[0]

# cresteUser: crea un nuevo usuario en la BD
def createUser(user,password,name,surname1,surname2,age,genre):
    bd=connectBD()
    cursor=bd.cursor()
    query = f"INSERT INTO users \
            VALUES(%s,%s,%s,%s,%s,%s,%s);"
    age=int(age)
    values=(user,password,name,surname1,surname2,age,genre)
    print(type(user))
    print(type(age))
    cursor.execute(query,values)
    bd.commit()
    bd.close()
    return

# Secuencia principal: configuración de la aplicación web ##########################################
# Instanciación de la aplicación web Flask
app = Flask(__name__)

# Declaración de rutas de la aplicación web
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    initBD()
    return render_template("login.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/results",methods=('GET', 'POST'))
def results():
    if request.method == ('POST'):
        formData = request.form
        user=formData['usuario']
        password=formData['contrasena']
        userData = checkUser(user,password)

        if userData == False:
            return render_template("results.html",login=False)
        else:
            EjercicioBigDATA(userData[4],userData[5])
            return render_template("results.html",login=True,userData=userData)

@app.route("/newUser",methods=('GET', 'POST'))
def newUser():
    if request.method == ('POST'):
        formData = request.form
        user=formData['usuario']
        password=formData['contraseña']
        name=formData['nombre']
        surname1=formData['apellido1']
        surname2=formData['apellido2']
        age=formData['edad']
        genre=formData['genero']
        createUser(user,password,name,surname1,surname2,age,genre)    
        return render_template("home.html")
    

           


# --------------------------- Big DATA ------------------------------------------------------------

def EjercicioBigDATA(edad,sexo):
    # %%
    import pandas as pd
    # import os 


    seriesPobl = pd.DataFrame()

    seriesPobl = pd.read_csv(f"recursos/seriespoblacionales.csv",sep=";")

    seriesPobl

    # %%
    seriesPobl.dtypes

    # %%
    seriesPobl.loc[seriesPobl.duplicated()]

    # %%
    seriesPobl=seriesPobl.loc[seriesPobl["Sexo"] != "Sexo"]

    # %%
    seriesPobl.loc[seriesPobl.duplicated()]

    # %%
    seriesPobl.loc[seriesPobl["Sexo"]=="Sexo"]

    # %%
    seriesPobl.iloc[13] # Hay un error producido por  los . en los numeros


    # %%
    seriesPobl=seriesPobl.replace(regex="[.]",value="")  # Reemplazamos los puntos

    # %%

    seriesPobl["Total"] = pd.to_numeric(seriesPobl["Total"])
    seriesPobl.dtypes

    # %%
    seriesPobl2022=seriesPobl.loc[seriesPobl["Año"]==2022]
    seriesPobl2022


    # %%
    seriesPobl2022=seriesPobl2022.drop(columns=["Año"])

    seriesPobl2022


    # %%
    seriesPobl2022Hombres=seriesPobl2022.loc[seriesPobl["Sexo"]=="Hombres"]    # Hacemos un dataframe para los hombres y otro para las mujeres 
    seriesPobl2022Mujeres=seriesPobl2022.loc[seriesPobl["Sexo"]=="Mujeres"]

    # %%
    seriesPobl2022HombresPorGrupo=seriesPobl2022Hombres.groupby("Edad (grupos quinquenales)")
    seriesPobl2022MujeresPorGrupo=seriesPobl2022Mujeres.groupby("Edad (grupos quinquenales)")

    # %%
    seriesPobl2022HombresPorGrupo=seriesPobl2022HombresPorGrupo.aggregate('sum')
    seriesPobl2022MujeresPorGrupo=seriesPobl2022MujeresPorGrupo.aggregate('sum')



    # %%
    seriesPobl2022HombresPorGrupo  

    # %%
    # Hay que reordenar las filas 
    seriesPobl2022HombresPorGrupo=seriesPobl2022HombresPorGrupo.reindex(["0-4 años",	
    "5-9 años",
    "10-14 años",
    "15-19 años",
    "20-24 años",
    "25-29 años",
    "30-34 años",
    "35-39 años",
    "40-44 años",	
    "45-49 años",	
    "50-54 años",
    "55-59 años",
    "60-64 años",
    "65-69 años",
    "70-74 años",
    "75-79 años",
    "80-84 años",
    "85-89 años",
    "90-94 años",
    "95-99 años",
    "100 años y mñs"])

    seriesPobl2022MujeresPorGrupo=seriesPobl2022MujeresPorGrupo.reindex(["0-4 años",	
    "5-9 años",
    "10-14 años",
    "15-19 años",
    "20-24 años",
    "25-29 años",
    "30-34 años",
    "35-39 años",
    "40-44 años",	
    "45-49 años",	
    "50-54 años",
    "55-59 años",
    "60-64 años",
    "65-69 años",
    "70-74 años",
    "75-79 años",
    "80-84 años",
    "85-89 años",
    "90-94 años",
    "95-99 años",
    "100 años y mñs"])


    # %%
    seriesPobl2022MujeresPorGrupo

    # %%
    # seriesPobl2022MujeresPorGrupo.plot(kind="bar")       

    # %%
    MujeresCantidad=list(seriesPobl2022MujeresPorGrupo["Total"])
    HombresCantidad=list(seriesPobl2022HombresPorGrupo["Total"])

    rangosEdad=["0-4 años",	
    "5-9 años",
    "10-14 años",
    "15-19 años",
    "20-24 años",
    "25-29 años",
    "30-34 años",
    "35-39 años",
    "40-44 años",	
    "45-49 años",	
    "50-54 años",
    "55-59 años",
    "60-64 años",
    "65-69 años",
    "70-74 años",
    "75-79 años",
    "80-84 años",
    "85-89 años",
    "90-94 años",
    "95-99 años",
    "100 años y mñs"]
    rangosEdadNum=[i for i in range(0,21)]




    # %%




    # %%
    EdadPersona=edad    # Los datos vienen de fuera de la funcion
    SexoPersona=sexo     

    # Para identificar el rango de edad al que pertenece la persona 
    if EdadPersona<5:
        RangoPersona=1
    elif EdadPersona<10:
        RangoPersona=2
    elif EdadPersona<15:
        RangoPersona=3
    elif EdadPersona<20:
        RangoPersona=4
    elif EdadPersona<25:
        RangoPersona=5
    elif EdadPersona<30:
        RangoPersona=6
    elif EdadPersona<35:
        RangoPersona=7
    elif EdadPersona<40:
        RangoPersona=8
    elif EdadPersona<45:
        RangoPersona=9
    elif EdadPersona<50:
        RangoPersona=10
    elif EdadPersona<55:
        RangoPersona=11
    elif EdadPersona<60:
        RangoPersona=12
    elif EdadPersona<65:
        RangoPersona=13
    elif EdadPersona<70:
        RangoPersona=14
    elif EdadPersona<75:
        RangoPersona=15
    elif EdadPersona<80:
        RangoPersona=16
    elif EdadPersona<85:
        RangoPersona=17
    elif EdadPersona<90:
        RangoPersona=18
    elif EdadPersona<95:
        RangoPersona=19
    elif EdadPersona<100:
        RangoPersona=20
    elif EdadPersona>=100:
        RangoPersona=21

    listaColoresH=["b" for i in range(0,21)]  # LLeno una lista de 21 "b"
    listaColoresM=["m" for i in range(0,21)]  # LLeno una lista de 21 "b"

    listaColoresH[RangoPersona-1]="y"   # Asigno en la posicion que toque  el color amarillo  
    listaColoresM[RangoPersona-1]="y"   # Asigno en la posicion que toque  el color amarillo  
    listaColoresH

    # %%

    from matplotlib import pyplot as plt
    fig, axs = plt.subplots(1,2,figsize=(13,7)) 
        # # Configuro  sistema d'eixos 
    plt.title("Piramide Poblacional")     
    

    # Printar la barra de edad que pertoque de la persona en amarillo
    if SexoPersona=="H":
        axs[0].barh(rangosEdad,HombresCantidad, color=listaColoresH, label='Hombres')
        axs[1].barh(rangosEdad,MujeresCantidad, color="m", label='Mujeres')

    if SexoPersona=="D":
        axs[0].barh(rangosEdad,HombresCantidad, color="b", label='Hombres')
        axs[1].barh(rangosEdad,MujeresCantidad, color=listaColoresM, label='Mujeres')

    # Resto parametros Grafico Hombre
    axs[0].legend()
    axs[0].set_title("Hombres")
    axs[0].tick_params(axis='both', which='major', labelsize=7)
    axs[0].set_ylabel ("Rangos de edad")
    axs[0].set_xlabel ("Millones de personas")
    axs[0].invert_xaxis()                          # Giro el grafico 
    axs[0].set_yticks(rangosEdadNum,rangosEdad)    
        
    # Resto parametros Grafico Mujer 
    axs[1].legend()
    axs[1].set_title("Mujeres")
    axs[1].set_xlabel ("Millones de personas")
    axs[1].tick_params(axis='both', which='major', labelsize=7)
    axs[1].set_yticks([])    # Vacio los strings del eje Y 


    # # Configuro com es mostren el subplot i  mostro la figura
    plt.tight_layout()

    #Guardem el grafic 
    plt.savefig(fname="static/grafico",
                # bbox_inches ="tight",
                # pad_inches = 1,
                # transparent = True,
                # facecolor ="g",
                # edgecolor ='w',
                # orientation ='landscape'
                )
    
    # plt.show()          # Mostro i deixo visible la FIGURA 
    
    return


# Configuración y arranque de la aplicación web
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run(host='localhost', port=5000, debug=True)

