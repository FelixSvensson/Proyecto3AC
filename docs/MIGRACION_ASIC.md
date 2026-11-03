# Registro de migración y evidencia

La fuente FPGA se conserva en rtl/. El proyecto original no fue modificado.
Los archivos equivalentes ASIC se generan o implementan en asic/rtl/.

| Construcción original | Explicación y cambio | Validación real |
|---|---|---|
| rtl/pochoco_soc.v: por_cnt inicializado | El estado inicial de FF no está garantizado al alimentar un ASIC. Se elimina el POR y se conecta rst_ni externo en pochoco_soc_asic.v y asic_top.v. | Juego arranca tras reset, se reinicia por botón 4 y vuelve a arrancar tras otro reset externo. |
| rtl/pochoco_ram.v: initial y $readmemh | El archivo puede servir como dato de elaboración, pero no representa una carga eléctrica en una RAM ASIC. A usa ROM combinacional; B restaura cada palabra mediante reset sintetizable. | Todas las 107 palabras verificadas después de reset; B restaura una instrucción modificada. |
| rtl/espino_core/espino_register_file.v: SB_RAM40_4K | Primitiva iCE40 inexistente en GF180. Se sustituye por 15 registros FF de 32 bits y dos salidas registradas, con lectura anterior a la escritura y x0 constante. | Juego RTL y netlist de celdas estándar producen las mismas trazas. |
| Lecturas de memoria síncronas | Sustituirlas por una conexión ROM combinacional directa rompería el protocolo del Espino. Se conserva el registro de salida en A; B también lee en flanco. | Pruebas de memoria y comparación de ciclos de ambas estrategias. |
| Contador de ciclos | Se extrae cycle_counter sin cambiar incremento ni reset, para medir área y ubicar instancias. led_cycle_q continúa en el periférico. | Trazas del juego idénticas antes y después; prueba original del periférico. |

No se ejecutó una corrida LibreLane del RTL FPGA original: los motivos anteriores
proceden de la inspección directa del código y del contrato de las primitivas.
La elaboración ASIC y la síntesis reales se registran en las corridas de
results/runs/.

La primera corrida ASIC reportó 14 advertencias de lint, todas sobre señales,
bits o parámetros no usados: registro illegal_insn no expuesto, bits de dirección
alineados, bits altos de escrituras de periféricos, códigos de desplazamientos
deshabilitados y campos no utilizados. Log original con archivo y línea:
results/runs/A_gf180_p100_u40/evidence/01-verilator-lint/verilator-lint.log.
Se permite continuar después de esas advertencias mediante
ERROR_ON_LINTER_WARNINGS=false. No se deshabilitaron DRC, LVS, antena ni timing.

Primer intento de PDK: el lanzador no pasó --pdk; LibreLane intentó obtener
el PDK predeterminado y luego no encontró GF180MCU D. Evidencia:
results/environment/first_flow.log. Corrección: scripts/run_flow.sh pasa
--pdk gf180mcuD explícitamente, además del PDK en la configuración.

La primera prueba del testbench de memoria B falló por una referencia ROM
desconocida en tiempo cero, no por contenido incorrecto: actual=800000b7,
expected=xxxxxxxx. Se hizo transicionar la dirección del modelo de referencia
y se añadieron comprobaciones explícitas de valores X. Las pruebas posteriores
de ambas memorias pasan. La prueba funcional del netlist requiere retirar
únicamente bloques specify del modelo de celdas porque Icarus no admite ciertas
rutas ifnone; no se anotan retardos ni se usa esta simulación para signoff STA.

Las corridas v1 usan aplanamiento temprano. Las v2 extraen el contador y usan
deferred_flatten para preservar la procedencia de las celdas. No deben combinarse
sus números como si fueran la misma implementación. Los ZIP y hashes de
results/snapshots/ guardan las fuentes y programas efectivos.
