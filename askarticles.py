from fonctions import *
def askarticles():
    """
    This function retrieves articles based on user queries.
    It connects to a database or an API to fetch relevant articles.
    """
    # Placeholder for the actual implementation
    is_valid =False
    while not is_valid:
        try :
            query=input("choose your article")
            article=read_article(query)
            print(article.content)
        except HTTPException:
            print("the file dont exiits")
        else :
            is_valid=True

askarticles()

