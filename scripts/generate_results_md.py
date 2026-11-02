from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'results/summary.json').read_text())
text=['# Resultados medidos','',
      'La aprobación se determina desde métricas por corner, no desde el código de salida del comando. Las corridas v1 y v2 se distinguen por nombre; las comparaciones principales usan v2.','',
      '| Corrida | T ns | FP % | Área síntesis µm² | Die µm² | Util. ruteada antes de filler % | Setup slack ns | Hold slack ns | Cierre |',
      '|---|---:|---:|---:|---:|---:|---:|---:|---|']
for r in rows:
    f=lambda v:'No medido' if v is None else f'{v:.4f}'
    text.append(f"| {r['run']} | {r['period_ns']} | {r['util_pct']} | {f(r['synth_area_um2'])} | {f(r['die_area_um2'])} | {f(r['routed_util_before_fill_pct'])} | {f(r['worst_setup_slack_ns'])} | {f(r['worst_hold_slack_ns'])} | {'Sí' if r['closed'] else 'No'} |")
text+=['','## Congestión: primer resultado real de routing','',
       'La métrica route__drc_errors__iter:0 se sobrescribe cuando el flujo vuelve a rutear tras reparar antena. El gráfico toma el primer «Number of violations» del log completo; se conserva también la métrica cruda para auditoría.','',
       '| FP % | Primera pasada real | Métrica cruda iteración 0 |','|---:|---:|---:|']
for r in sorted((x for x in rows if x['run'] in ['A_p100_u30_v2_resume','A_v2_p100_u40','A_p100_u50_v2_recovery']),key=lambda x:x['util_pct']):
    text.append(f"| {r['util_pct']} | {r['route_initial_drc']} | {r.get('route_iteration0_metric')} |")
text+=['','Todas las cifras proceden de results/summary.json. DRC, LVS, antena y nueve corners: results/runs/<corrida>/metrics.json y corners.csv. La utilización ruteada incluye celdas añadidas por implementación, antes de llenar espacios con filler.','',
       '## Frecuencia del layout final fijo','',
       'Se mantiene el layout y los retardos externos absolutos. Esto es distinto de sintetizar y ubicar nuevamente para otro objetivo.','',
       '| Período ns | Peor setup slack ns | Nueve corners |','|---:|---:|---|']
for f in sorted((ROOT/'results/timing').glob('STA_fixed_final_A_*.json')):
    r=json.loads(f.read_text());text.append(f"| {r['period_ns']} | {min(c['setup_ws'] for c in r['corners'].values()):.6f} | {'Pasa' if r['pass_timing'] else 'Falla'} |")
text+=['','59 ns pasa y 58 ns falla: máximo observado con resolución de 1 ns, 16,949153 MHz. La corrida final de entrega utiliza 100 ns y 10 MHz.','',
       '## Límites eléctricos','',
       'El final cumple DRC Magic/LVS/antena y setup/hold, pero reporta 2.196 violaciones máximas de slew, 57 de fanout y 4 de capacitancia. No se declara cierre eléctrico completo ni preparación para fabricación.','']
selection=ROOT/'results/environment/selected_b_run.json'
if selection.exists():
    selected=json.loads(selection.read_text())
    text+=['## Comparación física de memorias bajo las mismas condiciones','',
           '| Arquitectura | Corrida | FP % | Síntesis µm² | Die µm² | Límite medido ns | MHz |','|---|---|---:|---:|---:|---:|---:|']
    for label,tag in [('A',selected['a_comparison_run']),('B',selected['run'])]:
        row=next(r for r in rows if r['run']==tag)
        frequency=json.loads((ROOT/f'results/timing/frequency_{tag}.json').read_text())
        text.append(f"| {label} | {tag} | {row['util_pct']} | {row['synth_area_um2']:.4f} | {row['die_area_um2']:.0f} | {frequency.get('minimum_passing_period_ns','No cerrado')} | {frequency.get('frequency_mhz','No cerrado')} |")
    text+=['','Ambas implementaciones usan 100 ns, 30 % inicial, seis threads y routing predeterminado. El límite de frecuencia se mide con layout fijo y resolución de 1 ns; no es un PnR nuevo. El final obligatorio de A permanece a 100 ns / 40 %.','',
           'B conserva 15.634 violaciones máximas de slew, 291 de fanout y 1.923 de capacitancia. Sus criterios explícitos de DRC Magic/LVS/antena y setup/hold están cumplidos; no tiene cierre eléctrico completo. Ver final_artifact_audit.json y REPRODUCIR_B.md.','']
(ROOT/'docs/RESULTADOS_MEDIDOS.md').write_text('\n'.join(text),encoding='utf-8')
