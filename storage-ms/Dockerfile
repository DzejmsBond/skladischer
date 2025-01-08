FROM python:3.12

LABEL authors="Jure"

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r dependencies.txt

EXPOSE 8000

RUN useradd app
USER app

CMD ["python", "-m", "app.main"]
#ENTRYPOINT ["top", "-b"]
# TODO: create with docker init.