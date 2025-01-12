FROM python:3.12

LABEL authors="Jure"

WORKDIR /app

COPY storage-ms /app
COPY proto /app/proto

RUN export PYTHONPATH=. && pip install --no-cache-dir -e ./proto

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

RUN useradd app
USER app

CMD ["python", "-m", "app.main"]
#ENTRYPOINT ["top", "-b"]
# TODO: create with docker init.