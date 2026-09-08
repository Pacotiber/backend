from fastapi import FastAPI
from pathlib import Path
import markdown2
from urllib.parse import unquote
import json
# Convert Markdown text to HTML

app =FastAPI()
@app.get("/")
def root() ->dict[str,str]:
    return {"message":"It works"}
@app.get("/list")
def listing_article():
    
    articles_path = Path('C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\articles')
    articles = [i.stem for i in articles_path.iterdir()]
    jsonp=[]
    for i in articles:
        jsonp.append({"name":i,"articleUrl":getUrlformat(i)})
    return jsonp
def getUrlformat(name):
    for i in name:
        if i==" ":
            i="_"
    return name
def getNameformat(name):
    for i in name:
        if i=="_":
            i=" "
    return name

@app.get("/article/{articleurl}")
def read_article(articleurl: str):
    articleurl = unquote(articleurl)

    file_path = Path(
        f"C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\articles\\{articleurl}.md"
    )

    content = file_path.read_text(encoding="utf-8")
    html = markdown2.markdown(content)

    return {
        "name": getNameformat(file_path.stem),
        "articleUrl": articleurl+".md",
        "content": html,
        "source": content
    }

@app.post("/create")
def create_article(body :dict):
    path=Path(f"C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\articles\\{body["name"]}.md")
    content=body["content"]
    path.write_text(f"#{body["name"]} \n\n{content}", encoding="utf-8")
    return{
        "name":body["name"],
        "articleUrl": getUrlformat(body["name"]),
        "content":markdown2.markdown(content),
        "source": "# My article\n\nMarkdown source."
    }   

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)