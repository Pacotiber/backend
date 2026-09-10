from pydantic import BaseModel,Field


class Article(BaseModel):
    name:str
    content:str 
    articleUrl:str
    source: str 
    author: str = Field(default="Unknown")
    tags: list[str] = Field(default_factory=list)
    category: str = Field(default="Uncategorized")


class CreateArticle(BaseModel):
    name: str = Field(
    min_length=1,
    max_length=100,
    pattern=r"^[^.]+$")
    content: str=Field(min_length=1,max_length=10000)
    author: str = Field(default="Unknown")
    tags: list[str] = Field(default_factory=list)
    category: str = Field(default="Uncategorized")
    
class ArticleInfo(BaseModel):
    name:str
    articleUrl: str
class EditArticle(BaseModel):
    name:str
    articleUrl: str
    

class comment(BaseModel):
    id:int
    author:str
    content:str

class PostComment(BaseModel):
    author:str=Field(
    max_length=100,
    default="Anonymous",
    pattern=r"^[^.]*$")
    content:str =Field(min_length=1,
        max_length=500)
