from pydantic import BaseModel

class Article(BaseModel):
    name:str
    content:str 
    articleUrl:str
    source: str 
class ArticleInfo(BaseModel):
    name:str
    articleUrl: str
class EditArticle(BaseModel):
    name:str
    articleUrl: str

