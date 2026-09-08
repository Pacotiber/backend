from fastapi import FastAPI
from fonctions import root, listing_article, create_article, edit_article, read_article
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.get("/")(root)
app.get("/list")(listing_article)
app.get("/article/{articleurl}")(read_article)
app.post("/create")(create_article)
app.post("/article/{article_url}/edit")(edit_article)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)