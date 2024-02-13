from fastapi import FastAPI
from scraper.scrapers import run_scrapers
from src.index_generator import generate_indexes

app = FastAPI()


@app.get("/scrapers")
async def scraper_endpoint():
    run_scrapers()


@app.get("/vectors")
async def vector_endpoint():
    generate_indexes()
