# ETBII - Web semantic book

Book of ETBII web semantic session 

- [Book website](https://ifb-elixirfr.github.io/etbii_web_semantic_book/intro.html) 
- [Part of ETBII](https://moodle.france-bioinformatique.fr/course/view.php?id=13) 

[![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]
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

## Licence

This project is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/legalcode).

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg
