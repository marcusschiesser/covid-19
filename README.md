# Covid-19 Cases per Country

Simple web dashboard showing the cases per country - written with [Dash](https://plotly.com/dash/) and Python 3.

To run using docker, start:
```
docker build -t dashboard .
PORT=8080 && docker run -p 9090:${PORT} -e PORT=${PORT} dashboard:latest
```

Or run locally using:
```
python app.py
```
