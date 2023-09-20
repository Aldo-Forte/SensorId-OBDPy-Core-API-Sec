from fastapi_keycloak import FastAPIKeycloak, OIDCUser

idp = FastAPIKeycloak(
    server_url="https://auth.sensorid.it:8443",
    client_id="obd-client",
    client_secret="d9XXWgMN1WrNnZLCy02FCh6FwebL401H",
    admin_client_secret="SK7jPsFFONklEU2pdyBDz9D3c4tsMf6b",
    realm="OBD",
    callback_uri="https://obd-dev.sensorid.it:8010/callback"
)

# idp.add_swagger_config(app)