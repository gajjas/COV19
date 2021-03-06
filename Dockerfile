FROM python:3.8-slim-buster

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY . .
RUN pip install -r requirements.txt

#Expose the dash port
EXPOSE 80

# Run the application:
CMD ["python", "app.py"]