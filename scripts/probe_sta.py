from librelane.steps import OpenROAD
for v in OpenROAD.STAPostPNR.config_vars:
    if any(x in v.name for x in ['SDC','CORNER']): print(v.name,v.default,v.description)
for v in OpenROAD.DetailedRouting.config_vars:
    if 'DRT_' in v.name: print(v.name,v.default,v.description)
