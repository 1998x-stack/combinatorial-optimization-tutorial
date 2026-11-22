#!/usr/bin/env python3
"""Create a paper explainer from the canonical offline HTML and CSS template."""
from __future__ import annotations
import argparse,re,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--slug',required=True);ap.add_argument('--title',required=True)
    ap.add_argument('--dek',default='从一个具体问题开始，逐步建立论文所提出方法的直觉和计算过程。')
    ap.add_argument('--out',type=Path,default=Path('posts'))
    args=ap.parse_args()
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',args.slug):ap.error('Slug must be lowercase kebab-case')
    if not args.title.strip():ap.error('Title cannot be blank')
    dest=args.out/args.slug;dest.mkdir(parents=True,exist_ok=True)
    tpl=(ROOT/'assets/templates/article.html').read_text(encoding='utf-8')
    css=(ROOT/'assets/css/article.css').read_text(encoding='utf-8')
    tpl=tpl.replace('{{TITLE}}',args.title).replace('{{DEK}}',args.dek)
    tpl=tpl.replace('/* Inline assets/css/article.css at export time or use a relative path. */',css)
    (dest/'index.html').write_text(tpl,encoding='utf-8')
    (dest/'evidence.json').write_text('[]\n',encoding='utf-8')
    print('Created',dest.resolve())
    return 0
if __name__=='__main__':sys.exit(main())
