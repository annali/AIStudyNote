"""End-to-end content lifecycle checks in an isolated temporary project."""
import json
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
ROOT = Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.urls=[]
    def handle_starttag(self, tag, attrs):
        self.urls += [v for k,v in attrs if k in ('href','src') and v]
def run(root, success=True):
    result=subprocess.run([sys.executable,'scripts/build.py'],cwd=root,capture_output=True,text=True)
    if (result.returncode == 0) != success: raise AssertionError(result.stdout+result.stderr)
def check():
    with tempfile.TemporaryDirectory(prefix='notebook-check-') as temp:
        root=Path(temp)/'project'
        shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','dist','__pycache__'))
        run(root)
        out=root/'dist'
        for page in out.rglob('*.html'):
            doc=Links();doc.feed(page.read_text())
            for href in doc.urls:
                u=urlsplit(href)
                if u.scheme or u.netloc or not u.path: continue
                target=(page.parent/unquote(u.path)).resolve()
                assert target.is_relative_to(out.resolve()) and target.exists(),(page,href)
        print('PASS: 所有內部頁面、管理入口與資源路徑')
        seed=sorted((root/'content').glob('*.json'))[0]
        original=json.loads(seed.read_text())
        original.update(slug='lifecycle-check',title='內容生命週期檢查')
        note=root/'content/lifecycle-check.json'
        note.write_text(json.dumps(original,ensure_ascii=False))
        run(root)
        assert (out/'notes/lifecycle-check.html').exists()
        assert 'lifecycle-check.html' in (out/'index.html').read_text()
        assert 'lifecycle-check' in (out/'search-index.json').read_text()
        original['title']='修改後的筆記標題'
        note.write_text(json.dumps(original,ensure_ascii=False))
        run(root)
        assert '修改後的筆記標題' in (out/'notes/lifecycle-check.html').read_text()
        note.unlink();run(root)
        assert not (out/'notes/lifecycle-check.html').exists()
        assert 'lifecycle-check' not in (out/'index.html').read_text()
        assert 'lifecycle-check' not in (out/'search-index.json').read_text()
        print('PASS: 新增、修改、刪除同步更新文章、首頁與搜尋索引')
        original.update(slug='中文筆記測試',sources=[{'title':'格式相容測試','url':'http://www.wikipedia.org/'}])
        unicode_note=root/'content/中文筆記測試.json'
        unicode_note.write_text(json.dumps(original,ensure_ascii=False))
        run(root)
        assert (out/'notes/中文筆記測試.html').exists()
        assert 'http://www.wikipedia.org/' in (out/'notes/中文筆記測試.html').read_text()
        unicode_note.unlink();run(root)
        print('PASS: 中文網址名稱與 HTTP 來源可建置')
        demo_note=root/'content/few-shot-prompting.json'
        if demo_note.exists():
            saved=demo_note.read_bytes()
            demo_note.unlink();run(root)
            assert 'href="notes/few-shot-prompting.html"' not in (out/'extension-demo.html').read_text()
            demo_note.write_bytes(saved);run(root)
            print('PASS: 移除示範筆記時，歷史紀錄頁不留下失效連結')
        before=(out/'index.html').read_bytes()
        bad=json.loads(seed.read_text())
        bad['sections']=[]
        seed.write_text(json.dumps(bad))
        run(root,success=False)
        assert before == (out/'index.html').read_bytes()
        print('PASS: 無效內容阻止建置且保留前次產物')
if __name__ == '__main__': check()
