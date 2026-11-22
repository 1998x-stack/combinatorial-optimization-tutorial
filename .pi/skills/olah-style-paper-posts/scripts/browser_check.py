#!/usr/bin/env python3
"""Real Chromium smoke/interaction/viewport verification with JSON evidence."""
from __future__ import annotations
import argparse, json, sys, os
from pathlib import Path
from playwright.sync_api import sync_playwright

SIZES=[('desktop',1440,900),('tablet',768,1024),('mobile',390,844),('narrow-mobile',360,800)]

def main():
    pa=argparse.ArgumentParser(description=__doc__)
    pa.add_argument('html',type=Path);pa.add_argument('--output',type=Path,required=True)
    pa.add_argument('--click',default='button',help='CSS selector for interactive buttons')
    args=pa.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    page_file=args.html.resolve(); report={'file':str(page_file),'pass':True,'viewports':{},'errors':[],'interaction':{}}
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--no-sandbox'], **({'executable_path':os.getenv('CHROMIUM_PATH','/usr/bin/chromium')} if Path(os.getenv('CHROMIUM_PATH','/usr/bin/chromium')).exists() else {}))
        for label,w,h in SIZES:
            page=browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
            errors=[];network=[]
            page.on('pageerror',lambda e,log=errors:log.append(str(e)))
            page.on('console',lambda m,log=errors:log.append('console: '+m.text) if m.type=='error' else None)
            page.route('https?://**',lambda route,log=network:(log.append(route.request.url),route.abort()))
            page.set_content(page_file.read_text(encoding='utf-8'), wait_until='load')
            page.screenshot(path=str(args.output/f'{label}.png'),full_page=False)
            measure=page.evaluate('''() => {
              const math = [...document.querySelectorAll('math')];
              const ns = 'http://www.w3.org/1998/Math/MathML';
              const visible = e => getComputedStyle(e).display !== 'none'
                && e.getClientRects().length > 0;
              const fractions = [...document.querySelectorAll('math mfrac')].filter(visible);
              const badFractions = fractions.filter(e => {
                const children = [...e.children];
                if (children.length !== 2) return true;
                const numerator = children[0].getBoundingClientRect();
                const denominator = children[1].getBoundingClientRect();
                return !(numerator.top < denominator.top);
              }).length;
              const regions = [...document.querySelectorAll(
                '[data-math-scroll],.math-scroll,.eq-scroll')];
              const wrongScroll = regions.filter(e => e.scrollWidth > e.clientWidth + 2
                && (e.tabIndex < 0 || !['auto','scroll'].includes(getComputedStyle(e).overflowX))).length;
              return {
                scrollWidth:document.documentElement.scrollWidth,
                viewport:innerWidth,
                heading:document.querySelectorAll('h1').length,
                svgs:document.querySelectorAll('svg').length,
                blankSVG:[...document.querySelectorAll('svg')]
                  .filter(s=>s.getBoundingClientRect().width<1||s.getBoundingClientRect().height<1).length,
                brokenImages:[...document.images].filter(i=>!i.complete||i.naturalWidth<1).length,
                mathCount:math.length,
                mathWrongNamespace:math.filter(e=>e.namespaceURI!==ns).length,
                mathNestedInSVG:document.querySelectorAll('svg math').length,
                mathZeroSized:math.filter(e=>visible(e)
                  && (e.getBoundingClientRect().width<2||e.getBoundingClientRect().height<4)).length,
                mathBadFractions:badFractions,
                mathBadScrollRegions:wrongScroll
              };
            }''')
            okay=(measure['scrollWidth']<=measure['viewport']+1 and measure['blankSVG']==0
               and measure['brokenImages']==0 and measure['heading']==1
               and measure['mathWrongNamespace']==0 and measure['mathNestedInSVG']==0
               and measure['mathZeroSized']==0 and measure['mathBadFractions']==0
               and measure['mathBadScrollRegions']==0 and not errors and not network)
            report['viewports'][label]={'pass':okay,**measure,'errors':errors,'external_requests':network}
            if not okay:report['pass']=False
            if label=='desktop':
                candidates=page.locator(args.click)
                if candidates.count()>=2:
                    before=page.content();changed=False
                    for i in range(min(6,candidates.count())):
                        try:
                            candidates.nth(i).click(timeout=1500)
                            if page.content()!=before:changed=True;break
                        except Exception as exc:errors.append('interaction:'+str(exc)[:120])
                    report['interaction']={'status':'verified' if changed else 'failed','buttons':candidates.count()}
                    if not changed:report['pass']=False
                elif candidates.count()==1:
                    before=page.content();candidates.first.click();changed=page.content()!=before
                    report['interaction']={'status':'verified' if changed else 'failed','buttons':1}
                    if not changed: report['pass']=False
                else:report['interaction']={'status':'not-applicable','buttons':0}
                # Print-view smoke render; also preserve screenshot.
                page.emulate_media(media='print');page.screenshot(path=str(args.output/'print.png'),full_page=False)
            page.close()
        browser.close()
    (args.output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if report['pass'] else 1

if __name__=='__main__':sys.exit(main())
