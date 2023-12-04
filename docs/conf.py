extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.todo', 'sphinx.ext.ifconfig']

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = u'posmotrim_backend'
copyright = u'2023, Posmotrim Project'

version = '1.0'

release = '1.0.0'

exclude_patterns = ['_build']

pygments_style = 'sphinx'

html_theme = 'default'

html_static_path = ['_static']

html_show_sourcelink = False

html_show_copyright = False

htmlhelp_basename = 'posmotrimdoc'

epub_title = u'Posmotrim'
epub_author = u'Posmotrim Contributors'
epub_publisher = u'Posmotrim Contributors'
epub_copyright = u'2023, Posmotrim Contributors'

intersphinx_mapping = {'http://docs.python.org/': None}