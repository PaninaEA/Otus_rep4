FROM python:3.11

WORKDIR /tests

COPY requirements.txt /tests/

RUN pip config set global.trusted-host "pypi.org files.pythonhosted.org"
RUN pip install -r requirements.txt
RUN apt update && apt install -y netcat-traditional

COPY . /tests

ENTRYPOINT ["pytest"]
