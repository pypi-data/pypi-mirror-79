from setuptools import setup
import pypandoc

with open('./README.md', encoding='utf-8') as f:
    long_description = f.read()

# rst_description = pypandoc.convert_text(long_description, 'rst', format='markdown_github')

setup(
    name = "sout",
    version = '0.0.0',
    description = 'This package provides a simple output of python objects.',
    author = 'bib_inf',
    author_email = 'contact.bibinf@gmail.com',
    url = 'https://github.co.jp/',
    packages = ["sout"],
    install_requires = ["relpath==2.78"],
    long_description = long_description,
    long_description_content_type = "text/markdown"
)
