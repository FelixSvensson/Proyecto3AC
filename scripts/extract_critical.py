"""Extract start/end pins and measured path delays from the final STA report."""
from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parents[1]
tags=['A_v2_p100_u40','A_opt_v2_p100_u40','final_A_v2_p100_u40']
out=ROOT/'results/timing';out.mkdir(parents=True,exist_ok=True)
rows=[]
for tag in tags:
    run=ROOT/'asic/configs/runs'/tag
    report=next(run.glob('*stapostpnr/max_ss_125C_4v50/max.rpt'))
    text=report.read_text()
    start=re.search(r'Startpoint:\s+(\S+)',text).group(1)
    end=re.search(r'Endpoint:\s+(\S+)',text).group(1)
    first=text[:text.find('Startpoint:',text.find('Startpoint:')+1)]
    arrival=float(re.search(r'([-\d.]+)\s+data arrival time',first).group(1))
    required=float(re.search(r'([-\d.]+)\s+data required time',first).group(1))
    slack=float(re.search(r'([-\d.]+)\s+slack',first).group(1))
    qline=next(line for line in first.splitlines() if start+'/Q ' in line)
    # Table time is the last number preceding the transition marker and pin.
    launch_q_time=float(qline.split('^')[0].split('v')[0].split()[-1])
    nl=json.loads(next(run.glob('*yosys-synthesis/asic_top.nl.v.json')).read_text())['modules']['asic_top']
    def signal(cell,port):
        bits=nl['cells'].get(cell,{}).get('connections',{}).get(port,[])
        names=[name for name,net in nl['netnames'].items() if bits and net['bits']==bits and not name.startswith('_')]
        return names
    row=dict(run=tag,corner='max_ss_125C_4v50',startpoint=start+'/Q',endpoint=end+'/D',
             launch_output_time_ns=launch_q_time,data_arrival_time_ns=arrival,
             combinational_q_to_d_ns=arrival-launch_q_time,required_time_ns=required,slack_ns=slack,
             start_signal=signal(start,'Q'),end_state_signal=signal(end,'Q'),source=str(report.relative_to(ROOT)))
    rows.append(row)
    (out/(tag+'_critical_path.rpt')).write_text(first)
(out/'critical_paths.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
