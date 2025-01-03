FROM python:3.11

RUN addgroup --system app && adduser --system --ingroup app app
WORKDIR /home/app
RUN chown app:app -R /home/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY data data
COPY gnomad_sumstats_explorer gnomad_sumstats_explorer

EXPOSE 8000

USER app
ENV PYTHONPATH="."
CMD [ "shiny", "run", "--host", "0.0.0.0", "--port", "8000", "gnomad_sumstats_explorer/app.py" ]
