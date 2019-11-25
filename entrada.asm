ORG 2000H
LD A,(2100H); Obtencion del valor a calcular para el factorial
CP 00H; Se compara si es 0 porque de esa manera ya se sabe el resultado, es decir 1
JR Z, etiB; Si resulta verdadero, se salta a la etiB
CALL FACTORIAL
LD A, E; Almacenamiento en el acumlador el valor del factorial
etiA: LD (2101H), A; Definicion de etiA, se guarda en la direccion especificada el valor del factorial
HALT
FACTORIAL: CP 00H; Se compara si es 0 porque, de esa manera, se llega al caso base
JR Z, NULLO; Si resulta que es 0, se va a la etiqueta NULLO
DEC A;Se quiere obtener n-1 hasta llegar al caso base
CALL FACTORIAL
INC A; De igual manera, se desea conseguir ahora el n+1
LD C, A; Se carga en C el valor de n+1
CALL MULTIPLY; se realiza la multiplicacion vista en clase
LD E, A; El resultado del factorial se almacena
LD A, C; se obtiene el valor n
RET
etiB: LD A, 01H; se carga en el acumulador un 1 en caso de que se quiera obtener el factorial de 1
JR etiA; salto al final del programa
MULTIPLY: LD B, A; se guarda temporalmente el valor del acumulador para que este pueda utilizarse para operaciones, es el primer operador
LD D, E; es el segundo operdor
LD A, 00H
etiC: ADD A, D; multiplicacion definida para ensamblador
DEC B; decremento definido para el contador
JR NZ, etiC; de esta manera se repite el ciclo
RET
NULLO: LD E, 01H; se ha llegado al caso base, se almacena el valor de 1
RET
END
NELPERRO