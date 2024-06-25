import json
from CONEX.Conex import conexion
from flask import Response

conex = conexion()

ruta = 'static/json/pdf.json'

def prepararExportDataJson():
    try:
        cur = conex.cursor()
        data = []
        listData = []
        dataDict = {}
        cur.execute('select nombre, fecha, tipo, descripcion from solicitudes')
        result = cur.fetchall()
        for data1 in result:
            dato = (data1[0], data1[1], data1[2], data1[3])
            listData.append(dato)
        
        for data2 in listData:
            data.append({'cliente': data2[0],'fecha':data2[1],'tipo':data2[2],'problema':data2[3]})
        dataDict = data
        exportarDataJson(ruta, dataDict)
    except Exception as ex:
        print(ex)

def exportarDataJson(archivo, diccionario):
    resultData = {}
    try:
        out_file = open(archivo, 'w', encoding='utf-8')
        json.dump(diccionario, out_file, indent=4)
        out_file.close()
        resultData['Mesagge'] = 'Datos exportados excitosamente'
    except Exception as ex:
        resultData['Error'] = ex


def buscarBoleta(email):
    sql = 'SELECT folioBoleta FROM masterbikes.usuarios WHERE email = %s'
    cur = conex.cursor()
    cur.execute(sql,(email,))
    boleta = cur.fetchone()
    cur.close()
    return boleta

def ofertaCliente():
    sql = 'SELECT email FROM usuarios'
    cur = conex.cursor()
    cur.execute(sql)
    resultado = cur.fetchall()

    return resultado

def buscarElementoFolio(folioBoleta):
    sql = 'SELECT folioBoleta, fechaBoleta, productos FROM boleta WHERE folioBoleta = %s'
    cur = conex.cursor()
    cur.execute(sql,(folioBoleta,))
    boleta = cur.fetchone()
    cur.close()
    return boleta


def agregarProductos(PLU, nombre, descripcion, precio, stock, img):
    sql = "INSERT INTO productos (PLU, Nombre, Descripcion, Precio, Stock, images) VALUES (%s, %s, %s, %s, %s, %s)"
    cur = conex.cursor()
    cur.execute(sql, (PLU, nombre, descripcion, precio, stock, img))
    conex.commit()
    cur.close()

def buscarIMG():
    id = 1
    cur = conex.cursor()
    cur.execute('SELECT images from productos WHERE ID = %s',(id,))
    imagen = cur.fetchone()
    cur.close()
    if imagen:
        return Response(imagen[0],mimetype='image/png')
    else:
        return 'imagen no encontrada', 404

def VerifiedIMG(nombreIMG):
    extencionesPermitidas = {'png','jpg', 'webp'}
    return '.' in nombreIMG and nombreIMG.rsplit('.', 1)[1].lower() in extencionesPermitidas



def VerifiedPDF(nombreArchivo):
    return '.' in nombreArchivo and nombreArchivo.rsplit('.', 1)[1].lower() == 'pdf'