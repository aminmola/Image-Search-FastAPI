#RUN apt-get update
#COPY ./requirements.txt /code/requirements.txt
#RUN pip install --upgrade -r /code/requirements.txt
#COPY ./ /code/
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "2468"]
#CMD ["python","api/main.py"]
#############################################################################
# Use the Python 3.9 image
#FROM python:3.9-slim-buster
# Set the working directory to /Ezshop/IDAS
#WORKDIR /code
# Copy the current directory contents into the container at /Ezshop/ctas
#COPY requirements.txt requirements.txt
#ENV FLASK_APP=app.py
#ENV FLASK_RUN_HOST=0.0.0.0
#RUN pip install --upgrade pip
#Pip command without proxy setting
#RUN pip install -r requirements.txt
# Expose port 4040
#EXPOSE 4040
#COPY . .
#CMD ["python", "api/main.py"]



#
FROM python:3.9-slim-buster

#
WORKDIR /code


RUN apt-get update
#

COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./ /code/

#
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "2468"]
CMD ["python","main.py"]
