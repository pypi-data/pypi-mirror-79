from setuptools import setup
import pypandoc

with open('./README.md', encoding='utf-8') as f:
    long_description = f.read()

# rst_description = pypandoc.convert_text(long_description, 'rst', format='markdown_github')

setup(
    name = "llog",
    version = "0.0.1",
    description = "local log (a logging tool that doesn't pollute the global scope)",
    author = "bib_inf",
    author_email = "contact.bibinf@gmail.com",
    url = "https://github.co.jp/",
    packages = ["llog"],
    install_requires = ["relpath", "sout"],
    long_description = long_description,
    long_description_content_type = "text/markdown"
)
