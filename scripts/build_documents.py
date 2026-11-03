"""Genera los gráficos del informe (docs/figures/) a partir de las mediciones guardadas."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs';FIG=DOCS/'figures';FIG.mkdir(exist_ok=True)
def load(path,default=None):
    p=ROOT/path
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else default
rows=load('results/summary.json',[])
stats={s:load(f'results/synthesis/{s}_prod_hier/stat.json',{}) for s in ['A','B']}

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


if __name__=='__main__':
    charts()
    print('Generated figures from',len(rows),'completed runs')
