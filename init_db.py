from database import engine,Base
from models import User,Order


# used to create tables in the database
Base.metadata.create_all(bind=engine)