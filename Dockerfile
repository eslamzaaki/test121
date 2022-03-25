FROM python

COPY . /app
WORKDIR /app
RUN ln -s /app/run_tests.sh /usr/local/bin
RUN pip install --upgrade pip
RUN pip install gnupg
RUN pip install python-gnupg
RUN pip install -r requirements.txt
RUN  pytest test_main.py -v

ENTRYPOINT ["gunicorn"  , "-b", ":8080", "main:APP"]
