# Eco-Prix Yaoundé / TP INF232

Application de gestion intelligente des sessions d'achats.

## Diagramme de classe - Produits les plus achetés

```mermaid
classDiagram
    class Produit {
        +string nom
        +float prix
        +string categorie
    }
    class Achat {
        +int quantite
        +date date
    }
    class TopProduits {
        +calculerTop10()
    }
    Produit "1" -- "*" Achat
    TopProduits --> Produit
```

## Installation

```bash
pip install flask
python app.py
```

## Auteur

Votre nom
