FROM python:3.9-slim

WORKDIR /usr/src/app

RUN pip install --no-cache-dir \
        google-ads \
        environs \
        psycopg2-binary

COPY . .

CMD [ "python", "./report_conversions.py" ]
