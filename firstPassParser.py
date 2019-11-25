import treeGen
import string
import sys
from pprint import pprint
from copy import copy
from error import error
import sumhex

def hextoInt(cadena):
    return int(cadena,16)
def normalizeJR(etiqueta,actual):
    if etiqueta>actual:
        resultado = etiqueta-actual
    else:
        resultado = etiqueta-actual
        resultado += 256
    return hex(resultado).upper()[2:]

DEBUG = False
class FirstPassParser():
    def __init__(self,archivoOpCode,tokenList,abstractTokenL
    ,symbolTable):
        self.file = archivoOpCode
        self.tList = tokenList
        self.abstactTList = abstractTokenL
        self.symbolTable = symbolTable#Its incomplete until first pass
        self.arbol = treeGen.run(archivoOpCode)###Gets the hash tree for search
        self.sizeList = []
        self.opCodeList = []
    
    def _firstPassPart1(self):
        cL = 0
        firstInstruction = True
        for instruccion,instructReal in zip(self.abstactTList,self.tList):
            if instructReal[0] == "ORG" and firstInstruction:
                cL = hextoInt(instructReal[1][:-1])
                self.sizeList.append(hex(cL))
            elif instructReal[0] == "ORG":
                error(instructReal,"El ORG no es la primera instrucción o se definio más de un org")
            elif len(instruccion)==1 and instruccion[0]== "NN":
                if instructReal[0] in self.symbolTable:
                    self.symbolTable[instructReal[0]][1] = hex(cL)
                    self.sizeList.append(hex(cL))
                else:
                    if DEBUG:
                        print("Error, no se encuentra definido en la tabla")
                        print("Error mortal")
                        sys.exit()
            else:
                size,opCode = self.arbol.search(instruccion)
                if size == False:
                    error(instruccion)
                try:
                    size = int(size,16)
                    self.sizeList.append(hex(cL))
                    cL+=size

                except Exception as e:
                    if not (all(c in string.hexdigits for c in size) and 
                    all(c in string.hexdigits for c in size) ) and DEBUG:
                            print("This means the developers made a mistake, it should had been\
                                evaluated before")
                            print("valor actual",size)
                            print("valor dado",cL)
                            print(self.sizeList)
                            print(e)
                            sys.exit()
            firstInstruction = False
        if DEBUG:
            for i in self.symbolTable():
                if i[2] ==None:
                    error(self.symbolTable,"Error, algunas etiquetas no tienen dirección")
    
    def _secondPass(self):###TAbla opcode no necesariamente tendrá el tamaño de las anteriores
        #por las directivas.
        def normalize(absOp,realOp):
            if absOp == "NN" and ("#"+realOp in self.symbolTable):
                dir = self.symbolTable["#"+realOp][1]
                dir = str(dir[2:])
                if 4 - len(dir) > 0:
                    dir = "0"*(4-len(dir))+dir
                return dir[2:]+dir[:2] 
            elif absOp == "NN" or absOp == "(NN)":
                c = realOp.replace("h","").replace("H","").replace("(","").replace(")","")
                if len(c)<4:
                    c = "0"*(4-len(c))+c
                return c[2:]+c[:2]
            elif absOp == "N":
                return realOp.replace("h","").replace("H","")    
            else: return "" ##Se asume es un registro o una bandera.           
        for cont,instrucciones in enumerate(zip(self.tList,self.abstactTList)):
            realInst,absInst = instrucciones
            opCode=""
            op1 = ""
            op2 = ""
            if len(absInst)==1 and realInst[0][0]== "#":
                pass
            else:
                size,opCode = self.arbol.search(absInst)
                if opCode == -1 and DEBUG:
                    error(realInst)
                else:
                    if opCode == "-":
                        if absInst[0] == "DB":
                            opCode = normalize(absInst[1],realInst[1])
                        else:
                            opCode = " "
                    else:
                        ##operand1
                        if len(absInst) == 1:
                            pass
                        else:
                            if absInst[1] == "-":
                                pass
                            else:
                                if absInst[1]=="NN":#solo las etiquetas usan NN
                                    if "#"+realInst[1] in self.symbolTable:
                                        if realInst[0] == "JR":
                                            if cont+1 < len(self.sizeList):
                                                actual = hextoInt(self.sizeList[cont+1])
                                                etiqueta = hextoInt(self.symbolTable["#"+realInst[1]][1])
                                                op1 = normalizeJR(etiqueta,actual)
                                            else:
                                                actual = hextoInt(self.sizeList[-1])+hextoInt(size)
                                                etiqueta = hextoInt(self.symbolTable["#"+realInst[1]][1])
                                                op1 = normalizeJR(etiqueta,actual)
                                        else:
                                            op1 = normalize("NN",realInst[1])
                                    else:
                                        op1 = normalize("NN",realInst[1])
                                else:
                                    op1 = normalize(absInst[1],realInst[1])
                                if len(absInst) == 2:
                                    pass
                                else:
                                    if absInst[2] == "-":
                                        pass
                                    elif absInst[2]=="NN":
                                        if "#"+realInst[2] in self.symbolTable:
                                            if realInst[0] == "JR":
                                                if cont+1 < len(self.sizeList):
                                                    actual = hextoInt(self.sizeList[cont+1])
                                                    etiqueta = hextoInt(self.symbolTable["#"+realInst[2]][1])
                                                    op2 = normalizeJR(etiqueta,actual)
                                                else:
                                                    actual = hextoInt(self.sizeList[-1])+hextoInt(size)
                                                    etiqueta = hextoInt(self.symbolTable["#"+realInst[2]][1])
                                                    op2 = normalizeJR(etiqueta,actual)
                                            else:
                                                op1 = normalize("NN",self.symbolTable[realInst[2]])
                                        else:
                                            op1 = normalize("NN",realInst[2])
                                    else:op2 = normalize(absInst[2],realInst[2])
            opCode+=op1.upper()
            opCode+=op2.upper()
            self.opCodeList.append(opCode)
            
def run(archivo,TL,ATL,ST):
    fparser = FirstPassParser(archivo,TL,ATL,ST)
    fparser._firstPassPart1()
    fparser._secondPass()
    
    Tabla =  ""
    def dirST(realOp):
        dir = realOp[1]
        dir = str(dir[2:])
        if 4 - len(dir) > 0:
            dir = "0"*(4-len(dir))+dir
        return dir
    for i in ST.keys():
        Tabla+="\n"+str(i)+"\t"+str(dirST(ST[i]))
    
    
    codigoObjeto=  sumhex.toHEX(fparser.sizeList, fparser.opCodeList) #### DEVUELVE LA CONVERSIÓN DE LA LISTA DE OPCODE Y LA PRIMERA LOCALIDAD DE MEMORIA PARA EL FORMATO .HEX

    return fparser.sizeList,fparser.tList,fparser.opCodeList,Tabla,codigoObjeto

if __name__ == "__main__":
    archivo = "z80_table.txt"
    TL = [
            ["LD","A","0200H"],["LD","D","A"],["LD","C","08"],
            ["#eti1"],["DEC","C"],["RLCA"],["JP","NC","eti1"]
            ,["HALT"]                
        ]
    ATL = [
        ["LD","A","(NN)"],["LD","D","A"],["LD","C","N"],
            ["#eti1"],["DEC","C"],["RLCA"],["JP","NC","NN"]
            ,["HALT"]
        ]
    ST = {"eti1":[True,None]}
    fparser = FirstPassParser(archivo,TL,ATL,ST)
    fparser._firstPassPart1()
    fparser._secondPass()
    pprint(tuple(zip(fparser.sizeList,fparser.tList,fparser.opCodeList)))
    print("#####################Tabla de simbolos")
    pprint(ST)

