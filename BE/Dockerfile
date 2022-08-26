FROM python:3.9

# Set default directory
WORKDIR /code

# Create ENV for image
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# Copy files to image
COPY ./requirements.txt /code/requirements.txt
COPY . /code
COPY .env /code/app

# Remove tests folder
RUN rm -rf /code/tests

# Install requirements
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Run app and expose to 8000
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]