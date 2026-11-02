from pathlib import Path
import sys
from PIL import Image,ImageOps,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/(sys.argv[1] if len(sys.argv)>1 else 'work/pdfqa_review')
for kind in ['report','defence']:
    files=sorted(QA.glob(kind+'-*.png'))
    for offset in range(0,len(files),6):
        sheet=Image.new('RGB',(1000,1480),'#d7e0e6')
        draw=ImageDraw.Draw(sheet)
        for index,f in enumerate(files[offset:offset+6]):
            im=Image.open(f).convert('RGB');im.thumbnail((480,690))
            x=(index%2)*500+(500-im.width)//2;y=(index//2)*490+23
            # Fit 3 rows of pages while preserving each page's aspect ratio.
            im.thumbnail((325,455));x=(index%2)*500+(500-im.width)//2
            sheet.paste(im,(x,y));draw.text(((index%2)*500+20,(index//2)*490+6),f.name,fill='black')
        sheet.save(QA/f'{kind}_sheet_{offset//6+1}.png')
