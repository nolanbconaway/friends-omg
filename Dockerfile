  
FROM python:3.8

# download sqlite data
RUN curl http://nolanc.heliohost.org/omg-data/data.db.gz | gunzip > data.db

COPY requirements-app.txt requirements-app.txt
COPY src src
COPY setup.py setup.py

# install requires
RUN pip install -r requirements-app.txt

# go
CMD ["python", "-m", "app.wsgi"]
