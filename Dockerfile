# Separate build image
FROM python:3.10.12-slim-bullseye as compile-image
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
COPY requirements.txt .

RUN apt-get update
RUN apt-get install -y gcc
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -rf /var/lib/apt/lists/*

# Final image
FROM python:3.10.12-slim-bullseye
COPY --from=compile-image /venv /venv
ENV PATH="/venv/bin:$PATH"
COPY DatingApp /app/data
WORKDIR /app/data
EXPOSE 8000
CMD [ "python", "DatingApp/manage.py", "runserver", "0.0.0.0:8000", "--noreload" ]
