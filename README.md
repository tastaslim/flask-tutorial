# Introduction #
A basic flask based stores app which keeps stores all information of nearby stores, items, item tags and user present.

# Features #

- Security is provided to application using JWT token, API-keys, CORS, SQL Injection etc protected. Supports Access and Refresh token concepts.
- Sends Email for successful login and deletion operations
- Supports Caching Using Redis
- Supports Auto Scaling 
- Has DB Migration feature to avoid DB schema change handing pain

# Technologies Used #

- Postgres
- Python
- Flask
- Redis
- MailGun
- AWS SQS
- Swagger
  
# How to Run Application #

```text
flask run
```

# How to use #

- Once Application is up. Redirect to **/v1/swagger/** endpoint to see all available APIs. Provide x-api-key.
- Login with user credentials and get access token.
- Play with all APIs using access token and x-api-key.