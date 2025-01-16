FROM python:3.12

LABEL authors="Jure"

WORKDIR /app

COPY admin-ms /app
COPY skladischer_proto /app/skladischer_proto
COPY skladischer_auth /app/skladischer_auth
copy Makefile /app/
ENV GOOGLE_CLOUD_LOGGING=true

RUN export PYTHONPATH=. && pip install --no-cache-dir -r requirements.txt

RUN make clean-proto-files && make generate-proto-files && pip install --no-cache-dir -e ./skladischer_proto && pip install --no-cache-dir -e ./skladischer_auth

EXPOSE 8001

RUN useradd app
USER app

CMD ["python", "-m", "app.main"]
#ENTRYPOINT ["top", "-b"]