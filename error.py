import sys

class SalidaException(Exception):
    def __init__(self,mensaje):
        super(SalidaException, self).__init__(mensaje)
def error(instruccion,customMessage=""):
    mensaje = "Error, intrucción no valida"
    if customMessage:
        mensaje = customMessage
    mensaje+="\n"+str(instruccion)
    raise SalidaException(mensaje)
