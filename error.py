import sys
def error(instruccion,customMessage=""):
    mensaje = "Error, intrucción no valida"
    if customMessage:
        mensaje = customMessage
    print(mensaje)
    print(instruccion)
    sys.exit()