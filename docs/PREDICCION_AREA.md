# Predicción previa a síntesis

Escrita antes de obtener áreas. Se espera que la memoria unificada B domine por
sus palabras programables de 32 bits y multiplexores de lectura. La ROM de A
puede simplificarse como lógica constante; el banco RV32E tiene 15 registros de
32 bits y dos puertos de lectura síncrona, por lo que se espera que sea uno de
los mayores bloques de A. La ALU contiene sumador, restador, comparadores y
lógica booleana; no implementa desplazamientos. El contador de ciclos tiene
32 FF y lógica de incremento, además de un registro independiente de captura
del instante LED. Su área debe medirse por separado, sin atribuirle toda el área
del periférico. No se predicen cifras numéricas antes de medir.
