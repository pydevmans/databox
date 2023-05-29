FROM tecktron/python-waitress:latest
RUN mkdir /var/app
WORKDIR /var/app
COPY . /var/app/.
EXPOSE 80/tcp
RUN pip install -r requirements.txt
RUN export FLASK_APP=app.py
RUN export MODULE_NAME="app"
RUN export VARIABLE_NAME="app"
CMD ["waitress-serve","--listen=*:80","app:app"]
