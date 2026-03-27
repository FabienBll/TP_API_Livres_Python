from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

# Création de l'application
app = FastAPI(title="API Réseau Social de Livres")

# --- MODÈLES DE DONNÉES (Pydantic) ---

class Book(BaseModel):
    id: int
    title: str
    author: str

class Review(BaseModel):
    id: int
    book_id: int
    user_id: int
    content: str
    rating: int  # Note sur 5 par exemple

class Bookmark(BaseModel):
    user_id: int
    book_id: int

# --- "BASES DE DONNÉES" (Listes en mémoire) ---
books_db = []
reviews_db = []
bookmarks_db = []

# ==========================================
# 1 & 5. CRUD LIVRES + RECHERCHE PAR TITRE
# ==========================================

# Lire les livres (et gérer la recherche avec ?search=...)
@app.get("/books", response_model=List[Book])
def get_books(search: Optional[str] = None):
    # Si on a tapé ?search=quelquechose, on filtre les résultats
    if search:
        filtered_books = [book for book in books_db if search.lower() in book["title"].lower()]
        return filtered_books

    # Sinon, on renvoie tous les livres
    return books_db

# Lire un seul livre par son ID
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Livre non trouvé")

# Créer un livre
@app.post("/books", status_code=201)
def create_book(new_book: Book):
    books_db.append(new_book.model_dump())
    return {"message": "Livre ajouté", "data": new_book}

# Modifier un livre
@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    for index, b in enumerate(books_db):
        if b["id"] == book_id:
            books_db[index] = updated_book.model_dump()
            return {"message": "Livre modifié", "data": books_db[index]}
    raise HTTPException(status_code=404, detail="Livre non trouvé")

# Supprimer un livre
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, b in enumerate(books_db):
        if b["id"] == book_id:
            deleted_book = books_db.pop(index)
            return {"message": "Livre supprimé", "data": deleted_book}
    raise HTTPException(status_code=404, detail="Livre non trouvé")


# ==========================================
# 2 & 3. GESTION DES AVIS (REVIEWS)
# ==========================================

# Récupérer les avis d'un livre spécifique
@app.get("/books/{book_id}/reviews", response_model=List[Review])
def get_book_reviews(book_id: int):
    # On filtre la liste des avis pour ne garder que ceux de ce livre
    book_reviews = [review for review in reviews_db if review["book_id"] == book_id]
    return book_reviews

# Laisser un avis sur un livre
@app.post("/books/{book_id}/reviews", status_code=201)
def add_review(book_id: int, new_review: Review):
    # On s'assure que l'ID du livre dans l'URL correspond à l'avis
    new_review.book_id = book_id
    reviews_db.append(new_review.model_dump())
    return {"message": "Avis ajouté avec succès", "data": new_review}


# ==========================================
# 4. GESTION DES BOOKMARKS (FAVORIS)
# ==========================================
# Ici on choisit l'approche "Un utilisateur ajoute un livre à ses favoris"

# Ajouter un livre aux bookmarks d'un utilisateur
@app.post("/users/{user_id}/bookmarks", status_code=201)
def add_bookmark(user_id: int, bookmark_data: Bookmark):
    # On force l'ID de l'utilisateur venant de l'URL
    bookmark_data.user_id = user_id
    bookmarks_db.append(bookmark_data.model_dump())
    return {"message": "Livre ajouté aux favoris"}

# Supprimer un livre des bookmarks d'un utilisateur
@app.delete("/users/{user_id}/bookmarks/{book_id}")
def remove_bookmark(user_id: int, book_id: int):
    for index, b in enumerate(bookmarks_db):
        if b["user_id"] == user_id and b["book_id"] == book_id:
            bookmarks_db.pop(index)
            return {"message": "Livre retiré des favoris"}

    raise HTTPException(status_code=404, detail="Favori non trouvé")

# Lancement du serveur
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
