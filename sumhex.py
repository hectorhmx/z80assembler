def toHexComplement2(val, nbits):
    complemento=~val
    return hex(((complemento + (1 << nbits)) % (1 << nbits))+1)

def sumaRenglon(opcode):
    #opcode = ':102000003A0021FE00CA2120CD10207B32012176'
    n = 2
    op_split = [opcode[i:i+n] for i in range (1, len(opcode), n)] #Obtengo los bytes de opcode en un arreglo, voy de 2 en 2
    #print(op_split)
    hexint_split = [int(x, 16) for x in op_split] #Convierte los elementos hexadecimales para que los pueda sumar
    #print(hexint_split)
    hexsum = 0
    for i in range (len(hexint_split)):
        hexsum += hexint_split[i] #Suma de enteros
        #hexsum.append(hex(hexint_split[i] + hexint_split[i+1])[2:].upper())
    resultado=toHexComplement2(hexsum, 8)
    return resultado[len(resultado)-2:].upper()

def sumalocalidades(loc, inc):
    return cleanHex(hex(int(loc, 16) + inc))
    
def cleanHex(hexnum):
    salida = hexnum[2:]
    number = 4-len(salida)
    salida  = ("0"*number)+salida
    return salida.upper()

def toHEX(sizeList, opCodeList):
#if __name__ == "__main__":
    #opCodeList = ['3A0021', 'FE00', 'CA2120', 'CD1020', '7B32', '01', '21', '76','05', '3A0021', 'FE00', 'CA2120', 'CD1020', '7B32', '01', '21', '76','05''21', '76','05','21', '76','05','21', '76','05','21', '76','05','21','22']
    inc = 0
    localidadInicial = sizeList[0]

    
    cadena = "".join(opCodeList)
    cadena = cadena.strip(" ")
    tam = len(cadena)
    lista = []
    for i in range(tam//32):
        cadenaAnterior = cadena[:32]
        cadenaRenglon=':'
        cadenaRenglon+=hex(len(cadenaAnterior)//2)[2:]+ sumalocalidades(localidadInicial, inc)+'00'+cadenaAnterior
        cadenaRenglon+=sumaRenglon(cadenaRenglon)
        lista.append(cadenaRenglon)
        cadena = cadena[32:]
        inc += 16
        if len(cadena) == 0:
            lista.append(':00000001FF')
        elif len(cadena) < 32 and len(cadena) != 0:
            cadenaRenglon=':'
            cadenaRenglon+='0'+hex(len(cadena)//2)[2:].upper()+sumalocalidades(localidadInicial, inc)+'00'+cadena
            cadenaRenglon+=sumaRenglon(cadenaRenglon)
            lista.append(cadenaRenglon)
            lista.append(':00000001FF')
    #return lista
    return lista
    
        
