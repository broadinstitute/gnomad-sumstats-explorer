# gnomAD summary statistics Shiny app explorer
This is a Shiny app that allows you to explore the gnomAD individual level summary
statistics. The app is available at [FILL ME IN](FILL ME IN).

## Running locally
### Install required packages
```bash
pip install -r requirements.txt
```

### Run the app locally
```bash
shiny run gnomad_sumstats_explorer/app.py
```

You should see a message like this:
```
INFO:     Started server process [43622]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

In your browser, navigate to the URL in the last line of the output (in this
case, `http://127.0.0.1:8000`).
