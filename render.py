from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import PythonLexer, guess_lexer
from pygments.formatters import HtmlFormatter

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('jupyter_notebook.html')

with open('1_data_preparation.html', 'r', encoding='utf-8') as f:
    notebook_html = f.read()

rendered = template.render(notebook_html=notebook_html)

soup = BeautifulSoup(rendered, 'html.parser')
for pre in soup.find_all('pre'):
    if pre.parent.name == 'div' and pre.parent.get('class') and ('highlight' in pre.parent.get('class') or 'output_text' in pre.parent.get('class')):
        continue
    lexer = guess_lexer(pre.string)
    code = highlight(pre.string.rstrip(), lexer, HtmlFormatter())
    pre.replace_with(code)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(soup.prettify(formatter=None))