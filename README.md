# Strava API

## Start a postgres instance for the first time
How to create the postgres database exposing the 5432 port using docker
```docker run --name my-postgres -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres```

## Launch Fast API
```python -m uvicorn api.main:app --host 0.0.0.0 --reload```
http://localhost:8000/docs#/

## Launch frontend
Go to the frontend folder, there type the code below:
```npm run dev```

## Final result
![Strava APP Frontend](strava-app-frontend.png)