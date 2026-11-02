> Registro histórico. Para el estado vigente, consultar [ESTADO_ACTUAL.md](ESTADO_ACTUAL.md).

# Proyecto pausado por solicitud del usuario

El usuario pidió detener el trabajo para conservar su cupo de uso y avisará
cuándo continuar. **No reanudar ni lanzar nuevas corridas hasta ese aviso.**
Este archivo reemplaza, para la reanudación, el estado anterior al reinicio.

## Ya ejecutado y verificado

- Ubuntu 24.04.5 bajo WSL2 instalado y operativo. LibreLane 3.0.17 AppImage,
  GF180MCU D y biblioteca gf180mcu_fd_sc_mcu7t5v0 instalados y smoke test aprobado.
- Copia independiente Proyecto3AC con historial de Proyecto2AC/main 67d0c48.
  Proyecto 2 remoto permanece en las revisiones originales. No se hizo commit
  ni push. El remoto proyecto2 tiene pushurl=DISABLED.
- Migración ASIC: reset explícito, register file FF con lecturas síncronas,
  contador trazable, memorias A (ROM + RAM) y B (FF con programa por reset).
- Assembler extendido, 107 instrucciones verificadas, constantes finales para
  10 MHz. Fuente FPGA original preservado en sw/game_fpga_original.s.
- Seis pruebas originales del assembler y tres de la ROM aprobadas. Prueba
  original del periférico aprobada. Ambas memorias y el juego de diez rondas,
  error de botón, promedio y reset/reinicio aprobados.
- RTL A/B y netlist jerárquico GF180 A: estímulos idénticos por ciclo y trazas
  iguales; 136 ciclos por acierto y 1.360 acumulados. Ondas en work/ y algunas
  comprimidas en results/functional/waves/; completar archivado al reanudar.
- Síntesis jerárquica comparable: A 147.741,3504 µm²; B 613.575,9616 µm².
  Las cifras LibreLane son otras por sus optimizaciones; no confundirlas.
- Corrida final_A_v2_p100_u40 completada: 100 ns, 40 %, terminales agrupados,
  GDS real; DRC Magic=0, LVS=0, antena=0, nueve corners sin violaciones setup/hold.
  Área de síntesis LibreLane 154.474,0288 µm²; die 414.450 µm² (0,41445 mm²).
  Peor slack setup +41,45961558 ns; hold +0,10738377 ns. Costo lineal US$9.532,35.
  Permanecen advertencias de capacitancia; el deck DRC KLayout no está configurado.
- Barrido A comparable terminado a 100, 80 y 60 ns, todos con cierre en nueve
  corners. A 60 ns peor setup slack +1,13191593 ns. Menor período ensayado
  cerrado: 60 ns = 16,6667 MHz; aún no se ensayó por debajo para acotar el límite.
- Variante optimizada A_opt_v2_p100_u40: cierre completo, área de síntesis
  158.194,8928 µm² y peor setup slack +41,24584879 ns. Frente a A_v2_p100_u40:
  +0,11393553 ns de slack con aproximadamente +2,409 % de área. No compensa;
  se mantiene baseline para la final. Pasó juego y 2.000 ciclos comparativos
  aleatorios de memoria; no es una demostración formal exhaustiva.
- Capturas reales de KLayout y coordenadas de instancias de RF/ALU/contador
  obtenidas para A_v2_p100_u40. La vista gris con resaltados es legible; las
  primeras capturas multicolor se reemplazaron. No abrir más ventanas visibles.
- Existen borradores PDF de informe y guía (39 preguntas), README y comandos
  de publicación manual. Los PDF aún muestran una recopilación anterior de
  tres corridas: deben actualizarse y revisarse visualmente antes de entrega.

## Interrupciones realizadas al pausar

Se detuvieron únicamente los árboles de procesos del proyecto enumerados en
results/environment/paused_processes.json. Se paró primero el planificador para
impedir nuevas corridas y luego los procesos, conservando los archivos y estados
completados. No son procesos suspendidos en RAM: la etapa incompleta necesitará
relanzarse desde un estado guardado o mediante nueva corrida.

- B_v2_p100_u40 quedó en detailed routing, todavía sin signoff final.
- A_p100_u30_v2_20261028T153515Z quedó incompleta durante el flujo.
- A_p100_u50 no se había iniciado.
- B_gf180_p100_u40 (v1) se había cancelado antes por duplicar el trabajo v2.
- No se borró ninguna carpeta de corrida ni se publicaron archivos.

## Pendientes al reanudar

1. Revisar estados existentes y reanudar B v2 y los dos puntos del barrido de
   utilización (30 y 50 %) sin sobreescribir evidencia terminada. No iniciar
   varios trabajos pesados redundantes. Verificar DRC/LVS/timing reales de B.
2. Ensayar al menos un período menor de 60 ns si se busca acotar el máximo;
   distinguir menor período ensayado de máximo continuo demostrado.
3. Extraer ruta crítica final con pines, función y retardo exacto, y contraste
   numérico de la optimización. El informe actual identifica la ruta v1.
4. Extraer coordenadas y capturas del GDS final_A_v2_p100_u40; las imágenes
   existentes corresponden a la referencia A_v2 con distribución de pines previa.
   Usar KLayout -z (sin ventanas visibles). La captura de WSL con sky fue errónea.
5. Revisar advertencias de capacitancia y documentar límites. El caso de DRC
   inicial corregido tiene conteo real pero falta ubicación individual conservada;
   no inventarla. Mantenerlo parcial si no se recupera evidencia espacial.
6. Actualizar collect_results.py/archive_evidence.py, tablas/gráficos y PDFs;
   hacer QA visual de todas las páginas, completar CHECKLIST_ENTREGA.md y auditoría.
7. Revisar reproducibilidad, archivos grandes/secretos/.gitignore, manifiestos
   de todas las corridas y comandos exactos del alumno. No ejecutar commit/push.

## Entorno de documentación y comandos útiles

Python Windows del runtime: C:\Users\Lenovo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe.
ReportLab 4.4.9 ya disponible. Matplotlib 3.11.2 y dependencias instaladas localmente
en work/pythonpackages del chat (fuera del repo); definir PYTHONPATH a ese directorio.
Poppler está instalado en Ubuntu; páginas preliminares renderizadas en work/pdfqa/
del repo. El marcador de operación PDF ya se ejecutó para dos documentos; no repetir.

El perfil GitHub conectado devolvió FelixSvensson y fasvensson@miuandes.cl; esos
valores se configuraron solo localmente en Proyecto3AC. No se cambió Git global.
Proyecto3AC remoto devolvió Repository not found y el conector no tiene una
operación para crear repositorios vacíos. El alumno deberá crearlo manualmente.
Ver docs/PUBLICAR_MANUALMENTE.md. Nunca ejecutar commit ni push.
