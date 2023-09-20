FROM python:3.9.14-bullseye

COPY app app
RUN pip3 install -r /app/requirement.txt
RUN cat app/certs/cacert.pem >> /usr/local/lib/python3.9/site-packages/certifi/cacert.pem

# per rispolvere momentaneamente il problema del resurce_access
RUN cat app/files/api.py > /usr/local/lib/python3.9/site-packages/fastapi_keycloak/api.py


WORKDIR /app
CMD ["/usr/local/bin/python", "main.py"]

## Se si vuole avviare il docker senza lanciare il main
# CMD ["tail", "-f", "/dev/null"]