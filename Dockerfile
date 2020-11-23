FROM python:3.6

COPY . .
RUN pip install --upgrade pip setuptools wheel
RUN pip install git+https://git@github.com/galCohen88/kombu.git
RUN pip install git+https://git@github.com/galCohen88/celery.git
RUN pip install pycurl
RUN pip install -e .


EXPOSE 5000

