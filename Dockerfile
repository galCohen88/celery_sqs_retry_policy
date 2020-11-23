FROM python:3.6

COPY . .

RUN pip install -e .


EXPOSE 5000
