FROM python:3.9.1

WORKDIR /capsproject

RUN pip install --upgrade pip
COPY requirements.txt /capsproject/requirements.txt
RUN pip install -r /capsproject/requirements.txt

COPY . /capsproject

RUN chmod +x boot.sh
RUN chmod +x wait-for-it.sh


ENV FLASK_APP caps.py
ENV PYTHONPATH "${PYTHONPATH}:/course_project"


EXPOSE 5000
