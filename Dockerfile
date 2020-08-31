  
FROM python:3.8

# set up whoosh index. later, set this up to grab from a variable.
RUN curl http://nolanc.heliohost.org/omg-data/data.db.gz | gunzip > data.db

COPY requirements-app.txt requirements-app.txt
COPY src src
COPY setup.py setup.py

# install requires
RUN pip install -r requirements-app.txt

# go
CMD ["python", "-m", "app.wsgi"]