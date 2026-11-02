> Registro histórico anterior al cierre. Estado vigente: ESTADO_ACTUAL.md.

# Estado vigente — actualizado el 2 de noviembre de 2026

**REANUDADO a petición del usuario («Continua»).** La pausa anterior detuvo los
procesos de LibreLane y OpenROAD de la corrida B30 y se comprobó que no quedan
procesos EDA del proyecto activos durante la pausa.
Corrida pausada: B_p100_u30_v2_resume_20261102T151832Z, etapa
07-openroad-detailedrouting. Última iteración completa: 6, con 2643 violaciones.
Se conservan snapshots, reportes y logs; B no tiene signoff final.
La lista de procesos detenidos está en results/environment/latest_pause_processes.json.
La corrida activa es B_p100_u30_v2_resume_20261102T153658Z y carga drt_iter6.odb
de la corrida pausada. El router recupera los cables guardados, pero reinicia
sus contadores y estado de optimización: no se declara continuación exacta de
la iteración 6. Hash del snapshot y consola: results/environment/B_u30_candidate.json.
B30 terminó DetailedRouting con cero violaciones en las tres pasadas
(drt-run-0/1/2). La comprobación posterior de antenas reporta cero nets y pins
en violación. STA post-ruteo pasa setup/hold en nueve corners a 100 ns:
setup mínimo +9,666202334 ns; hold mínimo +0,119682712 ns. El flujo continúa
con GDS, Magic DRC y LVS. La búsqueda de frecuencia de este layout está activa:
results/timing/B_u30_frequency_characterization.log. No se declara cierre final
hasta revisar todos los verificadores.

Se probó el empaquetado y restauración portable de los diez archivos de entrada
del ECO B40: hashes idénticos, ZIP de 16 MB en work/ (prueba, no entrega final).
scripts/archive_checkpoint.py y restore_checkpoint.py permiten conservar solo
el checkpoint elegido, excluyendo PDK y herramientas.

Se probó además B_v2_p100_u40_detour_20261102T155443Z, un ECO físico dirigido
al cruce Metal3 que persistió en B40. En una copia se quitaron los dbWire de
los dos nets afectados y se añadió una obstrucción de routing Metal3 de
(750,82;852,18)-(751,66;853,02) µm para forzar otro recorrido. No se movieron
celdas ni se alteraron conexiones lógicas: el hash completo del grafo coincide
antes/después. Sigue a 100 ns / 40 %, dos threads y orden de routing por defecto.
Preparación reproducible: scripts/prepare_b_detour.py; metadatos y hashes:
results/environment/B_detour_candidate.json. Su primera pasada llegó a cero,
pero la reparación posterior de antenas abrió otra pasada, que conservaba 64
violaciones cuando se detuvo como intento redundante tras terminar el routing
y antena de B30. Conserva sus archivos y no tiene signoff. Procesos detenidos
verificados: results/environment/stopped_redundant_flows.json.

## Historial anterior

Se reanudó a solicitud del usuario. Los archivos PAUSA_ACTUAL.md y
PAUSA_Y_ESTADO_ACTUAL.md documentan pausas anteriores y no indican el estado actual.

A conserva su GDS final a 100 ns y 40 %, DRC Magic/LVS/antena sin violaciones
y setup/hold limpios en nueve corners. No hubo cambios en las fuentes del
hardware desde los experimentos: audit_sources.py volvió a comprobar sus hashes.

El primer intento reanudado fue B_v2_p100_u40_snapshot_resume desde drt_iter2.odb de la
corrida interrumpida. Se cargan los cables ROUTED del ODB, pero OpenROAD
reinicia su estado de optimización. No se declara una continuación exacta de
la iteración anterior ni cierre físico hasta finalizar los verificadores.
Snapshot y hash: results/environment/B_snapshot_resume.json.
Salida de ejecución: results/environment/B_snapshot_resume_console.log.
La primera pasada terminó con DRC de router cero en la iteración 29. El flujo
reparó antena y volvió a rutear las conexiones afectadas (drt-run-1). Todavía no
existe signoff final de B.

El segundo routing quedó en un cruce Metal3 entre u_pochoco.u_ram._07185_ y
u_pochoco.u_ram._08839_. Se conservaron dos candidatos adicionales, sin sobrescribir
la corrida anterior:

- B_v2_p100_u40_cold_resume: proceso nuevo desde el estado posterior a antena,
  cuatro threads, snapshot congelado y hash en results/environment/B_cold_resume.json.
- B_v2_p100_u40_eco_resume: en una copia se retiró únicamente el dbWire físico
  de u_pochoco.u_ram._08839_ (tres terminales) para reconstruirlo con el router,
  dos threads. El hash completo de conexiones lógicas es idéntico antes/después
  de esa operación. Evidencia: results/environment/B_routing_eco.json.

Los candidatos deben pasar DRC/LVS/antena y STA; el ECO no se considera aprobado
por haber preservado el hash de conexiones. Ninguno modifica RTL, programa,
PDK, período de 100 ns ni utilización del 40 %. La selección final se registrará
en results/environment/selected_b_run.json después de revisar sus resultados.

Las pruebas cold_resume y eco_resume conservaron el mismo cruce y se detuvieron
como pruebas redundantes; sus puntos de avance se mantienen. La corrida original
también se detuvo al persistir el mismo cruce. Se probó B_v2_p100_u40_ordered_resume.
Esta última usa la copia ECO y un orden
de reparación DRT distinto: or_seed=43, or_k=1, dos threads. El launcher
scripts/run_ordered_flow.py genera el Tcl desde la instalación fijada, registra
ambos hashes y cambia get_script_path solo en su proceso. No modifica herramientas
instaladas ni checkers. Evidencia: results/environment/B_ordered_routing.json y
stopped_redundant_flows.json. Falta verificar el resultado; no se afirma cierre.

La alternativa principal parte de B_p100_u30_v2_20261102T035316Z: flujo completo a
100 ns y 30 %, orden de routing predeterminado y seis threads. Se comparará con
A_p100_u30_v2_resume, ejecutado a los mismos 100 ns y 30 %. El final obligatorio
de A permanece a 100 ns y 40 %. Esto proporciona una comparación equivalente
de las memorias sin presentar las pruebas B al 40 % como terminadas.
Evidencia: results/environment/B_u30_candidate.json y B_u30_console.log.

Después de un reinicio de WSL se comprobó que no quedaban procesos EDA activos.
El 2 de noviembre se reanudó B30 en B_p100_u30_v2_resume_20261102T151832Z desde
el state_out completo de 37-openroad-resizertimingpostcts. Se repite STA posterior
a CTS y se continúa el flujo sin repetir síntesis ni alterar RTL/configuración.
El ODB de entrada tiene SHA256 dc927add1a065a191fbba886166dd150d8fa97ed6bdc1627901e8f8a2d8ce30c.
Los directorios anteriores se conservan. B40 ordered también quedó interrumpido
por el reinicio y no se ha relanzado. Consola vigente: B_u30_resume_console.log.

La caracterización STA del layout fijo A al 30 % terminó: 57 ns pasa los nueve
corners (setup mínimo +0,31544 ns) y 56 ns falla. Frecuencia en la cuadrícula de
1 ns: 17,54386 MHz. Este resultado de comparación es distinto del final A al
40 %, cuyo límite medido sigue siendo 59 ns (16,94915 MHz).

Se corrigió una interpretación de congestión de los documentos anteriores:
OpenROAD sobrescribe route__drc_errors__iter:0 al volver a rutear por antena.
Los conteos iniciales reales, extraídos del primer resultado del log, son
1764/2026/3061 para A a 30/40/50 %. En el final con terminales agrupados, las
pasadas son 1924,665,476,3,0 y luego 18,1,0 después de reparar antena. Las cifras
anteriores 139/4/3061 eran métricas crudas de iteración 0 y no siempre la primera
pasada. Los resultados finales de DRC y timing no cambian. Ver RESULTADOS_MEDIDOS.md.

Los PDF se revisaron como imágenes. Se están corrigiendo detalles de paginación,
fecha y tablas antes de la revisión final. Las cifras de B se incorporarán solo
cuando existan reportes físicos terminados.

La auditoría inicial de publicación confirmó que ningún archivo visible a Git
supera 10 MB; se excluyen caches, PDK y ODB intermedios. Falta regenerar el
archivo de evidencias y la auditoría final al terminar B.

No se ejecutó commit ni push. Proyecto2 no se modificó. La creación del remoto,
el commit y el push corresponden al usuario según PUBLICAR_MANUALMENTE.md.
