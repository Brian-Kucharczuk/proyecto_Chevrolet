#--------------------------------------------------------------------
# Instalar con pip install mysql-connector-python
import mysql.connector
#--------------------------------------------------------------------

#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify, render_template
from flask import request

# Instalar con pip install flask-cors
from flask_cors import CORS

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time


#Creamos una instancia de la aplicación Flask
app = Flask(__name__)
CORS(app) # Se habilita CORS para la aplicación Flask. CORS es una característica de seguridad en los navegadores que restringe cómo los recursos en una página web pueden ser solicitados desde otro dominio distinto del que sirvió la página original. Al habilitar CORS, se permite que los recursos de la aplicación web sean accesibles desde otros dominios, lo cual es necesario en muchos casos, como cuando se desarrolla una API que necesita ser consumida desde diferentes dominios.


# -------------------------------------------------------------------
# Definimos la clase Catalogo
# -------------------------------------------------------------------

class Catalogo:
          
    def __init__(self, host, user, password, database):
    
        #Establecemos una conexión sin especificar la base de datos.
        #self.conn es un atributo de la clase que representa una conexión activa a una base de datos.
        self.conn = mysql.connector.connect(
            host = host,
            user = user,
            password = password
        )

        # Un cursor permite interactuar con la base de datos de forma más directa para ejecutar comandos SQL.
        self.cursor = self.conn.cursor()        

        # Intentamos seleccionar la base de datos        
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
                self.conn.database = database
            else:
                raise err
            
        
        # Creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS vehiculos (
            codigo INT AUTO_INCREMENT PRIMARY KEY,
            modelo VARCHAR(255) NOT NULL,
            cantidad INT(4) NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            color VARCHAR(255) NOT NULL,
            puertas INT(3),                
            imagen_url VARCHAR(255))''')
        # Guardamos los cambios en la base de datos.
        self.conn.commit()

        
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
        # self.conn.cursor(dictionary=True) devuelve cada fila como un diccionario. Cada fila se representa como un diccionario, donde las claves son los nombres de las columnas y los valores son los datos correspondientes. Esto facilita el acceso a los datos sin tener que recordar el orden de las columnas.


    # -------------------------------------------------------------------
    # Método para agregar vehículos al arreglo
    # -------------------------------------------------------------------
    def agregar_vehiculo(self, modelo, cantidad, precio, color, puertas, imagen_url): 
       
        sql = "INSERT INTO vehiculos (modelo, cantidad, precio, color, puertas, imagen_url) VALUES (%s, %s, %s, %s, %s, %s)"

        valores = (modelo, cantidad, precio, color, puertas, imagen_url)
        #Ejecuta la sentencia
        self.cursor.execute(sql, valores)
        #La guarda
        self.conn.commit() #Guardo
        #proporciona el valor de la clave primaria generada automáticamente por la base de datos para la fila recién insertada.
        return self.cursor.lastrowid
          
    # -------------------------------------------------------------------
    # Método para consultar un vehículo a partir de su código
    # -------------------------------------------------------------------
    def consultar_vehiculo(self, codigo):
        #Consultamos un vehiculo a partir de su código
        self.cursor.execute(f"SELECT * FROM vehiculos WHERE codigo = {codigo}")
        return self.cursor.fetchone() #fetchone devuelve un sólo registro

    # -------------------------------------------------------------------
    # Método para modificar los datos de un vehículo a partir de su código
    # -------------------------------------------------------------------
    def modificar_vehiculo(self, codigo, nuevo_modelo, nueva_cantidad, nuevo_precio, nuevo_color, nuevas_puertas, nueva_imagen):

        sql = "UPDATE vehiculos SET modelo = %s, cantidad = %s, precio = %s, color = %s, puertas = %s, imagen_url = %s  WHERE codigo = %s"

        valores = (nuevo_modelo, nueva_cantidad, nuevo_precio, nuevo_color, nuevas_puertas, nueva_imagen, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit() 
        return self.cursor.rowcount > 0
        #rowCount() se utiliza para comprobar si una operación SQL ha afectado a alguna fila en la base de datos. Es una comparación que verifica si este número es mayor que cero, indica que al menos una fila fue afectada.
        
    # -------------------------------------------------------------------
    # Método para obtener un listado de los vehiculos en pantalla
    # -------------------------------------------------------------------
    def listar_vehiculos(self):
       self.cursor.execute("SELECT * FROM vehiculos")
       vehiculos = self.cursor.fetchall() #devuelve todas las filas en una consulta SQL
       return vehiculos

    # -------------------------------------------------------------------
    # Método para eliminar un vehículo a partir de su código
    # -------------------------------------------------------------------
    def eliminar_vehiculo(self, codigo):
        self.cursor.execute(f"DELETE FROM vehiculos WHERE codigo = {codigo}")
        self.conn.commit() #Guardar
        return self.cursor.rowcount > 0
        #rowCount() se utiliza para comprobar si una operación SQL ha afectado a alguna fila en la base de datos. Es una comparación que verifica si este número es mayor que cero, indica que al menos una fila fue afectada.


# -------------------------------------------------------------------
# Cuerpo del programa
# -------------------------------------------------------------------
# catalogo = Catalogo(host='localhost', user='root', password='root', database='proyecto_Chevrolet_crud')
catalogo = Catalogo(host='constanza06.mysql.pythonanywhere-services.com', user='constanza06', password='puchitril', database='constanza06$proyecto_Chevrolet_crud')


# Carpeta para guardar las imagenes.
# RUTA_DESTINO = './static/imagenes/'

RUTA_DESTINO = '/home/constanza06/mysite/static/imagenes'


#--------------------------------------------------------------------
# Listar todos los vehiculos
#--------------------------------------------------------------------
@app.route("/vehiculos", methods=["GET"]) 
def listar_vehiculos():
    vehiculos = catalogo.listar_vehiculos()
    return jsonify(vehiculos)


#--------------------------------------------------------------------
# Mostrar un sólo vehiculo según su código
#--------------------------------------------------------------------
@app.route("/vehiculos/<int:codigo>", methods=["GET"]) 
def mostrar_vehiculo(codigo):
    vehiculo = catalogo.consultar_vehiculo(codigo)
    if vehiculo:
        return jsonify(vehiculo), 201
    else:
        return "Vehiculo no encontrado.", 404


#--------------------------------------------------------------------
# Agregar un vehiculo
#--------------------------------------------------------------------
@app.route("/vehiculos", methods=["POST"])
#La ruta Flask `/vehiculos` con el método HTTP POST está diseñada para permitir la adición de un nuevo vehiculo a la base de datos.
#La función agregar_vehiculo se asocia con esta URL y es llamada cuando se hace una solicitud POST a /vehiculos.
def agregar_vehiculo():
    #Recojo los datos del form
    modelo = request.form['modelo']
    cantidad = request.form['cantidad']
    precio = request.form['precio']
    color = request.form['color']
    puertas = request.form['puertas']
    imagen = request.files['imagen'] 
    nombre_imagen=""

    # Genero el nombre de la imagen
    nombre_imagen = secure_filename(imagen.filename)
    nombre_base, extension = os.path.splitext(nombre_imagen)
    #Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" 

    # # Verifica que el directorio de destino exista, y si no, lo crea
    if not os.path.exists(RUTA_DESTINO):
        os.makedirs(RUTA_DESTINO)

    nuevo_codigo = catalogo.agregar_vehiculo(modelo, cantidad, precio, color, puertas, nombre_imagen)
    if nuevo_codigo:
        # Guarda la imagen en el directorio de destino
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))

        # Si el vehiculo se agrega con éxito, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 201 (Creado)
        return jsonify({"mensaje": "Vehiculo agregado correctamente.", "codigo": nuevo_codigo, "imagen": nombre_imagen}), 201
    else:
        # Si el vehiculo no se puede agregar, se devuelve una respuesta JSON con un mensaje de error y un código de estado HTTP 500 (Internal Server Error)
        return jsonify({"mensaje": "Error al agregar el vehiculo."}), 500

#--------------------------------------------------------------------
# Modificar un vehiculo según su código
#--------------------------------------------------------------------
@app.route("/vehiculos/<int:codigo>", methods=["PUT"])
#La ruta Flask /vehiculos/<int:codigo> con el método HTTP PUT está diseñada para actualizar la información de un vehiculo existente en la base de datos, identificado por su código.
#La función modificar_vehiculo se asocia con esta URL y es invocada cuando se realiza una solicitud PUT a /vehiculos/ seguido de un número (el código del vehiculo).
def modificar_vehiculo(codigo):
    #Se recuperan los nuevos datos del formulario
    nuevo_modelo = request.form.get("modelo")
    nueva_cantidad = request.form.get("cantidad")
    nuevo_precio = request.form.get("precio")
    nuevo_color = request.form.get("color")
    nuevas_puertas = request.form.get("puertas")
    
    
    # Verifica si se proporcionó una nueva imagen
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        # Procesamiento de la imagen
        nombre_imagen = secure_filename(imagen.filename) 
        nombre_base, extension = os.path.splitext(nombre_imagen) 
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" #Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.

        # Guardar la imagen en el servidor
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))
        
        # Busco el vehiculo guardado
        vehiculo = catalogo.consultar_vehiculo(codigo)
        if vehiculo: # Si existe el vehiculo...
            imagen_vieja = vehiculo["imagen_url"]
            # Armo la ruta a la imagen
            ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

            # Y si existe la borro.
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
    
    else:
        # Si no se proporciona una nueva imagen, simplemente usa la imagen existente del vehiculo
        vehiculo = catalogo.consultar_vehiculo(codigo)
        if vehiculo:
            nombre_imagen = vehiculo["imagen_url"]

    # Se llama al método modificar_vehiculo pasando el codigo del vehiculo y los nuevos datos.
    if catalogo.modificar_vehiculo(codigo, nuevo_modelo, nueva_cantidad, nuevo_precio, nuevo_color, nuevas_puertas , nombre_imagen):
        
        #Si la actualización es exitosa, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
        return jsonify({"mensaje": "Vehículo modificado"}), 200
    else:
        #Si el vehiculo no se encuentra, se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado).
        return jsonify({"mensaje": "Vehículo no encontrado"}), 403

#--------------------------------------------------------------------
# Eliminar un vehículo según su código
#--------------------------------------------------------------------
@app.route("/vehiculos/<int:codigo>", methods=["DELETE"])
#La ruta Flask /vehiculos/<int:codigo> con el método HTTP DELETE está diseñada para eliminar un vehiculo específico de la base de datos, utilizando su código como identificador.
#La función eliminar_vehiculo se asocia con esta URL y es llamada cuando se realiza una solicitud DELETE a /vehiculos/ seguido de un número (el código del vehiculo).
def eliminar_vehiculo(codigo):
    # Busco el vehiculo en la base de datos
    vehiculo = catalogo.consultar_vehiculo(codigo)
    if vehiculo: # Si el vehiculo existe, verifica si hay una imagen asociada en el servidor.
        imagen_vieja = vehiculo["imagen_url"]
        # Armo la ruta a la imagen
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

        # Y si existe, la elimina del sistema de archivos.
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

        # Luego, elimina el vehiculo del catálogo
        if catalogo.eliminar_vehiculo(codigo):
            #Si el vehiculo se elimina correctamente, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
            return jsonify({"mensaje": "Vehiculo eliminado"}), 200
        else:
            #Si ocurre un error durante la eliminación se devuelve un mensaje de error con un código de estado HTTP 500 (Error Interno del Servidor).
            return jsonify({"mensaje": "Error al eliminar el vehiculo"}), 500
    else:
        #Si el vehiculo no se encuentra se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado). 
        return jsonify({"mensaje": "Vehiculo no encontrado"}), 404




#------------------------ FLASK ------------------------
if __name__ == "__main__":
    app.run(debug=True)