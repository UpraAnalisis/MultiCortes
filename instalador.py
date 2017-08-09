#-*- coding: utf-8 -*-
import arcpy
import os,xlwt,xlrd
from xlrd import open_workbook
import arcgisscripting as script_tools
import subprocess
import exceptions
import locale
import shutil
import inspect
import sys
import exceptions
locale.setlocale(locale.LC_ALL,  'C')

#=========Funciones Auxiliares=====================#
def getPythonPath():
    pydir = sys.exec_prefix
    pyexe = os.path.join(pydir, "python.exe")
    if os.path.exists(pyexe):
        return pyexe
    else:
        raise RuntimeError("python.exe no se encuentra instalado en {0}".format(pydir))

def directorioyArchivo ():
    archivo=inspect.getfile(inspect.currentframe()) # script filename
    directorio=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
    return archivo, directorio

# ------------------------------------------------------------

#=========Validación de requerimientos=====================#

pyexe = getPythonPath()

if not "x64" in r"%s"%(pyexe):
    pyexe=pyexe.replace("ArcGIS","ArcGISx64")
if not arcpy.Exists(pyexe):
    arcpy.AddError("Usted no tiene instalado el Geoprocesamiento en segundo plano (64 bits)")
    raise RuntimeError("Usted no tiene instalado el Geoprocesamiento en segundo plano (64 bits) {0}".format(pyexe))
else:
    verPython64=pyexe
    verPythonfinal=verPython64
# ------------------------------------------------------------

verPython32=verPython64.replace("x64","")
ArcVersion=verPython32.replace("C:\Python27\ArcGIS","")
verPythonDir=verPython64.replace("\\python.exe","")
verPythonDir_32 =verPythonDir.replace("x64","")
archivo, directorio = directorioyArchivo()
directorio_raiz = directorio.replace("\Install","")




try:
    print "instalando librerias"
    try:
        import pip
    except:
        os.system(r"%s %s\get-pip.py")%(verPython32,directorio_raiz)
        os.system(r"%s %s\get-pip.py")%(verPython64,directorio_raiz)
        import pip

    print "pip instalado"

    try:
        import xlsxwriter
    except:
        pip.main(["install","xlsxwriter"])
        import xlsxwriter

    print "xlsxwriter instalado"

    try:
        import easygui
        srcfile = r"%s\fillable_box.py"%(directorio_raiz)
        dstdir = r"%s\Lib\\site-packages\easygui\boxes\fillable_box.py"%(verPythonDir_32)
        shutil.copy(srcfile, dstdir)
    except:
        pip.main(["install","easygui"])
        srcfile = r"%s\fillable_box.py"%(directorio_raiz)
        dstdir = r"%s\Lib\site-packages\easygui\boxes\fillable_box.py"%(verPythonDir_32)
        shutil.copy(srcfile, dstdir)
        import easygui

    print "easygui instalado"

    try:
        import xlutils
        from xlutils.copy import copy
    except:
        pip.main(["install","xlutils"])
        import xlutils
        from xlutils.copy import copy

    print "xlutils instalado"

    print "Proceso de instalacion finalizado correctamente..."
    os.system("PAUSE")

except exceptions.Exception as e:
    print e.__class__, e.__doc__, e.message
    os.system("pause")