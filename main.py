from fastapi import FastAPI, HTTPException
from fonctions import delete_article, root, listing_article, create_article, edit_article, read_article
from fastapi.middleware.cors import CORSMiddleware
from schemas import Article, ArticleInfo, CreateArticle, PostComment, comment
from comments import delete_comment, make_comment, read_comment


app = FastAPI()


# Route racine
app.get("/")(root)

# Liste des articles
app.get("/list")(listing_article)

# Récupère un article
@app.get("/article/{articleurl}")
def read_article_api(articleurl: str) -> Article:
    try:
        return read_article(articleurl)
    except FileNotFoundError:
        raise HTTPException(404, "file not found")


# Crée un article
@app.post("/create")
def create_articleApi(body: CreateArticle) -> Article:
    return create_article(body.name, body.content, body.author, body.tags, body.category)


app.post("/create")(create_articleApi)

# Modifie un article
app.post("/article/{article_url}/edit")(edit_article)

# Ajoute un commentaire
@app.post("/comments")
def commentsomethinh(comment: PostComment):
    if comment.author != "":
        return make_comment(comment.author, comment.content)
    else:
        return make_comment("Anonymous", comment.content)


# Récupère les commentaires
@app.get("/comments")
def read_com():
    return read_comment()


# Supprime un commentaire
@app.get("/comments/{comment_id}/delete")
def delete_comment_api(comment_id: int):
    try:
        delete_comment(comment_id)
    except FileNotFoundError:
        raise HTTPException(404, "Comment not found")


# Supprime un article
@app.get("/article/{article_url}/delete")
def delete_article_api(article_url: str):
    try:
        delete_article(article_url)
    except FileNotFoundError:
        raise HTTPException(404, "Article not found")


# Active le CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)