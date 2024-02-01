# For sandbox and testing environments
BASE_URL = "https://sandbox-quickbooks.api.intuit.com"

# For production environment
# BASE_URL = "https://quickbooks.api.intuit.com"

CREDENTIALS = {
    "realm_id": "",
    "refresh_token": "",
    "access_token": "",
}

CLIENT_SECRET = {
    "client_id": "",
    "client_secret": "Tdm4gGSqgp3ogMKejL6AKNJ34607F8O7y4eJytVp",
    "redirect_uri": "",
    "environment": "",  # sandbox or production
}

# service account file which has create table permission in bigquery
BIGQUERY_CREDETIALS = {}
