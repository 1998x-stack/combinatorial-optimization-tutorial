#!/usr/bin/env python3
"""Extract inline SVG as stand-alone, computed-style-preserving XML using Chromium."""
from __future__ import annotations
import argparse, re, sys, json, os
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

CSS = ['fill','stroke','stroke-width','stroke-dasharray','stroke-linejoin','stroke-linecap','opacity',
       'font-family','font-size','font-weight','font-style','letter-spacing','text-anchor',
       'dominant-baseline','paint-order','color','fill-rule','clip-rule','visibility']
JS = r'''(keys) => {
 const nodes = [...document.querySelectorAll('svg')];
 return nodes.map((root, i) => {
   const cloned = root.cloneNode(true);
   const a = [root, ...root.querySelectorAll('*')];
   const b = [cloned, ...cloned.querySelectorAll('*')];
   a.forEach((original, j) => {
     const computed = getComputedStyle(original);
     const node = b[j];
     let st = node.getAttribute('style') || '';
     keys.forEach(k => { const v = computed.getPropertyValue(k); if(v && v !== 'none' && v !== 'normal' && v !== 'auto') st += `;${k}:${v}`; });
     node.setAttribute('style', st);
   });
   cloned.setAttribute('xmlns','http://www.w3.org/2000/svg');
   if(!cloned.getAttribute('viewBox')) {
     const bb=root.getBBox(); cloned.setAttribute('viewBox', `${bb.x} ${bb.y} ${Math.max(bb.width,1)} ${Math.max(bb.height,1)}`);
   }
   const holder=document.createElement('div'); holder.appendChild(cloned);
   const fig=root.closest('figure');
   return { name:root.dataset.export || fig?.id || `figure-${String(i+1).padStart(2,'0')}`,
       title:root.getAttribute('aria-label')||root.querySelector('title')?.textContent||'', html:holder.innerHTML };
 });
}'''

def clean_svg(svg: str, title: str) -> str:
    # Browser serializes SVG as XML-compatible markup. Remove scripts/events/external references.
    svg = re.sub(r'<script\b[^>]*>.*?</script>', '', svg, flags=re.I|re.S)
    svg = re.sub(r'\s+on[a-zA-Z]+="[^"]*"', '', svg)
    svg = re.sub(r'\s+(?:href|xlink:href)="(?:https?:|javascript:)[^"]*"', '', svg, flags=re.I)
    svg = re.sub(r'<foreignObject\b[^>]*>.*?</foreignObject>', '', svg, flags=re.I|re.S)
    if '<title' not in svg and title:
        from xml.sax.saxutils import escape
        svg = svg.replace('>', f'><title>{escape(title)}</title>', 1)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + svg + '\n'

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html',type=Path);parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args(); args.out.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True, args=['--no-sandbox'], **({'executable_path':os.getenv('CHROMIUM_PATH','/usr/bin/chromium')} if Path(os.getenv('CHROMIUM_PATH','/usr/bin/chromium')).exists() else {}))
        page=browser.new_page(viewport={'width':1440,'height':900})
        page.set_content(args.html.resolve().read_text(encoding='utf-8'), wait_until='load')
        items=page.evaluate(JS,CSS)
        browser.close()
    names=set();manifest=[]
    for i,item in enumerate(items,1):
        slug=re.sub('[^A-Za-z0-9_-]+','-',item['name']).strip('-').lower() or f'figure-{i:02d}'
        slug=slug[:70]
        name=slug+'.svg'
        if name in names: name=f'{slug}-{i}.svg'
        names.add(name)
        content=clean_svg(item['html'],item['title'])
        try: ET.fromstring(content)
        except ET.ParseError as exc: raise RuntimeError(f'Invalid standalone SVG: {name}: {exc}') from exc
        (args.out/name).write_text(content,encoding='utf-8')
        manifest.append({'file':name,'title':item['title']})
    (args.out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Exported {len(manifest)} independent SVGs to {args.out}')
    return 0

if __name__=='__main__': sys.exit(main())
