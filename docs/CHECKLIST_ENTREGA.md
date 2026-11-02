# Checklist de entrega - revisión local completa

**Trabajo local completado y revisado el 2 de noviembre de 2026; publicación y defensa pendientes del grupo.**
B_p100_u30_v2_resume_20261102T153658Z cierra DRC Magic/LVS/antena y timing
en nueve corners a 100 ns / 30 %. Se compara con A al mismo 30 %; el GDS
final obligatorio de A permanece a 100 ns / 40 %. Las métricas están en
results/summary.csv y la selección en results/environment/selected_b_run.json.

| Ítem | Puntaje | Estado | Respaldo y prueba | Pendiente |
|---|---:|---|---|---|
| Del RTL FPGA al RTL ASIC | 0,5 | Completo funcionalmente | asic/rtl/, MIGRACION_ASIC.md; juego RTL/netlist aprobado | Verificado |
| Memoria, programa y assembler | 1,0 | Completo medido | A/B implementadas; 107 instrucciones; tests aprobados; comparación física a 100 ns / 30 %; A pasa 57 ns y B 91 ns, ambos con fallo medido a 1 ns menos | Verificado |
| Síntesis y trazabilidad | 0,4 | Completo medido | results/synthesis/*/stat.json; áreas RF/ALU/contador; coordenadas y capturas del GDS final | Verificado |
| Timing y optimización | 1,0 | Completo medido | 100/80/60 ns cerrados, 50 ns falla; variante medida/probada; layout final fijo pasa 59 ns y falla 58 ns; ruta final extraída | Verificado |
| Floorplan, placement y costo | 0,5 | Completo medido | 30/40/50 % cerrados; gráfico real de tres puntos, áreas/costos y terminales | Verificado |
| Signoff y layout | 0,5 | Completo para criterios explícitos | GDS A final a 100 ns / 40 % y B comparativa a 100 ns / 30 %; DRC Magic/LVS/antena=0 y timing limpio en nueve corners; capturas auténticas | Persisten límites eléctricos de slew/fanout/capacitancia de A y B declarados |
| Simulación post-síntesis | 0,6 | Completo ejecutado | Netlists A y B: results/synthesis/*_sim_hier/gate_comparison.json; estímulos/trazas iguales y ondas | Verificado |
| Defensa presencial | 1,5 | Pendiente presencial | Guía basada en la implementación y las mediciones, con 41 preguntas específicas | Preparación y defensa del grupo; guía revisada |
| Documentación y GitHub | - | Completo local; publicación personal pendiente | README, PDFs, scripts, paquete de reanudación con hashes verificados y PUBLICAR_MANUALMENTE.md | Crear/verificar remoto vacío y ejecutar personalmente commit/push; PDF revisados y evidencias auditadas |

No se ejecutó commit ni push. Proyecto 2 permanece intacto. No se declara DRC
de KLayout aprobado: falta deck configurado y el DRC reportado es de Magic.
