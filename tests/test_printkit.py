import contextlib
import importlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from pypdf import PdfReader, PdfWriter
from printkit import common, pipeline
from printkit.generators import introductions

class PrintKitTests(unittest.TestCase):
    def test_merge_order_and_failed_build_preserves_existing_pack(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp); parts=[]
            for width in [100,200]:
                p=tmp/f'{width}.pdf'; w=PdfWriter(); w.add_blank_page(width=width,height=300)
                with p.open('wb') as stream:w.write(stream)
                parts.append(p)
            output=tmp/'pack.pdf';common.merge_pdfs(parts,output)
            self.assertEqual([float(p.mediabox.width) for p in PdfReader(output).pages],[100,200])
            before=output.read_bytes()
            with self.assertRaises(FileNotFoundError):common.merge_pdfs(parts+[tmp/'missing.pdf'],output)
            self.assertEqual(output.read_bytes(),before)

    def test_html_failure_does_not_replace_existing_pdf(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp); source=tmp/'page.html';source.write_text('<p>Example</p>')
            output=tmp/'page.pdf';output.write_bytes(b'previous PDF')
            with patch.object(common,'chrome_path',return_value='/fake/chrome'),patch.object(common.subprocess,'run'):
                with self.assertRaises(RuntimeError):common.render_html(source,output)
            self.assertEqual(output.read_bytes(),b'previous PDF')

    def test_station_build_refreshes_dependencies_before_layout(self):
        calls=[]
        class Builder:
            def __init__(self,name):self.name=name
            def build(self,**kwargs):calls.append((self.name,kwargs))
        with patch.object(pipeline,'module',side_effect=lambda name:Builder(name)):
            pipeline.build_station(2)
        self.assertEqual(calls,[('introductions',{'stations':[2]}),('helpers',{'stations':[2],'combined':False}),('station2',{})])

    def test_introduction_uses_markdown_instead_of_embedded_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp); source=tmp/'Stations/Introductions/Station_2_Player_Introduction.md'
            source.parent.mkdir(parents=True);source.write_text('# Station 2: Changed title\n\n*Subtitle*\n\nChanged paragraph.\n\n---\n\n**Updated** note.\n')
            with patch.object(introductions,'ROOT',tmp):
                self.assertEqual(introductions.read_entry(2),('Changed title','Subtitle',['Changed paragraph.'],'<b>Updated</b> note.'))

    def test_layout_imports_do_not_build_anything(self):
        with patch.object(Path,'write_text',side_effect=AssertionError('import wrote a file')):
            for name in ['station1','station2','station3','station4','station5','finale','dm_guide']:
                importlib.reload(importlib.import_module('printkit.generators.'+name))

    def test_all_refreshes_shared_inputs_once_before_stations(self):
        from types import SimpleNamespace
        calls=[]
        def builder(name):
            return SimpleNamespace(build=lambda **kwargs:calls.append(name), build_opening=lambda:calls.append('opening'))
        with patch.object(pipeline,'module',side_effect=builder),patch.object(pipeline,'build_station') as station:
            pipeline.build_targets(['all'])
        self.assertEqual(calls[:2],['introductions','helpers'])
        self.assertEqual(calls.count('introductions'),1)
        self.assertEqual(calls.count('helpers'),1)
        self.assertEqual(station.call_count,5)
        self.assertTrue(all(call.kwargs['refresh_dependencies'] is False for call in station.call_args_list))

    def test_default_command_selects_all(self):
        with patch.object(pipeline,'build_targets',return_value=[]) as build:
            pipeline.main([])
        build.assert_called_once_with(['all'])

    def test_help_list_does_not_build(self):
        with patch.object(pipeline,'build_targets',side_effect=AssertionError('unexpected build')):
            with contextlib.redirect_stdout(io.StringIO()):pipeline.main(['--list'])

if __name__=='__main__':unittest.main()
