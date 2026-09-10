from pathlib import Path
import json
from schemas import comment

def make_comment(author: str,content):
    """
    Ajoute un commentaire.
    Parameters
    ----------
    author : str
        Auteur du commentaire.
    content : str
        Contenu du commentaire.
    Returns
    -------
    comment
        Commentaire créé.
    """
    path = Path("C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\comment\\comments.json")
    comments = json.loads(path.read_text(encoding="utf-8"))
    dernier_id = len(comments)+1
    new_comment=comment(id=dernier_id,author=author,content=content)
    new_comment_json={"id": dernier_id,"author": author,"content": content}
    comments.append(new_comment_json)
    with path.open("w", encoding="utf-8") as file:
        json.dump(comments,file,ensure_ascii=False,indent=2)
    return new_comment

def read_comment():
    """
    Récupère les commentaires.
    Returns
    -------
    list
        Liste des commentaires.
    """
    path = Path("C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\comment\\comments.json")
    with path.open("r",encoding="utf-8") as file:
        saved_comments=json.load(file)
    return saved_comments

def delete_comment(comment_id: int):
    """
    Supprime un commentaire.
    Parameters
    ----------
    comment_id : int
        ID du commentaire.
    """
    path = Path("C:\\Users\\Paco Tiberghien\\iCloudDrive\\Esilv\\année 4\\computerscience\\backend\\comment\\comments.json")
    comments=json.loads(path.read_text(encoding="utf-8"))
    comments=[comment for comment in comments if comment["id"] != comment_id]
    with path.open("w",encoding="utf-8") as file:
        json.dump(comments,file,ensure_ascii=False,indent=2)