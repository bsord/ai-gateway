FROM python:3.11

# 
WORKDIR /code

#
RUN apt-get -y update
RUN apt-get install -y ffmpeg

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
RUN mv /etc/ImageMagick-6/policy.xml /etc/ImageMagick-6/policy.xml.off

# 
COPY ./ /code

# 
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]