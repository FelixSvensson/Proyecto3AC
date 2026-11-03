# Índice de evidencia reproducible

Los archivos enlazados forman parte de la entrega. Las carpetas temporales
`asic/configs/runs/` permanecen fuera de Git; pueden reconstruirse con los scripts.

| Resultado | Evidencia incluida | Cómo reproducir |
|---|---|---|
| Procedencia | [inconsistencia original](../results/environment/original_program_consistency.json) | `scripts/audit_original_program.py` |
| Programa, 107 instrucciones | `sw/game.s`, `sw/game.hex`, `asic/generated/` | `make -f Makefile.asic generate` |
| Tests originales, ROM, memoria y juego | `results/functional/`, `results/optimization/` | `make -f Makefile.asic verify` |
| Netlists A/B ejecutados | `results/synthesis/A_sim_hier/gate_comparison.json`, `results/synthesis/B_sim_hier/gate_comparison.json` | `scripts/gate_verify.py A_sim_hier` y `B_sim_hier` |
| Área jerárquica comparable | `results/synthesis/A_prod_hier/stat.json`, `results/synthesis/B_prod_hier/stat.json` | `bash scripts/hier_batch.sh` |
| Barridos físicos y cierre por corner | [Resumen](../results/summary.csv), `results/runs/*/corners.csv` | `scripts/experiment_batch.sh`, `scripts/collect_results.py` |
| GDS final de A a 100 ns / 40 % | [GDSII](../results/runs/final_A_v2_p100_u40/views/gds/asic_top.gds), [métricas](../results/runs/final_A_v2_p100_u40/metrics.json) | `make -f Makefile.asic final` |
| DRC/LVS/antena/STA finales | `results/runs/final_A_v2_p100_u40/evidence/` | `scripts/archive_evidence.py` conserva los reportes del flujo |
| Ruta crítica real | [JSON](../results/timing/critical_paths.json), `results/timing/*critical*.rpt` | `scripts/extract_critical.py` |
| Frecuencia del layout fijo | `results/timing/STA_fixed_final_A_v2_p100_u40_p59.json` y `p58.json` | `scripts/fixed_layout_sta.py final_A_v2_p100_u40 59 58` |
| Comparación física A/B a 100 ns / 30 % | `results/environment/selected_b_run.json`, `results/runs/A_p100_u30_v2_resume/`, `results/runs/B_p100_u30_v2_resume_20261102T153658Z/` | [Reproducción de B](REPRODUCIR_B.md) |
| Frecuencia comparable de memorias | `results/timing/frequency_A_p100_u30_v2_resume.json`, `results/timing/frequency_B_p100_u30_v2_resume_20261102T153658Z.json` | `scripts/characterize_fixed_layout.py <corrida>` |
| Checkpoint portable y sus hashes | `results/checkpoints/B_p100_u30_v2_resume_20261102T153658Z.zip`, `results/environment/B_checkpoint_restore_verification.log` | `scripts/restore_checkpoint.py <paquete>` |
| Identidad de vistas finales y verificaciones | `results/environment/final_artifact_audit.json` | `scripts/audit_final_artifacts.py` |
| Ubicación de RF/ALU/contador | `results/layout/final_A_v2_p100_u40/cell_locations.json`, `docs/figures/` | `scripts/extract_layout.py`, `scripts/layout_capture.py`, bajo la AppImage |
| Caso DRC antes/después | [Caso medido](../results/incidents/drc_case/case.json), `docs/figures/drc_before.png`, `drc_after.png` | `scripts/prepare_drc_case.py`, `scripts/drc_case_capture.py` |
| Versiones y hashes | `results/environment/librelane_tool_versions.txt`, `results/snapshots/`, `results/runs/*/input_hashes_audited.json` | `scripts/audit_sources.py`, `scripts/hash_run_inputs.py` |
La comparación temporal usa siempre los nueve corners. Un código de salida cero
del flujo no demuestra cierre: la corrida a 50 ns conserva WNS/TNS negativos y
está clasificada como fallida. Las advertencias eléctricas de slew/fanout/capacitancia
de A se mantienen explícitas en el informe. DRC limpio se refiere a Magic/router;
no se dispone de un deck KLayout DRC configurado.

La arquitectura B seleccionada terminó DRC Magic/LVS/antena y timing en nueve
corners. Las pruebas B al 40 % se conservan como intentos incompletos, incluido
el ECO de desvío detenido cuando B30 cerró routing y antena. No se atribuye
signoff a esos intentos.
