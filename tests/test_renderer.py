import tempfile
import os
import pytest

try:
    from wikiscrapper.renderer import render_page
    PLAYWRIGHT_AVAILABLE = True
except Exception:
    PLAYWRIGHT_AVAILABLE = False

pytestmark = pytest.mark.skipif(not PLAYWRIGHT_AVAILABLE, reason="Playwright not available")

def test_render_simple_file_tmp():
    html = """<!doctype html>
    <html>
      <head><title>Test</title></head>
      <body>
        <div id="app">Hello</div>
        <script>document.getElementById('app').innerText += ' World';</script>
      </body>
    </html>
    """
    with tempfile.TemporaryDirectory() as td:
        fn = os.path.join(td, "test.html")
        with open(fn, "w", encoding="utf-8") as f:
            f.write(html)
        file_url = "file://" + fn
        try:
            content = render_page(file_url, timeout=5000)
        except RuntimeError as e:
            pytest.skip(f"Playwright runtime not available: {e}")
        assert "Hello World" in content
