import firstPassParser
import lexer
from pprint import pprint
import sys
import string
from error import error,SalidaException

def intToHex(entero):
    salida = hex(entero)
    salida = salida[2:]
    return salida
def cleanHex(hexnum):
    salida = hexnum[2:]
    number = 4-len(salida)
    salida  = ("0"*number)+salida
    return salida.upper()




def toLST(sizeList,opCodeList,tokenList,tabla):
    strings = []
    pre = None
    cont = -1
    for x,y,z in zip(sizeList,opCodeList,tokenList):
        cont+=1
        if z[0][0] == "#":
            pre = z[0][1:]+": "
        elif z[0][0] != "#":
            if len(z) == 3:
                z[1] += "," + z[2]
                del(z[2])
            if pre != None:
                z[0] = pre+z[0]
                pre = None
            if z[0] == "END" and cont == len(sizeList)-1:
                x="0000"
            elif z[0] == "END":
                error([x,y,],"El end no es la ultima instrucción del programa")
            elif cont==len(sizeList)-1:
                strings.append(' {:4s} {:6s}    {:25s}'.format(cleanHex(x),y," ".join(z)))
                strings.append(' {:4s} {:6s}    {:25s}'.format("0000","","END"))
                break
                

            strings.append(' {:4s} {:6s}    {:25s}'.format(cleanHex(x),y," ".join(z)))
    strings.append("\n")
    tabla = tabla.upper().replace("#","")
    strings.append(tabla)
    return strings
        
def validateInput(inputString):
    valid = set(string.ascii_letters)
    valid.add(".")
    valid |= set(map(str,range(10)))
    for i in inputString:
        if i not in valid:
            error(inputString,"Caracter invalido en nombre archivo:"+"'{}'".format(i))



if __name__ == "__main__":
    tableFile = "z80Table.txt"
    if len(sys.argv)==1:
        source = "entrada.asm"
    else:
        source = sys.argv[1]
    ###Validamos las rutas
    try:
        validateInput(source)
        validateInput(tableFile)

        with open(source) as entrada:
            ListaInstrucciones = entrada.readlines()
        ListaInstrucciones = [x.strip("\n") for x in ListaInstrucciones]
        ###Leeer iun archivo, generar lista de instrucciones
        
        ####Codigos, metodo run.
        tokenList,abstractTokenList,simTable=lexer.run(ListaInstrucciones)
        sizeList,tList,opCodeList,Tabla,codigoObjeto=firstPassParser.run(tableFile,tokenList,abstractTokenList,simTable)##Este hace los prints
        strings = toLST(sizeList,opCodeList,tokenList,Tabla)
        for i in strings:
            print(i)
        for i in codigoObjeto:
            print(i)
    except SalidaException as se:
        print(se)
