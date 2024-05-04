# sphinxcontrib-lightbox2

Sphinx extension to add [lightbox2](https://lokeshdhakar.com/projects/lightbox2/) to each figure and image added in HTML.

Usually Sphinx themes limit their content width to a limit to improve readability. This creates a problem for large
images and diagrams which might be needed in technical documentation.

## Installation

Install the package using

```sh
pip install sphinxcontrib-lightbox2
```

Add `sphinxcontrib.lightbox2` to the list of `extensions` in your *conf.py*:

``` python
extensions = ["sphinxcontrib.lightbox2"]
```
