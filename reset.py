# Ref.
# https://collerek.github.io/ormar/models/migrations/#database-initialization
import sqlalchemy
from main import metadata

engine = sqlalchemy.create_engine('sqlite:///test.db')
metadata.create_all(engine)
