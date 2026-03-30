import json
import os
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="API Réseau Social de Livres")

# --- GESTION DU FICHIER JSON ---

# On définit le chemin du fichier "database.json" dans le même dossier que ce script
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.json")

def load_db():
    """Charge les données depuis le fichier JSON. S'il n'existe pas, retourne une structure vide."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {"books": [], "reviews": [], "bookmarks": []}

def save_db():
    """Sauvegarde l'état actuel des listes dans le fichier JSON."""
    data = {
        "books": books_db,
        "reviews": reviews_db,
        "bookmarks": bookmarks_db
    }
    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# Chargement initial des données au démarrage du serveur
db = load_db()
books_db = db["books"]
reviews_db = db["reviews"]
bookmarks_db = db["bookmarks"]


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
    rating: int

class Bookmark(BaseModel):
    user_id: int
    book_id: int


# ==========================================
# 1 & 5. CRUD LIVRES + RECHERCHE PAR TITRE
# ==========================================

@app.get("/books", response_model=List[Book])
def get_books(search: Optional[str] = None):
    if search:
        return [book for book in books_db if search.lower() in book["title"].lower()]
    return books_db

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Livre non trouvé")

@app.post("/books", status_code=201)
def create_book(new_book: Book):
    books_db.append(new_book.model_dump())
    save_db() # <-- Sauvegarde dans le fichier !
    return {"message": "Livre ajouté", "data": new_book}

@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    for index, b in enumerate(books_db):
        if b["id"] == book_id:
            books_db[index] = updated_book.model_dump()
            save_db() # <-- Sauvegarde dans le fichier !
            return {"message": "Livre modifié", "data": books_db[index]}
    raise HTTPException(status_code=404, detail="Livre non trouvé")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, b in enumerate(books_db):
        if b["id"] == book_id:
            deleted_book = books_db.pop(index)
            save_db() # <-- Sauvegarde dans le fichier !
            return {"message": "Livre supprimé", "data": deleted_book}
    raise HTTPException(status_code=404, detail="Livre non trouvé")


# ==========================================
# 2 & 3. GESTION DES AVIS (REVIEWS)
# ==========================================

@app.get("/books/{book_id}/reviews", response_model=List[Review])
def get_book_reviews(book_id: int):
    return [review for review in reviews_db if review["book_id"] == book_id]

@app.post("/books/{book_id}/reviews", status_code=201)
def add_review(book_id: int, new_review: Review):
    new_review.book_id = book_id
    reviews_db.append(new_review.model_dump())
    save_db() # <-- Sauvegarde dans le fichier !
    return {"message": "Avis ajouté avec succès", "data": new_review}


# ==========================================
# 4. GESTION DES BOOKMARKS (FAVORIS)
# ==========================================

@app.post("/users/{user_id}/bookmarks", status_code=201)
def add_bookmark(user_id: int, bookmark_data: Bookmark):
    bookmark_data.user_id = user_id
    bookmarks_db.append(bookmark_data.model_dump())
    save_db() # <-- Sauvegarde dans le fichier !
    return {"message": "Livre ajouté aux favoris"}

@app.delete("/users/{user_id}/bookmarks/{book_id}")
def remove_bookmark(user_id: int, book_id: int):
    for index, b in enumerate(bookmarks_db):
        if b["user_id"] == user_id and b["book_id"] == book_id:
            bookmarks_db.pop(index)
            save_db() # <-- Sauvegarde dans le fichier !
            return {"message": "Livre retiré des favoris"}
    raise HTTPException(status_code=404, detail="Favori non trouvé")

# Lancement du serveur
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
