# Estado final local - 2 de noviembre de 2026

El desarrollo y la revisión local están terminados. No quedan procesos EDA del
proyecto activos. El informe final tiene 15 páginas y la guía, 5 páginas con
41 preguntas. Todas las páginas renderizadas se revisaron visualmente; hashes
y alcance: results/environment/pdf_visual_qa.json.

- Final obligatorio: final_A_v2_p100_u40, 100 ns / 40 %, GDS real,
  DRC Magic/LVS/antena en cero y setup/hold limpios en nueve corners.
- Comparación de memorias: A_p100_u30_v2_resume y
  B_p100_u30_v2_resume_20261102T153658Z, ambas a 100 ns / 30 %, seis threads,
  mismo programa, biblioteca y routing predeterminado. Ambas cumplen esos
  criterios de signoff. B terminó las tres pasadas de routing en cero.
- Layout fijo: A comparativa pasa 57 ns y falla 56 ns (17,543860 MHz);
  B pasa 91 ns y falla 90 ns (10,989011 MHz). El final A al 40 % pasa 59 ns
  y falla 58 ns (16,949153 MHz). Resolución de 1 ns; no es un nuevo PnR.
- Las simulaciones RTL y netlist A/B, assembler, memorias y variante de
  optimización están aprobadas. Las fuentes del hardware no cambiaron desde
  el snapshot de las mediciones; sus hashes fueron auditados.
- Vistas curadas idénticas a las corridas originales:
  results/environment/final_artifact_audit.json. La identidad de ODB/SPEF y
  de las restricciones salvo período fue verificada en las muestras A/B:
  results/environment/fixed_layout_input_audit.json.
- Checkpoint B portable: results/checkpoints/B_p100_u30_v2_resume_20261102T153658Z.zip.
  Se restauraron y verificaron sus diez vistas. Instrucciones: REPRODUCIR_B.md.

Las pruebas B al 40 % permanecen como intentos incompletos. El desvío físico
local llegó a cero en su primera pasada y se detuvo después, con 64 violaciones
en la pasada posterior a antenas, cuando B30 ya había cerrado routing y antena.
No se le atribuye signoff. Se conservan logs, estados y hashes.

## Límites y pasos personales pendientes

A mantiene 2.196 violaciones máximas de slew, 57 de fanout y 4 de capacitancia;
B mantiene 15.634, 291 y 1.923. No se declara cierre eléctrico completo ni
fabricación garantizada. No hay deck KLayout DRC configurado; el DRC limpio
reportado corresponde a Magic. El diseño es un macro sin pads físicos.

La defensa presencial y la publicación corresponden al grupo. El conector
no permite crear un repositorio remoto vacío y la última consulta al remoto
no permitió acceder a Proyecto3AC: crear/verificar ese remoto personalmente
siguiendo PUBLICAR_MANUALMENTE.md. No se ejecutó git add, commit ni push.
Proyecto 2 permanece intacto; su push está deshabilitado en este clon.

El historial de esta reanudación se conserva en
HISTORIAL_REANUDACION_2026-11-02.md. Las pausas anteriores son históricas.
