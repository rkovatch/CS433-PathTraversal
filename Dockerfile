FROM python:3.13-alpine
LABEL maintainer="rkovatch@uoregon.edu"
COPY static /static
COPY templates /templates
COPY photos /photos
COPY requirements.txt requirements.txt
COPY web_server.py web_server.py
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "-m"]
CMD ["flask", "--app", "web_server", "--debug", "run", "--host=0.0.0.0"]
