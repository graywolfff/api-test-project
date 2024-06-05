FROM python:3.12.3-alpine3.20 as builder

RUN apk update && apk add --virtual build-dependencies \
    build-base \
    gcc \
    zlib-dev \ 
    libffi-dev

COPY ./requirements.txt  /requirements.txt

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt

FROM python:3.12.3-alpine3.20

COPY . /app
WORKDIR /app

COPY --from=builder /py /py
COPY --from=builder /usr/lib/lib* /usr/lib/

ENV PATH="/py/bin:$PATH"
