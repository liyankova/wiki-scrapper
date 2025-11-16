from wikiscrapper.utils import normalize_url

def test_normalize_basic():
    u = "HTTP://Example.com/Path/index.html#section?b=2&a=1"
    n = normalize_url(u)
    assert "example.com" in n
    assert "#" not in n
