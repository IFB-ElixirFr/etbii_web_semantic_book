# ETBII - Web semantic book

Book of ETBII web semantic session 

- [Book website](https://ifb-elixirfr.github.io/etbii_web_semantic_book/intro.html) 
- [Part of ETBII](https://moodle.france-bioinformatique.fr/course/view.php?id=13) 

Licence

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7550601.svg)](https://doi.org/10.5281/zenodo.7550601)

## :hammer: Build the book 

```bash 
module load jupyter-book
jupyter-book build docs/
```

## :twisted_rightwards_arrows: Shared the book 

```bash 
# Install package
pip install ghp-import

# Shared on a special branch : gh-pages
ghp-import -n -p -f docs/_build/html
```

## :pencil: How to contribute ?

To do 

## :blue_book: Ressources 

- [Create your first Jupyter Book](https://github.com/IFB-ElixirFr/jupyterBook-demo)
- [Official documentation](https://jupyterbook.org/en/stable/intro.html)
