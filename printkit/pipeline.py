"""Dependency-ordered targets; each PDF has exactly one layout owner."""
import argparse
import importlib
import os
from pathlib import Path
from pypdf import PdfReader
from printkit.common import ROOT, render_html, merge_pdfs

TARGETS = ['station1','station2','station3','station4','station5','helpers','introductions','opening','finale','dm-guide']

def module(name):
    return importlib.import_module('printkit.generators.'+name.replace('-','_'))

def build_station(number, refresh_dependencies=True):
    if refresh_dependencies:
        module('introductions').build(stations=[number])
        module('helpers').build(stations=[number],combined=False)
    module(f'station{number}').build()
    d=ROOT/'Art'/f'Station_{number}'
    if number in (1,4):
        for part in ['Player_Print_Pack','Reveals_Print_Pack','DM_Notes']:
            render_html(d/f'Station_{number}_{part}.html')
        merge_pdfs([d/f'Station_{number}_{part}.pdf' for part in ['Player_Introduction','Player_Print_Pack','Reveals_Print_Pack','DM_Notes']]+[ROOT/'Helpers'/f'Station_{number}_Helper_Cards.pdf'],d/f'Station_{number}_Complete_Print_Pack.pdf')
    elif number==5:
        for part in ['Player','DM']:
            render_html(d/f'Station_5_{part}_Print_Pack.html')
        print('Station 5: component PDFs built; corridor clipping remains an open readiness issue. No complete pack published.')

def build_targets(targets):
    targets = list(dict.fromkeys(targets))
    if 'all' in targets:
        targets = ['introductions','helpers'] + [f'station{i}' for i in range(1,6)] + ['opening','finale','dm-guide']
    shared_ready = set()
    for target in targets:
        print(f'Building {target}...',flush=True)
        if target.startswith('station'):
            build_station(int(target[-1]), refresh_dependencies=not {'helpers','introductions'}.issubset(shared_ready))
        elif target in ['helpers','introductions','opening']:
            if target=='opening':module('helpers').build_opening()
            else:
                module(target).build()
                shared_ready.add(target)
        else:
            module(target).build()
    return targets

def check_outputs(targets):
    expected={'station1':16,'station2':13,'station3':14,'station4':16,'finale':12}
    for target in targets:
        if target.startswith('station') and target!='station5':
            number=target[-1];path=ROOT/f'Art/Station_{number}/Station_{number}_Complete_Print_Pack.pdf'
        elif target=='finale':path=ROOT/'Finale/Finale_Complete_Print_Pack.pdf'
        elif target=='opening':path=ROOT/'Finale/Opening_Print_Kit.pdf'
        elif target=='helpers':path=ROOT/'Helpers/All_Helper_GM_Cards.pdf'
        elif target=='introductions':path=ROOT/'Stations/Introductions/All_Stations_Player_Introductions.pdf'
        elif target=='dm-guide':path=ROOT/'DM_Guide/DM_Guide.pdf'
        else:continue
        reader=PdfReader(path)
        if not reader.pages:raise ValueError(f'Empty PDF: {path}')
        if target in expected and len(reader.pages)!=expected[target]:
            raise ValueError(f'{target}: expected {expected[target]} pages, got {len(reader.pages)}; review pagination')
        print(f'Checked {path.relative_to(ROOT)}: {len(reader.pages)} pages')

def main(argv=None):
    parser=argparse.ArgumentParser(description='Build Halloween one-shot PDFs in their existing station folders.')
    parser.add_argument('targets',nargs='*',choices=['all']+TARGETS,help='Default: all. Individual station builds include fresh intro and helper PDFs.')
    parser.add_argument('--list',action='store_true',help='List build targets without writing files')
    parser.add_argument('--check',action='store_true',help='Validate rebuilt complete-pack page counts')
    parser.add_argument('--chrome',type=Path,help='Override Chrome/Chromium executable (or use PRINTKIT_CHROME)')
    args=parser.parse_args(argv)
    if args.list:
        print('\n'.join(['all']+TARGETS));return
    if args.chrome:os.environ['PRINTKIT_CHROME']=str(args.chrome.resolve())
    built=build_targets(args.targets or ['all'])
    if args.check:check_outputs(built)
