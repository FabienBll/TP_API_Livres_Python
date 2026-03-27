# 📚 API Réseau Social de Livres

Une API RESTful basique développée en Python avec **FastAPI**, simulant le backend d'un réseau social de livres (style Goodreads). 
Ce projet a été réalisé dans le cadre d'un cours de conception et d'architecture d'API.

## ✨ Fonctionnalités

L'API respecte les standards REST et permet de gérer les entités suivantes :

* **Livres (Books) :** Création, lecture, mise à jour, suppression (CRUD) et recherche par titre.
* **Avis (Reviews) :** Consultation et ajout d'avis sur un livre spécifique (routes imbriquées).
* **Favoris (Bookmarks) :** Ajout et suppression de livres dans la liste de favoris d'un utilisateur.

> **Note :** Les données sont actuellement stockées en mémoire (listes Python) à des fins de démonstration et seront réinitialisées à chaque redémarrage du serveur.

---

## 🚀 Prérequis

* Python 3.10 ou supérieur
* `pip` (Gestionnaire de paquets Python)
* `python3-venv` (Recommandé pour Linux afin d'éviter les conflits d'environnement)

---

## 🛠️ Installation et Démarrage local

Voici les étapes pour faire tourner cette API sur votre machine locale (instructions adaptées pour Linux/macOS).

**1. Cloner le dépôt**
```bash
git clone [https://github.com/VOTRE_NOM_UTILISATEUR/VOTRE_NOM_DE_REPO.git](https://github.com/VOTRE_NOM_UTILISATEUR/VOTRE_NOM_DE_REPO.git)
cd VOTRE_NOM_DE_REPO
