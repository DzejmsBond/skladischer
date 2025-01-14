FROM python:3.12

LABEL authors="Jure"

WORKDIR /app

COPY codes-ms /app
COPY proto /app/proto
copy Makefile /app/

RUN export PYTHONPATH=. && pip install --no-cache-dir -r requirements.txt

RUN make clean-proto-files && make generate-proto-files && pip install --no-cache-dir -e ./proto

EXPOSE 8002

RUN useradd app
USER app

CMD ["python", "-m", "app.main"]
#ENTRYPOINT ["top", "-b"]
# TODO: create with docker init.