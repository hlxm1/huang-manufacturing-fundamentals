"""Locate original pages, optionally search a user-supplied OCR cache or render a page."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--chapter', type=int, choices=range(1, 10))
    group.add_argument('--topic', help='Exact or partial Chinese topic')
    group.add_argument('--page', type=int, help='Printed page, 1 through 311')
    group.add_argument('--search', help='Literal, case-insensitive OCR search')
    parser.add_argument('--ocr', type=Path, help='Local page-NNN.json cache')
    parser.add_argument('--pdf', type=Path, help='Local source PDF')
    parser.add_argument('--render', type=Path, help='PNG destination, requires --page and --pdf')
    args = parser.parse_args(argv)
    index = json.loads((ROOT/'references/source-index.json').read_text(encoding='utf-8'))
    if args.render and (args.page is None or args.pdf is None):
        parser.error('--render requires --page and --pdf')
    if args.page is not None:
        if not 1 <= args.page <= 311:
            parser.error('printed page must be between 1 and 311; front matter is not mapped')
        result = {'book_page': args.page, 'pdf_page': args.page+10}
        if args.render:
            if not args.pdf.is_file():
                parser.error('--pdf must name an existing file')
            if hashlib.sha256(args.pdf.read_bytes()).hexdigest() != index['source_sha256']:
                parser.error('PDF SHA-256 differs from the indexed source; verify edition and page mapping')
            try:
                import pymupdf
            except ImportError:
                parser.exit(2, 'Rendering requires PyMuPDF: python -m pip install pymupdf\n')
            with pymupdf.open(args.pdf) as doc:
                if len(doc) != index['pdf_pages']:
                    parser.error('PDF page count differs from this edition; verify page mapping')
                args.render.parent.mkdir(parents=True, exist_ok=True)
                doc[args.page+9].get_pixmap(matrix=pymupdf.Matrix(2, 2)).save(args.render)
            result['image'] = str(args.render.resolve())
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.search is not None:
        if not args.search.strip():
            parser.error('--search must not be empty')
        if args.ocr is None or not args.ocr.is_dir():
            parser.error('--search requires an existing local --ocr directory')
        matches=[]
        for path in sorted(args.ocr.glob('page-*.json')):
            page=json.loads(path.read_text(encoding='utf-8'))
            content=page.get('text','')
            offset=content.casefold().find(args.search.casefold())
            if offset>=0:
                pdf_page=page['pdf_page']
                matches.append({'pdf_page':pdf_page,
                    'book_page':pdf_page-10 if 11<=pdf_page<=321 else None,
                    'snippet':content[max(0,offset-60):offset+len(args.search)+160]})
        print(json.dumps(matches, ensure_ascii=False, indent=2))
    else:
        matches=[]
        for chapter in index['chapters']:
            if args.chapter is not None:
                if chapter['chapter']==args.chapter: matches.append(chapter)
            elif args.topic.casefold() in chapter['title'].casefold() or any(
                    args.topic.casefold() in term.casefold() for term in chapter['topics']):
                matches.append(chapter)
        print(json.dumps(matches, ensure_ascii=False, indent=2))
    return 0

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
