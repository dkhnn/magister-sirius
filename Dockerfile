# Use the Python image
FROM python:3.10

# Set the working directory inside the container to /app
WORKDIR /app

COPY ./requirements.txt .
ENV PYTHONPATH "${PYTHONPATH}:/app"
RUN pip install -r requirements.txt

COPY . .

RUN python liveness.py &
CMD ["python", "-u", "bot.py"]