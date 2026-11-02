"""Reproduce the real first routing iteration, preserving its transient DRC boxes."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
cfg=json.loads((ROOT/'asic/configs/final.json').read_text())
cfg.update(DRT_OPT_ITERS=0,DRT_SAVE_DRC_REPORT_ITERS=1)
(ROOT/'asic/configs/DEBUG_first_route.json').write_text(json.dumps(cfg,indent=2)+'\n')
