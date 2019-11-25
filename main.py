import firstPassParser
import lexer
from pprint import pprint
import sys
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

    
        
        
        


if __name__ == "__main__":
    archivo = "z80_table.txt"
    if len(sys.argv)==1:
        lol = "entrada.ASAM"
    else:
        lol = sys.argv[1]
    ###Lo importante es la ruta


    with open(lol) as entrada:
        ListaInstrucciones = entrada.readlines()
    ListaInstrucciones = [x.strip("\n") for x in ListaInstrucciones]
    ###Leeer iun archivo, generar lista de instrucciones
    
    ####Codigos, metodo run.
    tokenList,abstractTokenList,simTable=lexer.run(ListaInstrucciones)
    sizeList,tList,opCodeList,Tabla=firstPassParser.run(archivo,tokenList,abstractTokenList,simTable)##Este hace los prints

    strings = []
    pre = None
    for x,y,z in zip(sizeList,opCodeList,tokenList):
        if z[0][0] == "#":
            pre = z[0][1:]
            print(pre)
        if z[0][0] != "#":
            if len(z) == 3:
                z[1]+=","+z[2]
                del(z[2])
            strings.append(' {:4s} {:6s}    {:25s}'.format(cleanHex(x),y," ".join(z)))
    for i in strings:
        print(i)

    archivoHex(sizeList,opCodeList)




    #