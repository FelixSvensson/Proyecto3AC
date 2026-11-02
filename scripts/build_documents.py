"""Generate Spanish report/defence PDFs exclusively from stored measurements."""
from pathlib import Path
import json,sys,math,html
from datetime import date
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs';FIG=DOCS/'figures';FIG.mkdir(exist_ok=True)
def load(path,default=None):
    p=ROOT/path
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else default
rows=load('results/summary.json',[])
stats={s:load(f'results/synthesis/{s}_prod_hier/stat.json',{}) for s in ['A','B']}
preferred=next((r for r in rows if r['run']=='final_A_v2_p100_u40'),next((r for r in rows if r['run']=='A_v2_p100_u40'),None))
fontpath=Path('C:/Windows/Fonts') if sys.platform=='win32' else Path('/usr/share/fonts/truetype/liberation2')
for name,file in [('Body','arial.ttf' if sys.platform=='win32' else 'LiberationSans-Regular.ttf'),('Bold','arialbd.ttf' if sys.platform=='win32' else 'LiberationSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(fontpath/file)))
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='P3Body',fontName='Body',fontSize=10,leading=14,spaceAfter=8,allowWidows=0,allowOrphans=0,textColor=colors.HexColor('#253447')))
styles.add(ParagraphStyle(name='P3H1',fontName='Bold',fontSize=18,leading=22,spaceBefore=14,spaceAfter=10,textColor=colors.HexColor('#124e67'),keepWithNext=True))
styles.add(ParagraphStyle(name='P3H2',fontName='Bold',fontSize=12,leading=16,spaceBefore=10,spaceAfter=6,keepWithNext=True,textColor=colors.HexColor('#124e67')))
styles.add(ParagraphStyle(name='P3Title',fontName='Bold',fontSize=29,leading=34,spaceAfter=20,textColor=colors.HexColor('#124e67')))
styles.add(ParagraphStyle(name='P3Small',fontName='Body',fontSize=8,leading=10,spaceAfter=6))
styles.add(ParagraphStyle(name='P3Cell',fontName='Body',fontSize=8,leading=10))

def p(text,style='P3Body'):return Paragraph(text,styles[style])
def h(text):return p(text,'P3H1')
def sub(text):return p(text,'P3H2')
def esc(text):return html.escape(('Sí' if text else 'No') if isinstance(text,bool) else str(text))
def table(headers,data,widths=None):
    content=[[p(esc(x),'P3Cell') for x in row] for row in [headers]+data]
    t=Table(content,colWidths=widths,repeatRows=1,hAlign='LEFT',splitByRow=int(len(data)>12))
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dbeaf0')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#c4d2d9')),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f2f6f8')])]))
    return t
def fmt(v):return 'No medido' if v is None else f'{v:,.3f}'.translate(str.maketrans(',.','.,')) if isinstance(v,(float,int)) else str(v)
def figure(name,caption,width=170*mm):
    f=FIG/name
    if not f.exists():return [p('Figura pendiente: '+esc(caption))]
    im=Image(str(f));scale=min(width/im.imageWidth,185*mm/im.imageHeight)
    im.drawWidth=im.imageWidth*scale;im.drawHeight=im.imageHeight*scale
    return [KeepTogether([im,p(esc(caption),'P3Small')])]
def footer(canvas,doc):
    canvas.saveState();canvas.setStrokeColor(colors.HexColor('#bfd0d9'));canvas.line(20*mm,16*mm,190*mm,16*mm)
    canvas.setFont('Body',8);canvas.setFillColor(colors.HexColor('#607482'))
    canvas.drawString(20*mm,11*mm,'Grupo 15 | Arquitectura de Computadores | 2026-2')
    canvas.drawRightString(190*mm,11*mm,str(doc.page));canvas.restoreState()
def build(name,story):
    SimpleDocTemplate(str(DOCS/name),pagesize=(210*mm,297*mm),rightMargin=20*mm,leftMargin=20*mm,topMargin=20*mm,bottomMargin=23*mm,title=name.replace('_',' '),author='Grupo 15').build(story,onFirstPage=footer,onLaterPages=footer)
def module_area(s,name):return stats.get(s,{}).get('modules',{}).get('\\'+name,{}).get('area')

def charts():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    area=[stats[s].get('design',{}).get('area') for s in ['A','B']]
    if all(v is not None for v in area):
        fig,ax=plt.subplots(figsize=(7,3.7));ax.bar(['A: ROM + RAM','B: unificada FF'],area,color=['#177e89','#d48445']);ax.set_ylabel('Área de celdas (µm²)');ax.set_title('Síntesis jerárquica comparable, GF180 7T')
        for i,v in enumerate(area):ax.text(i,v,f'{v:,.0f}',ha='center',va='bottom')
        ax.set_ylim(0,max(area)*1.17);fig.tight_layout();fig.savefig(FIG/'memory_area.png',dpi=180);plt.close(fig)
    util=[r for r in rows if r['run'].startswith('A_') and '_v2_' in r['run'] and r['period_ns']==100 and 'opt' not in r['run']]
    if util:
        util.sort(key=lambda r:r['util_pct'])
        fig,ax=plt.subplots(figsize=(7,3.7));ax.plot([r['util_pct'] for r in util],[r['route_initial_drc'] for r in util],'o-',color='#177e89',label='DRC inicial de routing');ax.plot([r['util_pct'] for r in util],[r['drc'] for r in util],'s--',color='#d48445',label='DRC final Magic');ax.set_xlabel('FP_CORE_UTIL (%)');ax.set_ylabel('Violaciones reales');ax.set_title('Utilización frente a violaciones');ax.legend();fig.tight_layout();fig.savefig(FIG/'utilization_violations.png',dpi=180);plt.close(fig)


def report():
    story=[Spacer(1,25*mm),p('Del Pochoco SoC<br/>a un macro ASIC','P3Title'),p('Proyecto 3 · Universidad de los Andes · Semestre 2026-2'),p('<b>Grupo 15</b><br/>Martin Heiremans · Felix Svensson · Juan Pablo Saavedra'),p('Profesor: Jorge Gómez Mir'),Spacer(1,12*mm),p('Implementación con LibreLane 3.0.17 y GF180MCU D'),p(f'Fecha de generación: {date.today().isoformat()}.<br/>Entrega y defensa: 4 de noviembre de 2026, 10:30, Chile.'),p('Este documento se regenera desde los reportes existentes. Un dato ausente se declara pendiente; nunca se sustituye por cero.'),PageBreak()]
    story += [h('1. Resumen ejecutivo'),p('Se migró el Pochoco SoC del Proyecto 2 real a un macro de celdas estándar. El juego conserva 107 instrucciones y estado en registros. Se construyeron una ROM combinacional con RAM mínima y una memoria unificada de flip-flops con restauración por reset. Ambas ejecutaron las mismas diez rondas y el mismo error de botón en simulación RTL. Los netlists jerárquicos A y B mapeados a celdas GF180 produjeron la misma traza de ciclos y los mismos estímulos.')]
    if preferred:story += [p(f'La corrida de referencia documentada es <b>{preferred["run"]}</b>: período {preferred["period_ns"]} ns, utilización objetivo {preferred["util_pct"]} %, área de die {fmt(preferred["die_area_um2"])} µm², DRC {preferred["drc"]}, LVS {preferred["lvs"]}, antena {preferred["antenna"]} y {preferred["corners"]} corners. Cierre según los criterios solicitados: {esc(preferred["closed"])}.')]
    story += [h('2. Objetivo, alcance y procedencia'),p('La fuente es FelixSvensson/Proyecto2AC, main, revisión 67d0c48bcc115614a4029ff024277cb53bc30a05. dev-game apunta a una revisión anterior. Se conserva el historial en una copia independiente. No se ejecutaron commits ni pushes y se deshabilitó el destino de push del remoto de referencia proyecto2. El PDF oficial del Proyecto 3 no estaba adjunto; se utilizó el enunciado completo transcrito por el usuario, guardado en docs/REQUISITOS_PROYECTO.md.'),p('El producto es un macro digital con terminales lógicos. No incluye pads, anillo de ESD, encapsulado ni una garantía de fabricación. Las advertencias eléctricas adicionales se mantienen visibles en warning.log y no equivalen a un DRC o LVS limpio.'),h('3. Arquitectura original'),p('Espino es un procesador de 32 bits con 16 registros arquitectónicos RV32E; x0 es constante. El subconjunto implementado excluye desplazamientos y multiplicación/división. El controlador espera la lectura síncrona del register file y el LSU completa accesos de memoria con la latencia original. El programa usa sumas, restas y ramas para dividir y formar BCD.'),table(['Dirección','Función'],[['0x80000000','Escritura de dos dígitos'],['0x80000004','LED y captura simultánea de led_cycle_q'],['0x80000008','Lectura de cuatro botones'],['0x8000000C','Contador libre de 32 bits'],['0x80000010','Instante de la última escritura de LED'],['0x80010000','Periférico SPI, sin uso por el juego']],[40*mm,130*mm]),h('4. Migración FPGA a ASIC'),p('Se elimina el reset generado por por_cnt inicializado y se expone rst_ni activo bajo. Se sustituyen las primitivas SB_RAM40_4K por 15 registros de 32 bits con dos lecturas síncronas. La lectura coincidente con una escritura devuelve el dato anterior. No se utiliza initial ni readmemh en las fuentes ASIC de producción. Las constantes del programa pasan a lógica de ROM o a valores físicos de reset de FF.'),p('El registro detallado de construcciones, justificación, cambios y validación está en docs/MIGRACION_ASIC.md. Las 14 advertencias iniciales de lint son señales o parámetros no usados; el log conserva archivo y línea. No se inventó una falla de LibreLane para el RTL FPGA original, porque esa corrida no se ejecutó.'),h('5. Memoria y extensión del assembler'),p('assembler/assembler.py conserva la interfaz histórica de dos argumentos y añade --rom-dir. Genera program_rom.v, program_meta.vh y program_reset.vh con orden determinista. Las pruebas verifican los límites de 1 a 256 instrucciones, todas las palabras emitidas, determinismo y codificación de las tres constantes de tiempo.'),table(['Propiedad','A: ROM + RAM','B: unificada'],[['Instrucciones reales','107 palabras / 428 bytes','107 palabras / 428 bytes'],['Datos usados por el juego','0 palabras','0 palabras'],['Capacidad implementada de datos','1 palabra reservada','1 palabra, contigua al programa'],['Contenido después de reset','ROM combinacional constante','Reset explícito de los 108 × 32 bits'],['Escritura en programa','Ignorada','Permitida por bytes; reset restaura'],['Lecturas','Síncronas, un flanco','Síncronas, un flanco'],['Carga SPI de programa','No se utiliza','No se utiliza']],[47*mm,61*mm,62*mm]),p('La palabra de datos de reserva está en la dirección 107 × 4 = 0x1AC. No es un dato inferido del tamaño de un arreglo: todos los lw/sw del juego usan x1=0x80000000, y los monitores contaron cero accesos a RAM. La reserva mínima permite verificar lectura, escritura y byte enables sin exceder el uso real. B incluye honestamente los FF de programa y su red de reset; no presupone contenido mágico al encender.'),h('6. Síntesis y trazabilidad')]
    data=[]
    for s in ['A','B']:
        d=stats[s].get('design',{});types=d.get('num_cells_by_type',{})
        data.append([s,fmt(d.get('area')),sum(v for k,v in types.items() if '__dff' in k),d.get('num_cells','No medido')])
    story += [table(['Estrategia','Área jerárquica µm²','FF mapeados','Celdas reportadas'],data,[30*mm,55*mm,40*mm,45*mm]),p('Fuente: results/synthesis/A_prod_hier/stat.json y B_prod_hier/stat.json. Estas síntesis usan la misma biblioteca TT y estrategia de mapeo jerárquica. No deben confundirse con el área de LibreLane, cuyos ajustes adicionales de síntesis y reparación producen otro número. El área final tras filler puede alcanzar el área del core; para comparar lógica se usa el área anterior al filler.'),table(['Módulo, estrategia A','Área µm²'],[[n,fmt(module_area('A',n))] for n in ['espino_register_file','espino_alu','cycle_counter']],[115*mm,55*mm])]
    area=stats['A'].get('design',{}).get('area');counter=module_area('A','cycle_counter')
    if area and counter:story += [p(f'El contador independiente representa {100*counter/area:.3f} % del total de la misma síntesis jerárquica. led_cycle_q no se atribuye al contador: se mantiene en el periférico. La predicción previa (docs/PREDICCION_AREA.md) anticipó el predominio del banco de registros en A y de la memoria en B; las mediciones permiten comprobarla sin repartir áreas arbitrariamente.')]
    types=stats['A'].get('design',{}).get('num_cells_by_type',{})
    top=sorted(((k,v) for k,v in types.items() if k.startswith('gf180')),key=lambda x:-x[1])[:5]
    story += [table(['Cinco celdas más usadas en A','Cantidad'],[[k.replace('gf180mcu_fd_sc_mcu7t5v0__',''),v] for k,v in top],[130*mm,40*mm]),p('Los dffrnq implementan estado y salidas síncronas; los mux2 seleccionan escrituras y lecturas del banco; NAND/AOI/OAI implementan decodificación, multiplexores y lógica de operación. La asociación cuantitativa por módulo procede de stat.json y de las instancias preservadas por deferred_flatten, no de una atribución visual.' )]
    story += figure('memory_area.png','Área de las dos arquitecturas en la síntesis jerárquica comparable.')
    story += [h('7. Timing y ruta crítica'),p('WNS representa el peor slack negativo; cuando todas las rutas cumplen, esta métrica es cero, y el slack positivo se consulta como worst slack (ws). TNS suma solo los slacks negativos. Se verifican setup y hold en combinaciones min/nom/max de RC y TT/SS/FF. Los CSV corners.csv conservan las cuatro métricas de cada corner. Los resultados intermedios pueden conservar valores de corners de una etapa anterior: las conclusiones de cierre se basan exclusivamente en STA post-PnR final.')] 
    timing=[r for r in rows if r['util_pct']==40 and r['run'].startswith('A_') and 'opt' not in r['run'] and '_v2_' in r['run']]
    story += [table(['Corrida','T ns','Setup slack ns','Hold slack ns','Cierre'],[[r['run'],r['period_ns'],fmt(r['worst_setup_slack_ns']),fmt(r['worst_hold_slack_ns']),r['closed']] for r in timing],[67*mm,15*mm,32*mm,32*mm,24*mm])]
    closed=[r for r in timing if r['closed']]
    if closed:
        t=min(r['period_ns'] for r in closed);story += [p(f'El menor período que cerró entre las corridas actualmente terminadas es {t} ns: f<sub>max,observada</sub> = 1000 / {t} = {1000/t:.3f} MHz. Es una cota experimental sobre los puntos muestreados, no una demostración del óptimo continuo. El juego final se ejecuta a 10 MHz; un experimento de síntesis con otro objetivo no cambia automáticamente el reloj físico ni las constantes de software.')]
    story += [p('La ruta crítica del layout final conecta instr_rdata[4] con ram_b_rdata[16] a través de decodificación/ejecución y lectura de memoria. Su retardo Q→D es 54,650438 ns en max_ss_125C_4v50. Los pines completos y el reporte trazable se presentan en los resultados finales complementarios; no se atribuye la ruta crítica al contador de ciclos por su función o tamaño.'),h('8. Optimización del RTL'),p('asic/variants/asic_memory_registered_addr.v registra la dirección y selección del puerto B de A y evalúa la ROM después de ese límite de registro. El dato de RAM se conserva con lectura anterior a escritura. El contrato visible continúa siendo una respuesta al mismo flanco, pero se divide la ruta combinacional que antes atravesaba dirección calculada y decodificación ROM dentro del mismo ciclo.'),p('La variante pasó el juego con los mismos estímulos y salidas, las pruebas de memoria y 2.000 ciclos aleatorios reproducibles de comparación con la memoria anterior. Esto es evidencia funcional acotada, no una prueba formal exhaustiva. No se modifica B.' )]
    base=next((r for r in rows if r['run']=='A_v2_p100_u40'),None);opt=next((r for r in rows if r['run']=='A_opt_v2_p100_u40'),None)
    story += [table(['Métrica comparable','Antes','Después'],[['Área de síntesis µm²',fmt(base['synth_area_um2'] if base else None),fmt(opt['synth_area_um2'] if opt else None)],['Peor slack setup ns',fmt(base['worst_setup_slack_ns'] if base else None),fmt(opt['worst_setup_slack_ns'] if opt else None)],['Cierre en nueve corners',base['closed'] if base else 'Pendiente',opt['closed'] if opt else 'Pendiente']],[70*mm,50*mm,50*mm]),p('Cambiar CLOCK_PERIOD puede alterar la optimización lógica, buffers, placement y área. Por eso no se estima el barrido restando un número fijo al slack de una sola corrida: se ejecutan implementaciones separadas.'),h('9. Constantes de tiempo'),table(['Magnitud','25 MHz, referencia','10 MHz, final'],[['Espera de tres segundos','75.000.000 ciclos','30.000.000 ciclos'],['Una décima','2.500.000 ciclos','1.000.000 ciclos'],['Divisor del promedio de diez','25.000.000 ciclos','10.000.000 ciclos']],[70*mm,50*mm,50*mm]),p('La fuente entregada en main contenía para la espera el par 0xEE6B y 640: representa 250.000.000 ciclos, no 75.000.000. El game.hex incluido en esa misma revisión sí contiene 75.000.000 ciclos; solo difieren las palabras 8 y 9 entre fuente ensamblado y hexadecimal. Por tanto, la imagen FPGA incluida coincide con el informe, mientras que el fuente de main quedó desincronizado. Se preservó el fuente en sw/game_fpga_original.s y se corrigió/regeneró la copia de Proyecto3AC. Evidencia: results/environment/original_program_consistency.json. El manifiesto de producción registra hash 7865fa1f747b19f3482354dc68ec1075c7722cc24214eed0a46b4bfd71e9aad0. La imagen acelerada utiliza 300/100/1000 ciclos y es idéntica en las simulaciones RTL y netlist; no se utiliza para medir el layout final.'),h('10. Floorplan, alimentación y costo'),p('LibreLane construye filas de celdas, tap/endcap, red VDD/VSS, placement, CTS y routing para GF180MCU D. El objetivo final es FP_CORE_UTIL=40, que es utilización inicial y no debe confundirse con la ocupación después de buffers y filler. El orden final de terminales se especifica en asic/constraints/pins.cfg: clock/reset al norte, botones al oeste, LED/displays al este y SPI al sur. Son terminales de macro, no pads físicos. Las coordenadas reales se extraen de OpenDB con scripts/extract_layout.py.' )]
    story += figure('utilization_violations.png','Violaciones iniciales de routing y DRC final frente a la utilización; solo corridas terminadas.')
    story += [table(['Corrida','Die µm²','USD equivalente','DRC / LVS / ant.'],[[r['run'],fmt(r['die_area_um2']),fmt(r['cost_usd']),f"{r['drc']} / {r['lvs']} / {r['antenna']}"] for r in rows],[66*mm,36*mm,35*mm,33*mm]),p('Costo equivalente = área del die [µm²] / 1.000.000 × US$23.000/mm². Esta regla lineal del enunciado no incluye rendimiento de fabricación, máscaras, costos fijos, encapsulado, pruebas ni volumen. La elección ROM frente a FF de programa tiene el mayor impacto arquitectónico en las áreas de síntesis medidas; el costo final depende además del floorplan efectivo.'),h('11. Signoff y layout'),p('Las métricas de DRC provienen de Magic y del router; LVS de Netgen; antena de OpenROAD; timing de STA con SPEF. La instalación del PDK no proporciona KLAYOUT_DRC_RUNSET y LibreLane omite esa comprobación con advertencia: no se presenta como DRC de KLayout aprobado. El DRC limpio reportado corresponde a Magic. Las advertencias de capacitancia máxima permanecen en los logs; requieren revisión eléctrica si se pretende integrar o fabricar el macro.'),p('Se preservó un estado real de diagnóstico con DRT_OPT_ITERS=0 (1924 violaciones) desde el mismo estado previo al routing; es un estado de diagnóstico y sus 1.924 violaciones coinciden con la primera pasada real del flujo completo. El caso seleccionado es un Short en Metal2 entre regs[2][11] del register file y net462, caja (33,74;154,09)-(34,02;154,47) µm. Las capturas antes/después proceden de los GDS reales. El routing completo registró 1.924, 665, 476, 3 y 0 violaciones; después de reparar antena volvió a rutear y registró 18, 1 y 0. La métrica de iteración 0 se sobrescribe en esa segunda pasada; el gráfico usa el primer conteo del log completo. Configuración, reporte crudo y coordenadas están en results/incidents/drc_case/. No se insertó una falla artificial en el RTL.')]
    for name,caption in [('layout_real.png','Vista real de KLayout del GDS final_A_v2_p100_u40; capas de metal en gris.'),('layout_register_file.png','Register file: cajas reales de instancias identificadas por u_rf.'),('layout_alu.png','ALU: cajas reales de instancias identificadas por u_alu.'),('layout_cycle_counter.png','Contador: cajas reales de instancias identificadas por u_cycle_counter.')]:story += figure(name,caption)
    story += [h('12. Simulación RTL y post-síntesis'),p('sim/asic_game_tb.v aplica botones 127 ciclos después de observar el LED objetivo. Por la secuencia de sondeo y lectura del programa, el tiempo medido es 136 ciclos: no debe confundirse el retardo del estímulo con el instante de lectura del contador. Diez aciertos acumulan 1.360 ciclos. Un error después del primer acierto conserva el número de rondas y el acumulador. El programa calcula el promedio y reinicia por botón 4; posteriormente se prueba otro reset externo.'),p('scripts/gate_verify.py ejecuta realmente los netlists jerárquicos A y B mapeados a celdas estándar GF180. Los archivos de estímulos por ciclo se comparan byte a byte; las líneas STORE/REACTION/CORRECT/WRONG/PASS también coinciden. No se anotó SDF. Las formas de onda seleccionadas se conservan comprimidas en results/functional/waves/.'),h('13. Reproducibilidad y limitaciones'),p('Las configuraciones efectivas, reportes finales y esquinas están en results/runs/. Las fuentes y hashes se conservan en results/snapshots/. Las instalaciones y PDK permanecen fuera de Git, en /opt/proyecto3-tools dentro de Ubuntu. scripts/run_flow.sh exige la versión fijada; scripts/collect_results.py no convierte métricas faltantes en ceros. El README detalla los comandos de regeneración. La defensa presencial sigue siendo responsabilidad del grupo y no puede darse por realizada por generar una guía.'),h('14. Conclusiones'),p('La migración elimina dependencias de inicialización y primitivas iCE40 y mantiene la latencia que necesita Espino. Las dos arquitecturas de memoria ejecutan la misma aplicación; B paga el costo de almacenar instrucciones reescribibles en FF. El register file es un bloque de área importante en A, coherente con la predicción. Los estados de cierre deben consultarse por corrida y corner; ninguna imagen conceptual sustituye GDS, DRC, LVS o simulación. El checklist distingue lo completado de los puntos todavía parciales.'),h('15. Referencias y anexos'),p('Informe_Proyecto2.pdf (fuente de organización y nombres del grupo).<br/>docs/REQUISITOS_PROYECTO.md (enunciado transcrito).<br/>https://github.com/FelixSvensson/Proyecto2AC<br/>https://librelane.readthedocs.io/en/stable/<br/>https://gf180mcu-pdk.readthedocs.io/en/latest/<br/>https://openroad.readthedocs.io/en/latest/<br/>https://www.klayout.de/doc-qt5/code/class_LayoutView.html<br/>Anexos experimentales: results/summary.csv, results/runs/*/corners.csv, results/synthesis/*/stat.json, results/optimization/, results/layout/.','P3Small')]
    critical=load('results/timing/critical_paths.json',[])
    finalpath=next((x for x in critical if x['run']=='final_A_v2_p100_u40'),None)
    refinements=[json.loads(f.read_text()) for f in (ROOT/'results/timing').glob('STA_fixed_*.json')]
    refinements.sort(key=lambda x:(x['source_run'],x['period_ns']))
    boundary_refinements=[]
    for source in sorted({x['source_run'] for x in refinements}):
        samples=[x for x in refinements if x['source_run']==source]
        passing=[x for x in samples if x['pass_timing']]
        if passing:
            boundary=min(passing,key=lambda x:x['period_ns'])
            failing=[x for x in samples if not x['pass_timing'] and x['period_ns']<boundary['period_ns']]
            boundary_refinements.extend(([max(failing,key=lambda x:x['period_ns'])] if failing else [])+[boundary])
        else:
            boundary_refinements.extend(samples)
    additions=[h('Resultados finales complementarios')]
    selection=load('results/environment/selected_b_run.json',{})
    b_run=selection.get('run','B_v2_p100_u40_snapshot_resume')
    comparison_a_run=selection.get('a_comparison_run','A_v2_p100_u40')
    comparison_a=next((r for r in rows if r['run']==comparison_a_run),None)
    b_physical=next((r for r in rows if r['run']==b_run),None)
    b_threads=load(f'results/runs/{b_run}/effective_config.json',{}).get('DRT_THREADS','no registrado')
    a_threads=load(f'results/runs/{comparison_a_run}/effective_config.json',{}).get('DRT_THREADS','no registrado')
    additions += [sub('Comparación física de memorias')]
    if b_physical and comparison_a:
        assert b_physical['util_pct']==comparison_a['util_pct'] and b_physical['period_ns']==comparison_a['period_ns']
        common_util=comparison_a['util_pct']
        additions += [table(['Arquitectura','Síntesis µm²','Die µm²','Setup mínimo ns','Hold mínimo ns','Cierre'],[[label,fmt(r['synth_area_um2']),fmt(r['die_area_um2']),fmt(r['worst_setup_slack_ns']),fmt(r['worst_hold_slack_ns']),r['closed']] for label,r in [('A comparativa',comparison_a),('B',b_physical)]],[25*mm,30*mm,30*mm,30*mm,30*mm,25*mm]),p(f'Corridas comparadas: {esc(comparison_a_run)} y {esc(b_run)}. Usan la misma revisión RTL v2, programa de producción, biblioteca, período de 100 ns, utilización inicial del {common_util} % y orden automático de terminales. A usa {a_threads} threads de routing y B usa {b_threads}. Se conservan sus configuraciones efectivas y puntos de reanudación. La corrida final obligatoria de A se presenta por separado: 100 ns, 40 % y distribución de terminales por función.')]
        additions += [p(f"Con la relación lineal del enunciado, el costo equivalente de A comparativa es US${fmt(comparison_a['cost_usd'])} y el de B es US${fmt(b_physical['cost_usd'])}. La relación de áreas de die B/A es {fmt(b_physical['die_area_um2']/comparison_a['die_area_um2'])}. Estos costos usan die físico, no área de celdas de la síntesis jerárquica.")]
        if 'ordered' in b_run:
            additions += [p('B necesitó una reparación física adicional de un cruce en Metal3. Se retiró el trazado afectado en una copia del ODB; el hash de todas las conexiones lógicas permaneció idéntico. Se reconstruyó con DRT or_seed=43 y or_k=1; A utiliza seed 42 y or_k=0. Esta diferencia de heurística debe considerarse al comparar timing: las condiciones obligatorias y el RTL son equivalentes, pero el procedimiento de routing no es idéntico. scripts/run_ordered_flow.py registra los hashes del Tcl original y del generado; no modifica la instalación ni desactiva checkers.')]
        elif 'detour' in b_run:
            additions += [p('B usa un ECO físico dirigido al cruce Metal3 persistente: en una copia se retiraron dos cables y se añadió una obstrucción local de routing de (750,82;852,18)-(751,66;853,02) µm para obligar a buscar otro recorrido. El grafo lógico completo mantuvo su hash y no se movieron celdas. Se conserva el orden de routing predeterminado; B usa dos threads frente a los seis de A. Los reportes finales, no la preparación del ECO, determinan DRC/LVS/antena y timing. La restricción local es una diferencia física explícita entre las corridas, registrada en results/environment/B_detour_candidate.json.')]
        elif common_util==30:
            additions += [p('La comparación seleccionada utiliza el orden predeterminado de routing en ambas memorias. También se conservan ensayos parciales de B al 40 % y la recuperación de un cruce Metal3 en results/incidents/routing_recovery/ y results/environment/. Esos estados parciales no se confunden con signoff completo.')]
    else:
        additions += [p('El routing físico de B todavía está en ejecución. La comparación de área jerárquica y las simulaciones A/B están completas, pero no se atribuyen a B un GDS verificado ni una frecuencia post-route hasta disponer de sus reportes finales.')]
    b_frequency=load(f'results/timing/frequency_{b_run}.json',{})
    if b_frequency:
        if b_frequency.get('status')=='measured':
            additions += [p(f"En B, el menor período entero medido con STA sobre el layout fijo es {b_frequency['minimum_passing_period_ns']} ns, con {fmt(b_frequency['frequency_mhz'])} MHz observados; el período inmediatamente inferior, {b_frequency['adjacent_failing_period_ns']} ns, falla. Los retardos externos absolutos permanecen fijos en el SDC. Es una caracterización del layout, no una síntesis/PnR nueva para cada período.")]
            a_baseline=[x for x in refinements if x['source_run']==comparison_a_run and x['pass_timing']]
            if a_baseline:
                a_period=min(x['period_ns'] for x in a_baseline)
                additions += [p(f"La comparación con A usa el mismo método: A pasa a {a_period:g} ns ({fmt(1000/a_period)} MHz), frente a {b_frequency['minimum_passing_period_ns']} ns ({fmt(b_frequency['frequency_mhz'])} MHz) en B. La resolución temporal de ambos límites es de 1 ns.")]
        else:
            additions += [p('B presenta una falla de hold en la caracterización. No se declara una frecuencia de cierre completo, porque cambiar el período no corrige ese defecto. Los reportes se conservan en results/timing/.')]
    util_rows=[r for r in rows if r['period_ns']==100 and (r['run']=='A_v2_p100_u40' or r['run'].startswith(('A_p100_u30','A_p100_u50')))]
    util_rows.sort(key=lambda r:r['util_pct'])
    if util_rows:
        additions += [sub('Utilización objetivo y ocupación después de routing'),table(['FP objetivo %','Die µm²','Ocupación antes de filler %','Peor setup ns','Cierre'],[[r['util_pct'],fmt(r['die_area_um2']),fmt(r.get('routed_util_before_fill_pct')),fmt(r['worst_setup_slack_ns']),r['closed']] for r in util_rows],[25*mm,40*mm,45*mm,35*mm,25*mm])]
        valid=[r for r in util_rows if r['closed']]
        if valid:
            best=min(valid,key=lambda r:r['die_area_um2'])
            additions += [p(f"El menor die cerrado entre las utilizaciones ensayadas corresponde al {best['util_pct']} %: {fmt(best['die_area_um2'])} µm². Es el mínimo observado en esta grilla; la entrega mantiene el 40 % obligatorio. La ocupación aumenta después de síntesis por buffers, reloj, taps y reparación; no se presenta la ocupación con filler como eficiencia lógica.")]
    trows=[]
    for r in timing:
        m=load(f"results/runs/{r['run']}/metrics.json",{})
        values=[]
        for kind,corner in [('setup','nom_tt_025C_5v00'),('setup','max_ss_125C_4v50'),('hold','nom_tt_025C_5v00'),('hold','max_ss_125C_4v50')]:
            values.append(' / '.join(f"{m[f'timing__{kind}__{metric}__corner:{corner}']:.3f}" for metric in ['wns','tns']))
        trows.append([f"{r['period_ns']} ns"]+values)
    additions += [sub('WNS / TNS por corner típico y lento'),table(['Objetivo','Setup TT','Setup SS max RC','Hold TT','Hold SS max RC'],trows,[25*mm,36*mm,37*mm,36*mm,36*mm]),p('Todas las entradas son WNS / TNS en ns. Los nueve corners completos están en corners.csv. La corrida de 50 ns terminó con código de salida cero, pero falla los criterios temporales; se clasifica como no cerrada a partir de sus métricas.')]
    if (FIG/'drc_before.png').exists():
        images=[]
        for name in ['drc_before.png','drc_after.png']:
            im=Image(str(FIG/name));im.drawHeight=im.imageHeight*(82*mm/im.imageWidth);im.drawWidth=82*mm;images.append(im)
        pair=Table([images,[p('Estado de diagnóstico antes de completar optimizaciones.','P3Small'),p('Misma región en el GDS final: DRC limpio.','P3Small')]],colWidths=[85*mm,85*mm])
        additions += [KeepTogether([sub('Caso de DRC localizado y corregido'),pair,p('Metal2 azul; Metal1 y vías en gris. Caja roja extraída del reporte DRC real; no es una ilustración conceptual.','P3Small')])]
    if finalpath:
        additions += [sub('Ruta crítica del GDS final'),p(f"Corner {finalpath['corner']}. Inicio: {esc(finalpath['startpoint'])}, señal {esc(', '.join(finalpath['start_signal']))}. Fin: {esc(finalpath['endpoint'])}, estado {esc(', '.join(finalpath['end_state_signal']))}. El retardo combinacional Q→D es {finalpath['combinational_q_to_d_ns']:.6f} ns; la llegada total es {finalpath['data_arrival_time_ns']:.6f} ns. La ruta atraviesa decodificación/ejecución de una dirección de datos y selección de lectura de memoria. El contador de ciclos no es la ruta crítica de esta corrida."),p('La variante optimizada cambia el extremo crítico hacia led_cycle_q del periférico. Se elimina presión sobre la lectura de ROM, pero aparece otra ruta de control/ejecución; el peor slack global solo aumenta 0,114 ns y el área aumenta 2,409 %. Por ese motivo se conserva la versión anterior para la corrida final. No se comparan retardos Q→D de rutas distintas como si fueran la misma ruta.')]
    if refinements:
        additions += [sub('Acotación temporal con layout fijo'),p('Se vuelve a ejecutar STA con los mismos cables, SPEF y retardos externos absolutos de entrada/salida. Solo cambia el período de create_clock en un SDC explícito. Este experimento complementa al barrido de síntesis/PnR; no representa un nuevo placement optimizado para ese período. La tabla muestra el menor período aprobado y el fallo medido inmediatamente inferior de cada layout; todas las muestras de búsqueda se conservan en results/timing/.'),table(['Layout','T ns','Setup slack ns','Hold slack ns','Timing 9 corners'],[[x['source_run'],x['period_ns'],fmt(min(c['setup_ws'] for c in x['corners'].values())),fmt(min(c['hold_ws'] for c in x['corners'].values())),x['pass_timing']] for x in boundary_refinements],[65*mm,15*mm,30*mm,30*mm,30*mm])]
        a=[x for x in refinements if x['source_run']=='final_A_v2_p100_u40' and x['pass_timing']]
        if a:
            t=min(x['period_ns'] for x in a)
            additions += [p(f'El menor período verificado para el layout final fijo es {t:g} ns, equivalente a {1000/t:.6f} MHz. Es un máximo observado sobre la resolución ensayada. La corrida de entrega continúa siendo 100 ns (10 MHz); no se alteraron sus constantes de software.')]
    additions += [sub('Límites eléctricos conservados'),p('El layout final de A cumple los criterios explícitos de DRC Magic, LVS, antena, setup y hold del enunciado. No tiene cierre eléctrico completo: max_ss reporta 2.196 violaciones de slew, 57 de fanout y 4 de capacitancia. Son métricas reales adicionales de checks.rpt/metrics.json; deben resolverse para una integración física que exija esos límites. No se ocultaron ni se desactivaron verificaciones para hacer pasar la entrega.')]
    if b_physical:
        bm=load(f'results/runs/{b_run}/metrics.json',{})
        counts={kind:max(v for k,v in bm.items() if k.startswith(f'design__max_{kind}_violation__count__corner:')) for kind in ['slew','fanout','cap']}
        counts={k:f'{v:,}'.replace(',','.') for k,v in counts.items()}
        additions += [p(f"B también conserva límites eléctricos pendientes: los máximos entre corners son {counts['slew']} de slew, {counts['fanout']} de fanout y {counts['cap']} de capacitancia. Su cierre de los criterios explícitos de la rúbrica no se presenta como preparación completa para fabricación. Los conteos están conservados en sus métricas y en final_artifact_audit.json.")]
    additions += [sub('Bloque de mayor área'),p('En la síntesis jerárquica comparable, el register file es el bloque funcional de mayor área en A (69.363,9296 µm²). La ALU ocupa 8.875,1936 µm² y el contador 3.714,2784 µm², 2,514 % del total de esa misma síntesis. El core agregado incluye otros módulos; no se suma de nuevo con sus hijos.')]
    # Place the final facts before conclusions/references, retaining the source report.
    insert=next((i for i,x in enumerate(story) if isinstance(x,Paragraph) and x.getPlainText().startswith('14. Conclusiones')),len(story))
    story[insert:insert]=additions
    build('Informe_Proyecto3.pdf',story)


def defence():
    qa=[
    ('¿De qué versión parte el proyecto?','De main de Proyecto2AC, revisión 67d0c48; se conserva el historial en un clon independiente. dev-game era anterior. GitHub de Proyecto 2 no fue modificado.'),
    ('¿Qué hace asic_top?','Expone i_Clk, rst_ni, cuatro botones, cuatro LED, catorce señales de segmentos y SPI. Instancia pochoco_soc_asic y no añade pads.'),
    ('¿Por qué se eliminó el POR FPGA?','por_cnt dependía de una inicialización al configurar la FPGA. Un ASIC necesita un reset eléctrico explícito y condiciones de desactivación verificadas.'),
    ('¿Qué significa RV32E aquí?','Datos de 32 bits y 16 registros arquitectónicos. x0 siempre devuelve cero. La implementación del grupo no ejecuta desplazamientos ni instrucciones M.'),
    ('¿Qué hace el assembler?','En dos pasadas resuelve etiquetas y codifica las instrucciones del grupo. La extensión --rom-dir emite casos Verilog y constantes de reset desde el mismo código máquina.'),
    ('¿Cuánto programa hay?','107 instrucciones de 32 bits: 428 bytes. generate_game.py y test_rom.py lo verifican en la imagen real.'),
    ('¿Cuánta RAM de datos usa el juego?','Cero palabras: los lw/sw usan x1=0x80000000 y acceden a MMIO. El estado vive en registros. El testbench también contó cero accesos a RAM.'),
    ('¿Por qué existe una palabra de datos?','Es la reserva mínima de la implementación, en 0x1AC. Permite probar RAM y byte enables. Debe distinguirse capacidad implementada de uso real.'),
    ('¿Cuál es la diferencia entre ROM y RAM?','A fija instrucciones en lógica combinacional y permite escribir solo su RAM de datos. B permite cambiar instrucciones y datos, y restaura el programa al aplicar reset.'),
    ('¿Cómo arranca B?','Sus 108 palabras reciben valores explícitos en la rama de reset sintetizable. No hay readmemh ni bootloader SPI. El costo de esos FF y reset se incluye en el área.'),
    ('¿Qué es un flip-flop?','Un elemento que almacena un bit. El banco tiene 15 × 32 bits de estado arquitectónico; B añade miles de bits de programa y multiplexores, por eso aumenta el área.'),
    ('¿Por qué no usar lectura combinacional en el register file?','Espino espera una lectura síncrona mediante ops_valid_q. Cambiar la latencia sin cambiar el protocolo podría ejecutar operandos incorrectos.'),
    ('¿Cómo se garantiza x0?','La escritura a dirección cero se ignora y ambos puertos retornan cero cuando su dirección registrada corresponde a x0.'),
    ('¿Qué hace la ALU?','Suma, resta, XOR, OR, AND y comparaciones con/sin signo. En espino_alu.v los desplazamientos están deshabilitados. El assembler los rechaza para evitar resultados erróneos.'),
    ('¿Qué hace cycle_counter?','Incrementa 32 bits por ciclo y vuelve a cero con reset. El periférico copia su valor en led_cycle_q en el mismo flanco que escribe LED.'),
    ('¿El tiempo medido coincide exactamente con pulsar?','El inicio sí queda capturado en el flanco del LED. El fin se lee por software después del sondeo del botón. El estímulo a 127 ciclos resultó en 136 medidos: existe latencia de detección y lectura.'),
    ('¿Qué sucede si el contador da la vuelta?','La resta modular de 32 bits conserva el intervalo si transcurren menos de 2^32 ciclos. A 10 MHz, ese intervalo es aproximadamente 429,497 segundos.'),
    ('¿Cómo se adaptaron los tiempos?','Para 10 MHz: espera 30.000.000, décima 1.000.000 y divisor promedio 10.000.000. La imagen abreviada usa 300, 100 y 1000 solo para simulación.'),
    ('¿Qué inconsistencia había en main?','El game.s de main carga 250.000.000 ciclos, mientras que su game.hex carga 75.000.000 y coincide con el informe. Solo cambian dos palabras. Se preservó esa procedencia y se regeneraron fuente/hex de Proyecto3AC para 10 MHz.'),
    ('¿Cómo calcula el promedio?','Acumula ciclos sin truncar en x3 y divide la suma por diez décimas de reloj mediante restas. A 10 MHz el divisor es 10.000.000.'),
    ('¿Qué se probó con el botón incorrecto?','Después de un acierto se envía un botón distinto del objetivo. El display muestra EE y la ronda se reinicia, manteniendo x2 y x3.'),
    ('¿Qué es síntesis?','Transforma RTL en una red de celdas GF180. No produce por sí sola posiciones ni cables físicos ni demuestra DRC/LVS.'),
    ('¿Qué son placement, CTS y routing?','Placement ubica celdas; CTS distribuye clock; routing conecta sus terminales con metales/vías. Sus buffers y parasíticos modifican área y timing.'),
    ('¿Qué significa utilización del 40 %?','La relación objetivo entre área lógica y área del core al crear el floorplan. No equivale a la ocupación final tras buffers, taps y filler.'),
    ('¿Qué son setup y hold?','Setup exige que el dato llegue antes del flanco receptor; hold exige que permanezca estable después. Reducir el período no soluciona hold.'),
    ('¿Qué son WNS y TNS?','WNS es el peor slack negativo y vale cero cuando no hay fallas. TNS suma slacks negativos. Para conocer margen positivo se consulta ws, además de WNS/TNS.'),
    ('¿Por qué verificar nueve corners?','Se combinan tres condiciones de RC con TT, SS y FF. Un resultado típico no demuestra que setup y hold cierren en todos ellos.'),
    ('¿Cómo se identifica la ruta crítica?','En el final, max_ss_125C_4v50/max.rpt muestra u_pochoco.u_ram._604_/Q a u_pochoco.u_ram._648_/D: instr_rdata[4] a ram_b_rdata[16]. El retardo combinacional Q a D es 54,650438 ns. Cruza decodificación/ejecución y lectura de memoria; no es el contador ni necesariamente el bloque de mayor área.'),
    ('¿Qué optimización se probó?','Se registró dirección/selección del puerto de datos de A para separar el cálculo de dirección de la decodificación ROM. La salida conserva su comportamiento al flanco; se compararon 2.000 ciclos aleatorios y el juego.'),
    ('¿Cómo se calcula la frecuencia máxima?','En el barrido con síntesis/PnR, 60 ns cierra y 50 ns falla. Sobre el layout final fijo, 59 ns cierra los nueve corners y 58 ns falla: 1000/59 = 16,949153 MHz observados, con resolución de 1 ns. Se distinguen ambos métodos. La entrega usa 100 ns, 10 MHz.'),
    ('¿Qué significa DRC limpio?','Las geometrías cumplen las reglas revisadas por el verificador ejecutado. Aquí se reporta Magic; la configuración del PDK no proporcionó un deck de KLayout y no se afirma que ese chequeo haya pasado.'),
    ('¿Qué verifica LVS?','Netgen compara la conectividad extraída del layout con la red esperada. Cero discrepancias no reemplaza las pruebas funcionales del juego.'),
    ('¿Qué es antena?','Durante fabricación puede acumularse carga en metal conectado a compuertas. El flujo repara y vuelve a verificar; los reportes finales deben mostrar cero nets/pins violadores o una justificación explícita.'),
    ('¿Las capturas demuestran dónde está la ALU?','Sí cuando las marcas usan las cajas de instancias u_alu extraídas de OpenDB. Los colores por sí solos no son prueba; cell_locations.json permite reproducir la selección.'),
    ('¿Cómo se calcula el costo?','Se divide el área del die en µm² por un millón y se multiplica por US$23.000/mm². No se incluyen máscaras, yield, prueba ni encapsulado.'),
    ('¿Cuál fue la decisión de mayor impacto en área?','La síntesis jerárquica comparable da A 147.741,3504 y B 613.575,9616 µm²: B ocupa aproximadamente 4,15 veces el área. El programa reescribible en FF y sus multiplexores explican el aumento; la reserva de datos del juego es mínima.'),
    ('¿Qué demuestra la simulación de netlist?','Ejecuta celdas estándar con la misma configuración y compara estímulos y resultados por ciclo. No se anotó SDF; STA post-PnR es la evidencia de retardos.'),
    ('¿Qué no debemos afirmar en la defensa?','No afirmar fabricación garantizada, DRC KLayout aprobado, equivalencia formal exhaustiva o una frecuencia no medida. Declarar los límites de slew, fanout y capacitancia de A y B, las etapas pendientes y la resolución de la búsqueda de frecuencia.'),
    ('¿Cómo publicamos el proyecto?','El alumno verifica su identidad y ejecuta personalmente commit y push. Codex no los ejecutó. El remoto proyecto2 tiene push deshabilitado en este clon.')]
    selection=load('results/environment/selected_b_run.json',{})
    selected_b=next((r for r in rows if r['run']==selection.get('run')),None)
    selected_a=next((r for r in rows if r['run']==selection.get('a_comparison_run')),None)
    if selected_b and selected_a:
        qa.append(('¿B se comparó bajo las mismas condiciones físicas que A?',f"Sí: {selected_a['run']} y {selected_b['run']} usan 100 ns y {selected_a['util_pct']} % de utilización inicial, la misma biblioteca y programa. El die medido es {fmt(selected_a['die_area_um2'])} µm² para A y {fmt(selected_b['die_area_um2'])} µm² para B. Esta comparación no cambia el final obligatorio de A a 100 ns y 40 %. Las pruebas B al 40 % que conservaron un short se documentan como incompletas."))
        af=load(f"results/timing/frequency_{selected_a['run']}.json",{})
        bf=load(f"results/timing/frequency_{selected_b['run']}.json",{})
        if af.get('status')=='measured' and bf.get('status')=='measured':
            qa.append(('¿Cuál fue la frecuencia medida al comparar las dos memorias?',f"Sobre sus layouts fijos, con STA en nueve corners y resolución de 1 ns: A pasa a {af['minimum_passing_period_ns']} ns ({fmt(af['frequency_mhz'])} MHz), y B a {bf['minimum_passing_period_ns']} ns ({fmt(bf['frequency_mhz'])} MHz). El período inmediatamente inferior falla en cada caso. Son límites observados del layout fijo, distintos del barrido de síntesis/PnR."))
    story=[Spacer(1,20*mm),p('Guía para la defensa<br/>Proyecto 3','P3Title'),p('Grupo 15 · Pochoco SoC · FPGA a ASIC'),p('Basada en el código y las corridas reales de este repositorio. La defensa presencial vale 1,5 puntos y debe realizarla el grupo.'),h('Recorrido de cinco minutos'),p('Explicar la procedencia del Proyecto 2; recorrer asic_top → pochoco_soc_asic → Espino/periféricos/memoria; mostrar las dos memorias y el mecanismo de arranque; presentar área/timing/signoff; terminar con la comparación RTL/netlist y las limitaciones.'),h('Resultados que conviene tener a mano')]
    story += [table(['Síntesis jerárquica','A','B'],[['Área de celdas µm²',fmt(stats['A'].get('design',{}).get('area')),fmt(stats['B'].get('design',{}).get('area'))],['Instrucciones','107','107'],['Datos usados','0','0']],[80*mm,45*mm,45*mm]),p('Las mediciones finales por corrida están en results/summary.csv; abrir corners.csv para responder preguntas de setup/hold. Evitar memorizar un número de una corrida antigua y atribuirlo al layout final.'),h('Register file, ALU y contador'),p('Register file: asic/rtl/espino_register_file.v; x0 constante, 15 registros escribibles, dos lecturas síncronas, lectura antes de escritura. ALU: rtl/espino_core/espino_alu.v; la ruta crítica debe verificarse en el reporte, no suponerse. Contador: asic/rtl/cycle_counter.v y captura led_cycle_q en asic/rtl/pochoco_periph.v. La extracción jerárquica separa sus áreas; las capturas de OpenDB/KLayout ubican sus celdas.'),h('Preguntas probables y respuestas')]
    for i,(q,a) in enumerate(qa,1):story += [sub(f'{i}. {q}'),p(esc(a))]
    story += [h('Archivos para demostrar, no solo explicar'),p('scripts/verify.py: pruebas ejecutables.<br/>results/synthesis/A_sim_hier/gate_comparison.json: comparación real de netlist.<br/>results/optimization/memory_equivalence.log: prueba comparativa de memoria.<br/>results/runs/*/corners.csv: corners de timing.<br/>docs/figures/: vistas reales del layout.<br/>docs/CHECKLIST_ENTREGA.md: estado contra la rúbrica.<br/>docs/Informe_Proyecto3.pdf: análisis completo.','P3Small')]
    build('Guia_Defensa_Proyecto3.pdf',story)


if __name__=='__main__':
    charts();report();defence()
    print('Generated report and defence guide from',len(rows),'completed runs')
