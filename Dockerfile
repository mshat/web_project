FROM python:3.9
ENV PYTHONBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN sed -i 's/staticfiles/static/g' /usr/local/lib/python3.9/site-packages/rest_framework_swagger/templates/rest_framework_swagger/index.html