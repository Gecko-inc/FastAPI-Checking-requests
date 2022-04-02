FROM python:3.9

RUN mkdir /api_token

WORKDIR /api_token

# Copy the current directory contents into the container at /music_service
ADD . /api_token/

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]

