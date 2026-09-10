
from schemas import ArticleInfo, Article, CreateArticle, comment
from fastapi import HTTPException
from pathlib import Path
import markdown2
from urllib.parse import unquote
import json


def root() -> dict[str, str]:
    """
    Return the API welcome message.

    Returns
    -------
    dict[str, str]
        A dictionary containing the API status message.
    """
    return {"message": "It works"}


def listing_article() -> list[ArticleInfo]:
    """
    List all active articles.

    Returns
    -------
    list[ArticleInfo]
        A list containing the name and URL of each article.
    """
    articles_path = Path(
        'C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\articles'
    )
    articles = [i.stem for i in articles_path.iterdir()]
    jsonp = []

    for i in articles:
        jsonp.append(ArticleInfo(name=getNameformat(i), articleUrl=i))

    return jsonp


def create_article(name, content, author, tags, category) -> Article:
    """
    Create and save a new Markdown article.

    Parameters
    ----------
    name : str
        Name of the article.
    content : str
        Markdown content of the article.

    Returns
    -------
    Article
        The created article with its HTML content and source.
    """
    path = Path(
        f"C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\articles\\{getUrlformat(name)}.md"
    )   
    print(f"Creating article at: {path}")
    print(getUrlformat(name))
    path_metadata = Path(
        f"C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\metadata\\{getUrlformat(name)}.json")
    with path_metadata.open("w", encoding="utf-8") as file:
        json.dump({"author": author, "tags": tags, "category": category}, file, ensure_ascii=False, indent=2)
    article = Article(
        name=name,
        articleUrl=getUrlformat(name),
        content=markdown2.markdown(content),
        source=f"#{name} \n\n{content}",
        author=author,
        tags=tags,
        category=category
    )


    path.write_text(f"#{name} \n\n{content}", encoding="utf-8")

    return article


def edit_article(body: dict, article_url):
    """
    Update an existing article and its metadata.

    Parameters
    ----------
    body : dict
        Dictionary containing the article content and metadata.
    article_url : str
        URL-formatted identifier of the article to edit.
    """
    path = Path(
        f"C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\articles\\{article_url}.md"
    )

    content = body["content"]

    path.write_text(
        f"{content}",
        encoding="utf-8"
    )

    metadata_dir = Path(
        f"C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\metadata\\{article_url}.json"
    )

    metadata = {
        "author": body.get("author", "Unknown"),
        "tags": body.get("tags", []),
        "category": body.get("category", "Uncategorized")
    }

    with metadata_dir.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, ensure_ascii=False, indent=2)

def getUrlformat(name) -> str:
    """
    Convert spaces in an article name to underscores.

    Parameters
    ----------
    name : str
        Article name to format.

    Returns
    -------
    str
        Article name with spaces replaced by underscores.
    """
    for i in name:
        if i == " ":
            name = name.replace(" ", "_")

    return name


def getNameformat(name) -> str:
    """
    Convert underscores in an article name to spaces.

    Parameters
    ----------
    name : str
        Article name to format.

    Returns
    -------
    str
        Article name with underscores replaced by spaces.
    """
    for i in name:
        if i == "_":
            name = name.replace("_", " ")

    return name


def read_metadata(articleurl: str) -> dict:
    """
    Read the metadata associated with an article.

    Parameters
    ----------
    articleurl : str
        URL-formatted identifier of the article.

    Returns
    -------
    dict
        Article metadata containing the author, tags and category.
        Default values are returned if the metadata file does not exist.
    """
    article_dir = Path(
        f"C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\metadata\\{articleurl}.json"
    )

    if article_dir.exists():
        with article_dir.open("r", encoding="utf-8") as file:
            saved_metadata = json.load(file)
    else:
        return {
            "author": "Unknown",
            "tags": [],
            "category": "Uncategorized"
        }

    return saved_metadata


def read_article(articleurl: str) -> Article:
    """
    Read an article and convert its Markdown content to HTML.

    Parameters
    ----------
    articleurl : str
        URL-formatted identifier of the article.

    Returns
    -------
    Article
        Article containing its name, URL, HTML content, source and metadata.
    """
    articleurl = unquote(articleurl)
    print(f"Reading article: {articleurl}")

    file_path = Path(
        f"C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\articles\\{articleurl}.md"
    )

    content = file_path.read_text(encoding="utf-8")
    html = markdown2.markdown(content)

    article = Article(
        name=getNameformat(file_path.stem),
        articleUrl=articleurl,
        content=html,
        source=content,
        author=read_metadata(articleurl)["author"],
        tags=read_metadata(articleurl)["tags"],
        category=read_metadata(articleurl)["category"]
    )

    return article


def delete_article(articleurl: str):
    """
    Move an article and its metadata to the trash directory.

    If an article or metadata file with the same name already exists
    in the trash, the existing files are deleted before moving the
    new ones.

    Parameters
    ----------
    articleurl : str
        URL-formatted identifier of the article to move to trash.

    Returns
    -------
    dict
        Confirmation indicating that the article was successfully deleted.
    """
    source = Path(
        f"C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\articles\\{articleurl}.md"
    )
    destination = Path(
        f"C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\trash\\{articleurl}.md"
    )
    source_metadata = Path(
        f"C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\metadata\\{articleurl}.json"
    )
    destination_metadata = Path(
        f"C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\trash\\{articleurl}.json"
    )
    if destination.exists():
        destination.unlink()
    source.rename(destination)
    if(source_metadata.exists()):
        if destination_metadata.exists():
            destination_metadata.unlink()
        source_metadata.rename(destination_metadata)

    return {"deleted": True}
