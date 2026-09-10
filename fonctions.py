from schemas import ArticleInfo,Article
from fastapi import HTTPException
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

def create_article(name,content) -> Article:
    
    path=Path(f"C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\articles\\{name}.md")    
    path.write_text(f"#{name} \n\n{content}", encoding="utf-8")
    article=Article(
        name=name,
        articleUrl=getUrlformat(name),
        content=markdown2.markdown(content),
        source=f"#{name} \n\n{content}"
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
def getUrlformat(name) -> str:
    for i in name:
        if i==" ":
            name=name.replace(" ","_")
    return name
def getNameformat(name) -> str:
    for i in name:
        if i=="_":
            name=name.replace("_"," ")
    return name
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
    