# ETBII - Web semantic book

Book of ETBII web semantic session 

- [Book website](https://ifb-elixirfr.github.io/etbii_web_semantic_book/intro.html) 
- [Part of ETBII](https://moodle.france-bioinformatique.fr/course/view.php?id=13) 

To do : DOI 

## Build the book 

```bash 
module load jupyter-book
jupyter-book build docs/
```

## Shared the book 

```bash 
# Install package
pip install ghp-import

# Shared on a special branch : gh-pages
ghp-import -n -p -f docs/_build/html
```

## How to contribute ?

To do 

## Ressources 

- [Create your first Jupyter Book](https://github.com/IFB-ElixirFr/jupyterBook-demo)
- [Official documentation](https://jupyterbook.org/en/stable/intro.html)
