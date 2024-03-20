FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt /app
RUN apt update && apt install -y libpq-dev python-dev
RUN PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.3/bin
RUN pip3 install --upgrade pip
RUN pip install --upgrade wheel
RUN pip install --upgrade setuptools
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python", "main.py"]