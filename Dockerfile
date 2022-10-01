  
FROM python:3.8



# download sqlite data
ARG REMOTE_DB_AT
ENV REMOTE_DB_AT=${REMOTE_DB_AT}

RUN curl -s $REMOTE_DB_AT | gunzip > data.db

COPY requirements-app.txt requirements-app.txt
COPY src src
COPY setup.py setup.py

# install requires
RUN pip install -r requirements-app.txt

# go
CMD ["python", "-m", "app.wsgi"]
