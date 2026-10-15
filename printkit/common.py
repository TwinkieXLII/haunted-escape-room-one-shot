"""Repository paths, browser export and safe PDF assembly."""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]

def chrome_path():
    configured = os.environ.get('PRINTKIT_CHROME')
    candidates = [configured] if configured else [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        shutil.which('google-chrome'), shutil.which('chromium'), shutil.which('chromium-browser')]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(Path(candidate).resolve())
    raise RuntimeError('Chrome/Chromium was not found. Set PRINTKIT_CHROME to its executable path.')

def render_html(source, output=None, budget_ms=8000):
    """Export to a temporary PDF; replace the destination only after validation."""
    source = Path(source).resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    output = Path(output or source.with_suffix('.pdf')).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    browser = chrome_path()
    with tempfile.TemporaryDirectory(prefix='printkit-') as temp:
        temp = Path(temp)
        pdf = temp / 'export.pdf'
        subprocess.run([browser, '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
                        f'--virtual-time-budget={budget_ms}', f'--print-to-pdf={pdf}', source.as_uri()],
                       stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True, timeout=90)
        if not pdf.is_file() or not PdfReader(pdf).pages:
            raise RuntimeError(f'Browser did not produce a valid PDF: {source}')
        # Stage on the destination filesystem so replacement is atomic.
        staged = output.with_name('.' + output.name + '.building')
        try:
            shutil.copyfile(pdf, staged)
            staged.replace(output)
        finally:
            staged.unlink(missing_ok=True)
    return output

def merge_pdfs(parts, output):
    """Merge in declared order without replacing an existing pack on failure."""
    output = Path(output)
    writer = PdfWriter()
    for part in parts:
        reader = PdfReader(Path(part))
        if not reader.pages:
            raise ValueError(f'Empty PDF: {part}')
        for page in reader.pages:
            writer.add_page(page)
    if not writer.pages:
        raise ValueError('Cannot assemble a pack without pages')
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, staged = tempfile.mkstemp(prefix='.'+output.stem, suffix='.pdf', dir=output.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            writer.write(stream)
        Path(staged).replace(output)
    finally:
        Path(staged).unlink(missing_ok=True)
    return output
