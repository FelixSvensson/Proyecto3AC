# Resultados medidos

La aprobación se determina desde métricas por corner, no desde el código de salida del comando. Las corridas v1 y v2 se distinguen por nombre; las comparaciones principales usan v2.

| Corrida | T ns | FP % | Área síntesis µm² | Die µm² | Util. ruteada antes de filler % | Setup slack ns | Hold slack ns | Cierre |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| A_gf180_p100_u40 | 100 | 40 | 147128.8896 | 395416.0000 | 51.9187 | 40.9986 | 0.1270 | Sí |
| A_opt_v2_p100_u40 | 100 | 40 | 158194.8928 | 424085.0000 | 51.4776 | 41.2458 | 0.1673 | Sí |
| A_p100_u30_v2_resume | 100 | 30 | 154474.0288 | 547483.0000 | 39.2346 | 43.3154 | 0.1292 | Sí |
| A_p100_u50_v2_recovery | 100 | 50 | 154474.0288 | 334270.0000 | 63.6718 | 38.4554 | 0.1329 | Sí |
| A_p50_u40_v2_20261028T174610Z | 50 | 40 | 154474.0288 | 414450.0000 | 51.3834 | -8.8681 | 0.1205 | No |
| A_p60_u40_v2_20261028T152420Z | 60 | 40 | 154474.0288 | 414450.0000 | 51.3834 | 1.1319 | 0.1205 | Sí |
| A_p80_u40_v2_20261028T150844Z | 80 | 40 | 154474.0288 | 414450.0000 | 51.3834 | 21.1319 | 0.1205 | Sí |
| A_v2_p100_u40 | 100 | 40 | 154474.0288 | 414450.0000 | 51.3834 | 41.1319 | 0.1205 | Sí |
| B_p100_u30_v2_resume_20261102T153658Z | 100 | 30 | 628066.4768 | 2158790.0000 | 41.4917 | 9.6662 | 0.1197 | Sí |
| final_A_v2_p100_u40 | 100 | 40 | 154474.0288 | 414450.0000 | 51.6665 | 41.4596 | 0.1074 | Sí |

## Congestión: primer resultado real de routing

La métrica route__drc_errors__iter:0 se sobrescribe cuando el flujo vuelve a rutear tras reparar antena. El gráfico toma el primer «Number of violations» del log completo; se conserva también la métrica cruda para auditoría.

| FP % | Primera pasada real | Métrica cruda iteración 0 |
|---:|---:|---:|
| 30 | 1764 | 139 |
| 40 | 2026 | 4 |
| 50 | 3061 | 3061 |

Todas las cifras proceden de results/summary.json. DRC, LVS, antena y nueve corners: results/runs/<corrida>/metrics.json y corners.csv. La utilización ruteada incluye celdas añadidas por implementación, antes de llenar espacios con filler.

## Frecuencia del layout final fijo

Se mantiene el layout y los retardos externos absolutos. Esto es distinto de sintetizar y ubicar nuevamente para otro objetivo.

| Período ns | Peor setup slack ns | Nueve corners |
|---:|---:|---|
| 58.0 | -0.540378 | Falla |
| 59.0 | 0.459622 | Pasa |

59 ns pasa y 58 ns falla: máximo observado con resolución de 1 ns, 16,949153 MHz. La corrida final de entrega utiliza 100 ns y 10 MHz.

## Límites eléctricos

El final cumple DRC Magic/LVS/antena y setup/hold, pero reporta 2.196 violaciones máximas de slew, 57 de fanout y 4 de capacitancia. No se declara cierre eléctrico completo ni preparación para fabricación.

## Comparación física de memorias bajo las mismas condiciones

| Arquitectura | Corrida | FP % | Síntesis µm² | Die µm² | Límite medido ns | MHz |
|---|---|---:|---:|---:|---:|---:|
| A | A_p100_u30_v2_resume | 30 | 154474.0288 | 547483 | 57 | 17.54385964912281 |
| B | B_p100_u30_v2_resume_20261102T153658Z | 30 | 628066.4768 | 2158790 | 91 | 10.989010989010989 |

Ambas implementaciones usan 100 ns, 30 % inicial, seis threads y routing predeterminado. El límite de frecuencia se mide con layout fijo y resolución de 1 ns; no es un PnR nuevo. El final obligatorio de A permanece a 100 ns / 40 %.

B conserva 15.634 violaciones máximas de slew, 291 de fanout y 1.923 de capacitancia. Sus criterios explícitos de DRC Magic/LVS/antena y setup/hold están cumplidos; no tiene cierre eléctrico completo. Ver final_artifact_audit.json y REPRODUCIR_B.md.
