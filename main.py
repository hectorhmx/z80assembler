import firstPassParser
import lexer
from pprint import pprint
import sys
import string
from error import error

def hextoInt(cadena):
    return int(cadena,16)
def intToHex(entero):
    salida = hex(entero)
    salida = salida[2:]
    return salida
def cleanHex(hexnum):
    salida = hexnum[2:]
    number = 4-len(salida)
    salida  = ("0"*number)+salida
    return salida.upper()



def archivoHex(sizeList,opCodeList):
    cadena = "".join(opCodeList)
    cadena = cadena.strip(" ")
    tam = len(cadena)
    lista = []
    for i in range(tam//32):
        cadenaAnterior = cadena[:32]
        lista.append(cadenaAnterior)
        cadena = cadena[32:]
    print("")
    for i in lista:
        print(i)
    print(cadena)

def toLST(sizeList,opCodeList,tokenList):
    strings = []
    pre = None
    for x,y,z in zip(sizeList,opCodeList,tokenList):
        if z[0][0] == "#":
            pre = z[0][1:]+": "
        elif z[0][0] != "#":
            if len(z) == 3:
                z[1] += "," + z[2]
                del(z[2])
            if pre != None:
                z[0] = pre+z[0]
                pre = None
            strings.append(' {:4s} {:6s}    {:25s}'.format(cleanHex(x),y," ".join(z)))

    return strings
        
def validateInput(inputString):
    valid = set(string.ascii_letters)
    valid.add(".")
    valid |= set(range(10))
    if not all(v in valid for v in inputString):
        error(inputString,"Archivo de entrada    no valido")


if __name__ == "__main__":
    tableFile = "z80Table.txt"
    if len(sys.argv)==1:
        source = "entrada.ASAM"
    else:
        source = sys.argv[1]
    ###Validamos las rutas
    validateInput(source)
    validateInput(tableFile)

    with open(source) as entrada:
        ListaInstrucciones = entrada.readlines()
    ListaInstrucciones = [x.strip("\n") for x in ListaInstrucciones]
    ###Leeer iun archivo, generar lista de instrucciones
    
    ####Codigos, metodo run.
    tokenList,abstractTokenList,simTable=lexer.run(ListaInstrucciones)
    sizeList,tList,opCodeList,Tabla=firstPassParser.run(tableFile,tokenList,abstractTokenList,simTable)##Este hace los prints
    strings = toLST(sizeList,opCodeList,tokenList)
    for i in strings:
        print(i)
    archivoHex(sizeList,opCodeList)