FROM python:3.12

LABEL authors="Jure"

WORKDIR /app

COPY admin-ms /app
COPY proto /app/proto
COPY auth /app/auth
copy Makefile /app/

RUN export PYTHONPATH=. && pip install --no-cache-dir -r requirements.txt

RUN make clean-proto-files && make generate-proto-files && pip install --no-cache-dir -e ./proto && pip install --no-cache-dir -e ./auth

EXPOSE 8001

RUN useradd app
USER app

CMD ["python", "-m", "app.main"]
#ENTRYPOINT ["top", "-b"]