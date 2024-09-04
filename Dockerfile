# Use the Python image
FROM python:3.10

# Set the working directory inside the container to /app
WORKDIR /app

COPY ./requirements.txt .
ENV PYTHONPATH "${PYTHONPATH}:/app"
RUN pip install -r requirements.txt

# Download the AWS DocumentDB Root CA bundle
RUN wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem -O /etc/ssl/certs/rds-combined-ca-bundle.pem


COPY . .

RUN python liveness.py &
CMD ["python", "-u", "bot.py"]