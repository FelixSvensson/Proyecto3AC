> Registro histórico. Para el estado vigente, consultar [ESTADO_ACTUAL.md](ESTADO_ACTUAL.md).

# Pausa solicitada por el usuario - 28 de octubre de 2026

El usuario indicó «deten, seguiremos otro dia». Se detuvo el único árbol de
procesos EDA activo (B: PID 388 y descendientes 401/416). Se verificó que no
quedan procesos LibreLane/OpenROAD del proyecto activos. No reanudar hasta
recibir una nueva instrucción explícita del usuario.

Este archivo sustituye como punto de reanudación a PAUSA_Y_ESTADO_ACTUAL.md,
que describe una pausa anterior. No hubo commit ni push; Proyecto 2 sigue intacto.

## Avance nuevo desde la pausa anterior

- Barrido completo de utilización A a 100 ns: 30/40/50 % cerrados con DRC
  Magic/LVS/antena=0 y setup/hold limpios en nueve corners.
  - 30 %: die 547.483 µm²; utilización ruteada antes de filler 39,2346 %;
    peor setup +43,315436 ns; costo lineal US$12.592,109.
  - 40 %, final obligatorio: die 414.450 µm²; ocupación ruteada 51,6665 %;
    peor setup +41,459616 ns y hold +0,107384 ns; US$9.532,35.
  - 50 %: die 334.270 µm²; ocupación ruteada 63,6718 %;
    peor setup +38,455363 ns; US$7.688,21. Es el mínimo observado en la grilla,
    pero la entrega conserva el 40 % obligatorio.
- Barrido de período con síntesis/PnR: 100/80/60 ns cierran; 50 ns falla setup
  (WNS lento -8,868096 ns), aunque LibreLane devuelve código de salida cero.
  El recolector verifica métricas por corner y clasifica ese resultado como falla.
- Refinamiento sobre el GDS final fijo y los mismos retardos externos absolutos:
  59 ns cierra los nueve corners (+0,459622 ns setup mínimo); 58 ns falla
  (-0,540378 ns). Máximo observado con resolución 1 ns: 16,949153 MHz.
  No confundir con una nueva síntesis/PnR a 59 ns. Entrega final: 100 ns/10 MHz.
- Ruta crítica final extraída con trazabilidad real:
  u_pochoco.u_ram._604_/Q (instr_rdata[4]) a u_pochoco.u_ram._648_/D
  (estado ram_b_rdata[16]), corner max_ss_125C_4v50. Q→D=54,650438 ns;
  llegada total 60,116585 ns; slack +41,459614 ns. JSON y reporte en results/timing/.
- Capturas de RF/ALU/contador actualizadas al GDS final_A_v2_p100_u40, en gris
  con resaltados reales derivados de OpenDB. No abrir ventanas visibles.
- Caso espacial DRC ahora documentado: DEBUG_first_route retiene un estado
  previo a optimizaciones (DRT_OPT_ITERS=0), con 1924 violaciones. Caso Short
  Metal2 entre regs[2][11] del RF y net462, bbox (33,74;154,09)-(34,02;154,47) µm.
  Capturas nativas antes/después, reporte crudo y configuración en
  results/incidents/drc_case/ y docs/figures/drc_before.png / drc_after.png.
  No es una corrida de signoff ni el mismo conteo que iteración 0 del flujo
  completo. El routing completo final registra 18,1,0,3,0 y termina limpio.
- También se ejecutó netlist GF180 de B con imagen abreviada: mismos estímulos
  y resultados que RTL (136 ciclos por acierto, 1360 acumulados, diez rondas,
  botón incorrecto y resets). results/synthesis/B_sim_hier/gate_comparison.json.
- Auditoría del programa original: fuente main espera 250.000.000 ciclos,
  pero game.hex incluido espera 75.000.000; difieren solo palabras 8/9. Ambos
  tienen 107 instrucciones. Evidencia original_program_consistency.json.
- Se corrigió .gitignore: solo se ignoran /asic/configs/runs/, no los reportes
  curados en results/runs/. Nunca publicar caches, PDK ni snapshots ODB grandes.
- Se actualizaron tablas, README y scripts. Se regeneraron ambos PDF con nueve
  corridas terminadas y se renderizaron sus páginas en work/pdfqa_final/.
  Falta inspección visual de esa última versión antes de declararlos finales.

## Corrida B pendiente y recuperación

Hubo un reinicio externo de WSL entre sesiones que dejó sin procesos las
corridas largas anteriores. Se recuperó A 50 % y terminó; B se relanzó como
B_v2_p100_u40_recovery, con snapshots por iteración y reportes DRC persistentes.
Ese proceso se detuvo ahora a solicitud del usuario, conservando:

- asic/configs/runs/B_v2_p100_u40_recovery/01-openroad-detailedrouting/drt-run-0/
  drt_iter0.odb (44 MB), drt_iter1.odb (45 MB), drt_iter2.odb (46 MB),
  asic_top.drc-1.rpt y asic_top.drc-2.rpt.
- La corrida aún no tiene signoff ni GDS final. No atribuirle cierre.
- Configuración asic/configs/B_recovery.json: DRT_THREADS=8 (A usa 6),
  DRT_SAVE_SNAPSHOTS=true, DRT_SAVE_DRC_REPORT_ITERS=1. Registrar esa diferencia
  de ejecución al comparar resultados; reloj/utilización/PDK/RTL son los mismos.
- Evaluar cómo recuperar routing desde drt_iter2.odb con OpenROAD; no asumir
  sin verificar que una nueva llamada reutiliza incrementalmente todos los cables.
  No sobrescribir carpetas terminadas. Si no se puede, el estado completo previo
  sigue en B_v2_p100_u40/43-openroad-stamidpnr-3/state_out.json.

## Lo que resta

1. Completar o resolver el routing B y documentar su resultado real; medir su
   frecuencia del layout con STA cuando exista SPEF post-route. A ya está cerrada.
2. Revisar visualmente todas las páginas de los PDF actualizados, corregir
   cualquier defecto y actualizar texto/tablas si se agregan resultados B.
3. Actualizar checklist y README al estado final; limpiar notas históricas que
   pudieran confundirse con el estado vigente, sin destruir evidencia.
4. Terminar auditoría de hashes/tamaños/secretos/lista publicable y regenerar
   archivo de evidencia con scripts/archive_evidence.py (ahora evita copias idénticas).
5. Mantener explícitas las limitaciones eléctricas del final: 2196 violaciones
   de slew, 57 de fanout y 4 de capacitancia en el peor corner. El deck KLayout DRC
   no existe en esta instalación; DRC limpio se refiere a Magic y router.
6. Preparación de GitHub manual: remoto Proyecto3AC no existe o no es accesible,
   el conector no permite crearlo vacío. Comandos en PUBLICAR_MANUALMENTE.md.
   Prohibido ejecutar commit o push. La defensa presencial corresponde al grupo.

## Entorno y precauciones

El marcador PDF para dos documentos ya se ejecutó; no repetirlo. Python Windows
del runtime con PYTHONPATH al work/pythonpackages del chat permite ejecutar
scripts/build_documents.py. requirements-docs.txt fija dependencias. Poppler en
Ubuntu renderiza los PDF. Las rutas y versiones completas están en README.

Las imágenes de KLayout son vistas reales: no usar ImageGen. Usar -z y evitar
ventanas visibles; la captura Windows/WSLg devolvió imágenes equivocadas.
Las áreas de síntesis jerárquica y LibreLane son mediciones distintas, identificadas
como tales. No mezclar números v1 y v2 ni métricas intermedias con signoff final.
