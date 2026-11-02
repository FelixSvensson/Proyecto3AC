# MISIÓN: PROYECTO 3 DE ARQUITECTURA DE COMPUTADORES — FPGA A ASIC

Actúa como un ingeniero senior de diseño digital, microarquitectura RISC-V, Verilog, verificación funcional e implementación física ASIC.

Tu misión es **desarrollar, ejecutar, verificar, documentar y dejar preparado para entregar el Proyecto 3 de Arquitectura de Computadores de la Universidad de los Andes, semestre 2026-2**.

No quiero únicamente un plan, ejemplos, configuraciones iniciales ni una demostración. Quiero que efectúes el trabajo completo sobre mi computador, incluyendo instalación de herramientas, modificación de código, simulaciones, síntesis, place and route, signoff, análisis de resultados, gráficos y documentación.

Tienes autorización para utilizar la terminal, instalar dependencias, ejecutar scripts, investigar documentación técnica y modificar los archivos del nuevo proyecto. Debes trabajar de forma autónoma y resolver problemas técnicos utilizando evidencia real.

**REGLA ABSOLUTA: NO HAGAS `git commit` NI `git push`.** Yo realizaré personalmente esas dos operaciones cuando hayas terminado.

## 1. CONTEXTO Y PUNTO DE PARTIDA

Repositorio original del Proyecto 2:

https://github.com/FelixSvensson/Proyecto2AC

Cuenta GitHub: `FelixSvensson`

Nueva entrega deseada: `FelixSvensson/Proyecto3AC`

El Proyecto 3 debe partir del repositorio entregado por el grupo en el Proyecto 2, no del proyecto base proporcionado por el profesor.

El repositorio original tiene como rama principal `main`. Existe también una rama `dev-game`, pero debes inspeccionar ambas y utilizar como fuente la versión efectivamente entregada del Proyecto 2, priorizando `main` mientras no exista evidencia contraria.

El Proyecto 2 contiene:

- Pochoco SoC, basado en Espino Core.
- Procesador RV32E, con registros x0 a x15.
- RTL en Verilog.
- `rtl/game_top.v`, `rtl/pochoco_soc.v`, `rtl/pochoco_ram.v`, `rtl/pochoco_periph.v`, `rtl/pochoco_spi_slave.v` y `rtl/espino_core/`.
- `assembler/assembler.py`, desarrollado por el grupo.
- `assembler/test_assembler.py`.
- `sw/game.s` y `sw/game.hex`.
- `sim/pochoco_periph_tb.v`.
- Un Makefile de generación, pruebas y síntesis.
- Un juego de reflejos que ya funcionaba en la Nandland Go Board.

El juego genera aproximadamente 107 instrucciones en la versión del Proyecto 2; verifica nuevamente la cantidad desde el programa real.

Su funcionamiento incluye una espera de tres segundos, selección de uno de cuatro LEDs, medición exacta del tiempo de reacción mediante contador de ciclos, detección de pulsaciones correctas e incorrectas, presentación de tiempos en décimas y promedio de diez rondas correctas.

La memoria del diseño original emplea `$readmemh`, el SoC incorpora un contador de ciclos de 32 bits y guarda el instante de la escritura a LEDs.

El RTL de la versión FPGA contiene un reset de encendido generado con un contador inicializado. Esto requiere atención especial al pasar a ASIC.

**No destruyas, sobrescribas ni modifiques el repositorio original del Proyecto 2.**

Crea una copia de trabajo independiente para el Proyecto 3, conservando la procedencia e historial de Git cuando corresponda.

## 2. ENUNCIADO OFICIAL Y PLAZO

Documento: `Proyecto_3_arquitectura.pdf`.

Si el documento está disponible en el entorno, léelo íntegramente y úsalo como fuente de autoridad. También te proporciono todos sus requisitos principales a continuación para que puedas trabajar aunque no tengas acceso al adjunto.

Fecha límite de entrega en GitHub y defensa presencial: **4 de noviembre de 2026, 10:30 AM, horario de Chile.**

Objetivo: transformar el Pochoco SoC con el juego del Proyecto 2 desde RTL hasta un GDSII mediante LibreLane y GF180MCU.

El producto es un macro digital de celdas estándar, no un chip encapsulado. Los puertos son terminales lógicos y no pads físicos de entrada/salida.

Parámetros obligatorios de la corrida final:

- `CLOCK_PERIOD = 100` ns.
- `FP_CORE_UTIL = 40` %.
- PDK: GF180MCU.
- Flujo: LibreLane.
- DRC limpio.
- LVS limpio.
- Violaciones de antena corregidas o justificadas.
- Setup y hold: WNS ≥ 0 y TNS = 0, en todos los corners exigidos.

Debes conservar evidencia verificable y reproducibilidad de todas las decisiones.

## 3. PREPARAR EL ENTORNO DE DESARROLLO

Primero inspecciona el sistema operativo, capacidad de almacenamiento, RAM, CPU, herramientas instaladas, Git y autenticación de GitHub.

Si estás trabajando en mi Lenovo con Windows 11, considera WSL2 con Ubuntu y una instalación soportada de LibreLane mediante Docker o el método recomendado por su documentación actual.

Si estás en macOS u otro entorno, elige una instalación realmente compatible con esa versión del sistema operativo.

Documentación oficial:

- https://librelane.readthedocs.io/en/stable/
- https://gf180mcu-pdk.readthedocs.io/en/latest/
- https://openroad.readthedocs.io/en/latest/

Instala o configura las herramientas necesarias:

- LibreLane.
- GF180MCU y bibliotecas estándar compatibles.
- Yosys.
- OpenROAD.
- KLayout.
- Magic, Netgen y demás herramientas requeridas por el flujo.
- Icarus Verilog o simulador equivalente.
- Python y herramientas para gráficos e informes.

Utiliza versiones compatibles y reproducibles. No mezcles versiones arbitrariamente.

Registra versiones exactas, revisión del PDK, variante, biblioteca estándar, comandos de instalación y configuración efectiva.

Prefiere GF180MCU D y la biblioteca estándar compatible que determine la instalación de LibreLane, verificando sus nombres reales.

Antes de ejecutar un flujo costoso, comprueba que la instalación funciona con una prueba apropiada.

No instales servicios de pago ni utilices recursos de nube que generen cargos.

Evita cambios destructivos al computador, el sistema y otros proyectos. No borres datos preexistentes ni credenciales.

## 4. IMPLEMENTACIÓN RTL: FPGA A ASIC

Crea el módulo superior `asic_top.v`.

Debe instanciar el SoC y exponer únicamente funciones lógicas necesarias:

- Clock.
- Reset explícito.
- Cuatro LEDs.
- Cuatro botones.
- Dos displays de siete segmentos.
- Señales SPI.

Conserva la funcionalidad original del juego.

Identifica y resuelve todas las construcciones dependientes de FPGA, incluyendo:

- `$readmemh`.
- Bloques `initial`.
- Inicialización de registros en declaraciones.
- Inferencia de memorias BRAM.
- Reset de encendido específico de la FPGA.
- Supuestos de clock y comportamiento de memorias.
- Cualquier primitiva o dependencia tecnológica incompatible.

Utiliza una estrategia ASIC sintetizable y verificable.

No basta con eliminar warnings: debes conservar el funcionamiento lógico.

Para cada incompatibilidad crea un registro de evidencia con:

1. Archivo y construcción afectada.
2. Warning o error real de LibreLane, con ruta al log y línea cuando exista.
3. Explicación técnica.
4. Modificación efectuada.
5. Validación posterior.

Si una construcción no genera warning, documenta por qué sigue siendo inapropiada para ASIC.

No inventes mensajes de las herramientas.

## 5. MEMORIA Y EXTENSIÓN DEL ASSEMBLER

Implementa obligatoriamente y compara dos arquitecturas distintas.

### Estrategia A: ROM + RAM

- ROM combinacional generada automáticamente desde `sw/game.s` mediante el assembler propio.
- RAM de datos reducida.
- Generación determinista y reproducible.
- Sin depender de que un archivo hexadecimal se cargue al encender el ASIC.

### Estrategia B: memoria unificada

- Memoria unificada implementada mediante flip-flops.
- Dimensionada según el uso real del juego.
- Mecanismo verificable para disponer del programa después del reset, sin depender de inicializaciones FPGA.
- Mantener y justificar el comportamiento de lectura, escritura y latencia.

La inicialización necesaria debe implementarse como hardware sintetizable o mediante un mecanismo de carga explícito y explicado. No consideres que una RAM de flip-flops sin contenido inicial ejecutará mágicamente el juego.

Si utilizas lógica auxiliar para cargar instrucciones, inclúyela honestamente en la comparación de área.

Límites recomendados por el profesor:

- 256 palabras de instrucciones.
- 64 palabras de datos.

Si necesitas excederlos, explica y fundamenta la razón antes de efectuar la comparación final.

No implementes un bootloader SPI como reemplazo de las dos alternativas.

Extiende `assembler/assembler.py` para producir los archivos RTL correspondientes a la ROM, conservando su funcionalidad original.

Escribe pruebas automáticas del assembler y de las dos memorias.

Mide y documenta:

- Palabras reales de instrucciones.
- Palabras reales de datos.
- Área de celdas.
- Número de flip-flops.
- Utilización.
- Frecuencia máxima obtenida.

No asumas el número de palabras de datos: dedúcelo del comportamiento real del programa, mapa de direcciones y pruebas.

Compara las dos estrategias bajo condiciones equivalentes y explica sus diferencias.

## 6. SÍNTESIS Y TRAZABILIDAD

Ejecuta síntesis real y conserva sus reportes.

Identifica las cinco celdas estándar más utilizadas y explica qué parte del RTL justifica su cantidad.

Determina:

- Módulo de mayor área.
- Área del register file.
- Área de la ALU.
- Área del contador de ciclos añadido en Proyecto 2.
- Fracción porcentual del área total que representa el contador.

Antes de obtener resultados, escribe una predicción razonada sobre los módulos que consumirán más área.

Después contrasta la predicción con los resultados medidos.

Conserva jerarquía o trazabilidad de:

- Register file.
- ALU.
- Contador de ciclos.

Si la síntesis aplana la jerarquía, utiliza estadísticas previas al aplanamiento, reportes jerárquicos o trazabilidad de instancias/celdas. Explica el procedimiento y verifica que las cifras son coherentes.

No atribuyas áreas arbitrariamente.

## 7. TIMING Y OPTIMIZACIÓN

Realiza un barrido de `CLOCK_PERIOD` utilizando por lo menos tres valores, incluyendo obligatoriamente 100 ns.

Busca el menor período que cierre timing bajo los criterios de la pauta.

Para cada corrida obtén WNS y TNS de setup y hold, tanto del corner típico como del más lento. Además, verifica los demás corners exigidos.

Presenta tablas generadas a partir de reportes reales.

Calcula la frecuencia máxima a partir del menor período que cierre timing en todos los corners exigidos:

`f_max = 1 / T_min`

Aclara la diferencia entre período objetivo, período de cierre observado y frecuencia máxima estimada.

Identifica la ruta crítica con:

- Celda o pin de inicio.
- Celda o pin de fin.
- Módulo.
- Retardo.
- Función microarquitectónica correspondiente: fetch, decode, ejecución, acceso a memoria o write-back.

Propón una modificación concreta al RTL destinada a mejorar esa ruta.

Impleméntala, prueba su equivalencia funcional y vuelve a sintetizar.

Compara:

- Slack anterior.
- Slack posterior.
- Área anterior.
- Área posterior.

Aunque la optimización no mejore el diseño, conserva los resultados y explica técnicamente por qué.

Explica que cambiar `CLOCK_PERIOD` puede provocar nuevas optimizaciones, variaciones de buffering, placement y área.

### Actualización de constantes del juego

El Proyecto 2 utilizaba un reloj de 25 MHz.

Su código original implementaba:

- Tres segundos: 75.000.000 ciclos.
- Una décima de segundo: 2.500.000 ciclos.
- Divisor del promedio de diez rondas: 25.000.000 ciclos.

Para el objetivo de 100 ns, la frecuencia es 10 MHz.

Por tanto, las constantes correctas para esta frecuencia son:

- Tres segundos: 30.000.000 ciclos.
- Una décima de segundo: 1.000.000 ciclos.
- Divisor equivalente para promedio de diez rondas: 10.000.000 ciclos.

Verifica todas las dependencias de estos valores en `game.s`.

Modifica las constantes correspondientes, regenera el programa y comprueba mediante simulación que la lógica sigue siendo correcta.

Conserva una forma reproducible de generar también la versión de simulación con espera abreviada.

## 8. FLOORPLAN, POWER DISTRIBUTION Y PLACEMENT

Implementa floorplan y red de alimentación apropiados para GF180MCU.

Explora por lo menos tres valores de `FP_CORE_UTIL` o tres dimensiones de `DIE_AREA`.

Incluye una corrida con la utilización final obligatoria del 40 %.

Ejecuta los experimentos necesarios para encontrar el área mínima que completa el flujo con los criterios exigidos.

Para cada variante registra métricas reales:

- Área.
- Utilización.
- DRC.
- Timing.
- Congestión o violaciones reportadas.
- Estado final de la corrida.

Genera un gráfico de utilización frente a violaciones o métrica de congestión.

Justifica la posición de terminales en el borde del macro según su función.

Distingue claramente terminales del macro de pads de I/O de un chip completo.

### Costo estimado

El profesor entrega el dato:

**US$23.000 por cada 1 mm².**

Calcula el costo equivalente usando el área medida del diseño y una relación lineal.

Utiliza una conversión correcta de unidades.

Explica las limitaciones de esta simplificación, incluyendo que no representa necesariamente el costo real de fabricar o encapsular un chip.

Identifica qué decisión de arquitectura tuvo mayor impacto sobre área y costo.

## 9. SIGNOFF Y LAYOUT

Ejecuta el flujo completo hasta generar GDSII.

Obtén resultados verificables de:

- DRC.
- LVS.
- Antena.
- Setup.
- Hold.

DRC y LVS deben resultar limpios para declarar la corrida final como cerrada.

Las violaciones de antena deberán corregirse o justificarse técnicamente con evidencia.

No desactives verificaciones para aparentar resultados satisfactorios.

Si aparecieron errores durante el desarrollo, conserva al menos un caso documentado, su localización en el layout y la explicación de cómo fue resuelto.

Si no apareció ningún caso, no fabriques uno.

Abre el layout en KLayout u OpenROAD GUI.

Identifica y anota visualmente las ubicaciones correspondientes a:

- Register file.
- ALU.
- Contador de ciclos.

Asegúrate de que las ubicaciones estén sustentadas por nombres de instancias, celdas o una metodología de trazabilidad reproducible.

Genera capturas reales, legibles y anotadas.

No utilices capturas inventadas, renders ilustrativos ni diagramas conceptuales como sustitutos de evidencia del layout.

## 10. SIMULACIÓN POST-SÍNTESIS

Construye un testbench que ejecute el juego y presione botones en ciclos de reloj determinados.

Realiza:

1. Simulación RTL.
2. Simulación del netlist post-síntesis, sin retardos anotados.

Aplica exactamente los mismos estímulos y la misma configuración de tiempo a ambas.

Debes demostrar:

- Una ronda correcta produce igual cantidad de ciclos medidos en ambas simulaciones.
- Una pulsación incorrecta reinicia la ronda actual.
- Las rondas correctas anteriores se conservan.
- Se respetan los mecanismos de reset e inicio del programa.

Utiliza una espera reducida para simulación si resulta necesario, siempre que documentes su implementación y sea idéntica en ambos modelos.

Guarda logs, resultados numéricos y formas de onda.

Automatiza la comparación mediante assertions o scripts.

No marques la simulación como aprobada sin ejecutar realmente el netlist post-síntesis.

La simulación post-PnR con SDF es opcional, y no debe desplazar los requisitos obligatorios.

## 11. EXPERIMENTOS REPRODUCIBLES

No quiero experimentos aislados que después no puedan repetirse.

Crea scripts que ejecuten, en la medida en que permita el flujo:

- Tests originales.
- Generación del juego.
- Generación de ROM.
- Simulación RTL.
- Síntesis de ambas estrategias.
- Barrido de timing.
- Barrido de utilización.
- Generación de métricas.
- Simulación post-síntesis.
- Corrida final.
- Extracción de evidencia para informe.

Usa nombres de corridas descriptivos e identificadores únicos.

Guarda los archivos de configuración efectivos de cada experimento.

Cada tabla y gráfico debe poder rastrearse a logs o métricas.

No combines resultados obtenidos con versiones distintas del RTL sin identificarlos.

Evita llenar Git con carpetas temporales enormes, caches o instalaciones del PDK. Conserva configuraciones, scripts, datos resumidos y los artefactos finales razonables para la entrega.

## 12. INFORME FINAL

Genera un archivo real:

`docs/Informe_Proyecto3.pdf`

Debe tener presentación profesional, redacción clara en español, ecuaciones bien formateadas, tablas, gráficos y capturas legibles.

Utiliza como referencia la organización del informe entregado en el Proyecto 2.

Identifica a los integrantes desde el informe original si esa información está disponible de manera confiable; no inventes nombres.

Estructura sugerida:

1. Portada.
2. Resumen ejecutivo.
3. Introducción y objetivo.
4. Arquitectura original del Proyecto 2.
5. Migración FPGA-ASIC.
6. Estrategias de memoria y extensión del assembler.
7. Síntesis y análisis jerárquico.
8. Barrido de timing y ruta crítica.
9. Optimización del RTL.
10. Actualización de constantes de tiempo.
11. Floorplan, alimentación y placement.
12. Análisis de área y costo.
13. Signoff, DRC, LVS y antena.
14. Layout y trazabilidad.
15. Simulación RTL versus post-síntesis.
16. Conclusiones.
17. Referencias.
18. Anexos de evidencias y reproducibilidad.

No incluyas tablas con datos supuestos como si fueran experimentales.

Cada conclusión importante debe estar respaldada por datos de tus corridas.

Verifica que el PDF abra correctamente, que las figuras no estén cortadas y que las tablas sean legibles.

Si algún criterio no se pudo cumplir, decláralo expresamente con evidencia y explicación.

## 13. README Y ESTRUCTURA DE ENTREGA

Prepara un README completo para GitHub, en español, que documente:

- Descripción general del Proyecto 3.
- Relación con el Proyecto 2.
- Arquitectura del sistema.
- Estructura de carpetas.
- Instalación de LibreLane.
- Instalación/configuración del PDK.
- Versiones exactas.
- Biblioteca estándar.
- Regeneración del programa desde `game.s`.
- Uso del assembler extendido.
- Ejecución de ambas estrategias de memoria.
- Simulaciones.
- Síntesis.
- Corrida final.
- Parámetros obligatorios.
- Resultados principales.
- Ubicación del informe y evidencias.
- Limitaciones conocidas.

Organiza el código de forma clara. Por ejemplo:

```text
Proyecto3AC/
├── assembler/
├── rtl/
├── sw/
├── sim/
├── asic/
│   ├── rtl/
│   ├── configs/
│   └── constraints/
├── scripts/
├── results/
│   ├── memory/
│   ├── timing/
│   ├── floorplan/
│   └── signoff/
├── docs/
│   ├── figures/
│   └── Informe_Proyecto3.pdf
├── Makefile
├── README.md
└── .gitignore
```

Puedes adaptar esta estructura según necesidades técnicas, pero mantenla ordenada y coherente.

No abandones los scripts existentes del Proyecto 2 innecesariamente.

## 14. PREPARACIÓN PARA LA DEFENSA

Además del informe, crea:

`docs/Guia_Defensa_Proyecto3.pdf`

Debe servir para que un estudiante de Arquitectura de Computadores pueda comprender y defender el proyecto.

Incluye:

- Resumen de arquitectura.
- Explicación sencilla de módulos importantes.
- Qué hace el assembler.
- Diferencia entre ROM y RAM.
- Qué son flip-flops y por qué afectan el área.
- Qué significan WNS, TNS, setup y hold.
- Cómo identificar una ruta crítica.
- Qué representa la utilización.
- Diferencia entre síntesis, placement, routing y signoff.
- Qué son DRC, LVS y antena.
- Cómo se calcula la frecuencia máxima.
- Cómo se estima el costo.
- Explicación de los cambios más importantes al RTL.

Agrega al menos 25 preguntas probables de defensa, con respuestas precisas y basadas en el proyecto real.

Relaciona cada explicación relevante con archivos, módulos, señales, resultados o líneas del código.

Prepara una sección específica sobre el register file, la ALU y el contador de ciclos.

No uses respuestas genéricas cuando exista información específica de nuestra implementación.

La defensa vale 1,5 puntos de un máximo de 6,0.

## 15. VALIDACIÓN CONTRA LA RÚBRICA

Antes de declarar el trabajo terminado, comprueba explícitamente estos criterios:

| Ítem | Puntaje |
|---|---:|
| Del RTL FPGA al RTL ASIC | 0,5 |
| Memoria, programa y assembler | 1,0 |
| Síntesis y trazabilidad | 0,4 |
| Timing y optimización | 1,0 |
| Floorplan, placement y costo | 0,5 |
| Signoff y layout | 0,5 |
| Simulación post-síntesis | 0,6 |
| Defensa presencial | 1,5 |
| **Total** | **6,0** |

Crea `docs/CHECKLIST_ENTREGA.md`.

Para cada ítem registra:

- Estado: completo, parcial o pendiente.
- Archivos que lo respaldan.
- Prueba o corrida realizada.
- Evidencia disponible.
- Problemas pendientes.

No declares éxito únicamente porque una herramienta haya terminado sin mostrar errores evidentes.

## 16. CONDICIONES DE CALIDAD

Prioridades:

1. Correctitud funcional.
2. Cumplimiento del enunciado.
3. Evidencia experimental.
4. Reproducibilidad.
5. Calidad técnica del informe.
6. Orden de GitHub.

No ocultes problemas ni inventes resultados.

Si un flujo falla, inspecciona logs, formula una causa, aplica una corrección y vuelve a ejecutar.

No reemplaces simulaciones faltantes por explicaciones teóricas.

No sustituyas un GDSII real por un dibujo.

No modifiques la arquitectura solamente para obtener mejores números si eso rompe el juego.

No sacrifiques resultados obligatorios para agregar funcionalidades opcionales.

Si un problema técnico sigue sin solución después de intentos razonables, documenta claramente el bloqueo, deja los archivos reproducibles y continúa con las demás actividades independientes.

Registra cualquier diferencia de configuración que impida comparar dos corridas de manera justa.

## 17. POLÍTICA ESTRICTA DE GIT Y GITHUB

Esta sección es obligatoria y tiene prioridad sobre cualquier automatización de Git.

El repositorio del Proyecto 2 debe conservarse intacto.

Prepara un directorio independiente `Proyecto3AC` a partir de su versión entregada y conserva correctamente el historial y la procedencia.

Puedes crear un repositorio remoto nuevo y vacío `FelixSvensson/Proyecto3AC` si la autenticación y permisos lo permiten, sin subir archivos ni crear commits.

Si no es posible, deja preparado el repositorio local y proporciona las instrucciones para crear el remoto manualmente.

**PROHIBIDO:**

- Ejecutar `git commit`.
- Ejecutar `git push`.
- Crear commits mediante herramientas, APIs o interfaz de GitHub.
- Realizar merges que generen commits.
- Reescribir historia existente.
- Ejecutar `git reset --hard` sobre trabajo del usuario.
- Modificar el autor o committer para simular una identidad.
- Introducir como autor a Codex u otra identidad automática.

No establezcas una dirección de correo inventada.

Al finalizar verifica:

```bash
git status
git branch --show-current
git remote -v
git config user.name
git config user.email
```

El objetivo es que yo cree personalmente el commit utilizando mi identidad real de GitHub y un correo asociado a mi cuenta.

Deja todos los cambios preparados, sin commitear ni subir.

Proporcióname exactamente los comandos que debo copiar para:

1. Verificar que Git utilizará mi identidad.
2. Añadir los archivos correctos.
3. Crear personalmente el commit.
4. Subir la rama al repositorio nuevo.
5. Verificar la publicación.

Puedes sugerir este mensaje:

`Proyecto 3: implementación ASIC de Pochoco SoC con LibreLane y GF180MCU`

Si hay archivos grandes, secretos, logs temporales o datos que no deban publicarse, resuélvelo previamente con `.gitignore` y revisa la lista de archivos.

**No ejecutes nunca el commit o push, aunque todo esté aprobado.**

## 18. EJECUCIÓN AUTÓNOMA

No te detengas después de analizar el repositorio ni después de redactar un plan.

Trabaja por fases:

**Fase 1:** diagnóstico del entorno y repositorio.

**Fase 2:** instalación y validación de herramientas.

**Fase 3:** implementación ASIC y ambas memorias.

**Fase 4:** tests funcionales y síntesis.

**Fase 5:** experimentos de timing y área.

**Fase 6:** floorplan, placement, routing y signoff.

**Fase 7:** simulación post-síntesis.

**Fase 8:** informe, gráficos y guía de defensa.

**Fase 9:** auditoría final de rúbrica y preparación de GitHub.

En cada fase, utiliza los resultados para orientar la siguiente.

Tienes autorización para ejecutar las acciones necesarias dentro del alcance del proyecto, sin solicitar confirmación para cada comando ordinario.

No realices cambios destructivos fuera del proyecto, no expongas credenciales y no consumas recursos pagados.

Si necesitas un dato esencial que realmente no puedas obtener del repositorio, enunciado o entorno, déjalo identificado; no inventes la información.

Entrega periódicamente estados concretos, con las corridas completadas, errores encontrados y evidencia registrada.

## 19. DEFINICIÓN DE TRABAJO TERMINADO

Antes de terminar, necesito que verifiques:

- El proyecto parte de nuestro Proyecto 2 real.
- El juego conserva su funcionamiento.
- Las dos memorias están implementadas.
- El assembler genera la ROM automáticamente.
- El RTL ASIC es sintetizable.
- Existen mediciones reales de síntesis.
- Se completaron los barridos obligatorios.
- Se calculó correctamente la frecuencia máxima.
- Se probó la modificación de la ruta crítica.
- Se actualizaron las constantes del juego.
- El flujo final se intentó con 100 ns y 40 %.
- Existe un GDSII real si el flujo completó satisfactoriamente.
- Los resultados de DRC, LVS, antena y timing están verificados.
- Se compararon las simulaciones RTL y post-síntesis.
- Hay capturas auténticas del layout.
- El informe PDF es coherente con los archivos de evidencia.
- El README permite reproducir los resultados.
- La guía de defensa está basada en nuestra implementación.
- La rúbrica está revisada ítem por ítem.
- GitHub está preparado para mi commit manual.

Si alguna condición está pendiente, indícala expresamente; no afirmes que la entrega está completa.

Tu último mensaje debe incluir un resumen de los trabajos realizados, los resultados medidos más importantes, los archivos finales, los criterios pendientes y los comandos necesarios para que yo haga el commit y push.

**Empieza ahora inspeccionando el entorno y el repositorio. Después continúa con la implementación real, no solamente con una propuesta.**