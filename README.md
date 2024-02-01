## QUICKBOOK ONLINE API
#### 1. Create and Start Developing Your App
- If you haven't created an app yet, please log in to your developer account and proceed to create a new app.
- If you already have an app, redirect to the following link: `https://developer.intuit.com/app/developer/playground` (log in to your developer account if not already logged in). Next, select the app for which you want to retrieve data and choose the necessary scopes.
- Upon completing these steps, you will obtain information such as client_id, client_secret, Realm ID, access token, and refresh token. In the next step, populate the above information to match the settings.py file.
#### 2. Retrieve Information from the API and Push it into GPQ
- To push data to the GPB table, you will need the service_account file which is CREATE TABLE permissions for GBQ. Populate its content into the corresponding variable in the settings.py file.
#### 3. Running
- Clone project `https://github.com/duc-dn/quickbook_api.git`
- Begin by creating a virtual environment: `python -m venv venv` and activate virtual enviroment
- Install the required libraries: `pip install -r requirements.txt`.
- Run the main file: `python -m src.main`. After successfully executing the code, verify the table on GPB.

#### 4. Shedule Job
- To setup run automatically, use crontab of ubuntu

#### 5. Note
- If you face below error, it can refresh token is changed
```
intuitlib.exceptions.AuthClientError: HTTP status 400, error message: b'{"error":"invalid_grant"}'
```
- I think that you should get again `access_token` and `refresh_token` in link `https://developer.intuit.com/app/developer/playground`


#### 6. Pivot table
- Balance Sheet
```
SELECT Time, ReportName, ReportBasis, StartPeriod, EndPeriod, SummarizeColumnsBy, Currency, Field, conversion_name, conversion_value 
FROM `radar-377104.api_connection.quickbook_balance_sheet`
UNPIVOT(conversion_value FOR conversion_name IN 
(Aug2023, Sep2023, Oct2023, Nov2023, Dec2023, Jan2024))
```

- Profit and Loss
```
SELECT Time, ReportName, ReportBasis, StartPeriod, EndPeriod, SummarizeColumnsBy, Currency, Field, conversion_name, conversion_value 
FROM `radar-377104.api_connection.quickbook_profit_and_loss`
UNPIVOT(conversion_value FOR conversion_name IN 
(Aug2023, Sep2023, Oct2023, Nov2023, Dec2023, Jan2024, Total))
```

- Cash Flow
```
SELECT Time, ReportName, StartPeriod, EndPeriod, SummarizeColumnsBy, Currency, Field, conversion_name, conversion_value 
FROM `radar-377104.api_connection.quickbook_cash_flow`
UNPIVOT(conversion_value FOR conversion_name IN 
(Aug2023, Sep2023, Oct2023, Nov2023, Dec2023, Jan2024, Total))
```