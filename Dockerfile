FROM python:3.10.15-slim 

# Set working directory in the container and copy the contents of current directory
WORKDIR /app
COPY . ./app/

# Install packages specified in requirements.txt

RUN pip install --upgrade pip && pip install -r ./app/requirements.txt

# Expose the port that Django will run on
EXPOSE 8000

# Run Django development server ( for development purposes )
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
