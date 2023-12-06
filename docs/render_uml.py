from eralchemy2 import render_er

from src.app.models import Base

render_er(Base, 'erd_from_sqlalchemy.png')
