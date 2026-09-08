from schemas import ArticleInfo,Article
from fastapi import FastAPI, HTTPException
from pathlib import Path
import markdown2
from urllib.parse import unquote

def root() ->dict[str,str]:
    return {"message":"It works"}

def listing_article() -> list[ArticleInfo]:
    
    articles_path = Path('C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\articles')
    articles = [i.stem for i in articles_path.iterdir()]
    jsonp=[]
    for i in articles:
        jsonp.append(ArticleInfo(name=getNameformat(i),articleUrl=i))
    return jsonp

def create_article(body :dict) -> Article:
    if(len(body["content"])>1000):
            raise HTTPException(400,"Text is too long")
    if(len(body["name"])>100):
            raise HTTPException(400,"name is too long")
    if(len(body["name"])<1):
            raise HTTPException(400,"name is too short")
    if(len(body["content"])<1):
            raise HTTPException(400,"Text is too short")
    if(".." in body["name"]):
            raise HTTPException(400,"name is not valid")
    
    path=Path(f"C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\articles\\{body["name"]}.md")
    content=body["content"]
    
    path.write_text(f"#{body["name"]} \n\n{content}", encoding="utf-8")
    
    article=Article(
        name=body["name"],
        articleUrl=getUrlformat(body["name"]),
        content=markdown2.markdown(content),
        source=f"#{body["name"]} \n\n{content}"
    )
    return article

def edit_article(body: dict, article_url):
    path = Path(
        f"C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\articles\\{article_url}.md"
    )

    content = body["content"]

    path.write_text(
        f"#{article_url} \n\n{content}",
        encoding="utf-8"
    )
def read_article(articleurl: str)-> Article:
    articleurl = unquote(articleurl)

    file_path = Path(
        f"C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\articles\\{articleurl}.md"
    )  
    try:
        content = file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Article not found")

    html = markdown2.markdown(content)
    article=Article(
        name=getNameformat(file_path.stem),
        articleUrl=articleurl,
        content=html,
        source=content
    )
    return article
    