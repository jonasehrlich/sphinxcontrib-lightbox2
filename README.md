# sphinxcontrib-lightbox2

Sphinx extension to add [lightbox2](https://lokeshdhakar.com/projects/lightbox2/) to each figure and image added in HTML.

---

**[Read the documentation on ReadTheDocs!](https://sphinxcontrib-lightbox2.readthedocs.io/)**

---

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

## Configuration

Lightbox2 offers different configuration [options](https://lokeshdhakar.com/projects/lightbox2/#options).
These options are exposed in `sphinxcontrib-lightbox2` through options in the *conf.py*.

See the mapping of lightbox2 options to Sphinx options

| Lightbox2 Option Name | Sphinx Option Name | Default Value |
| ----------------------|--------------------|---------------|
| `alwaysShowNavOnTouchDevices` | `lightbox2_always_show_nav_on_touch_devices` | `False` |
| `albumLabel` | `lightbox2_album_label` | `"Image %1 of %2"` |
| `disableScrolling` | `lightbox2_disable_scrolling`| `False` |
| `fadeDuration` | `lightbox2_fade_duration`| `600` |
| `fitImagesInViewport` | `lightbox2_fit_images_in_viewport`| `True` |
| `imageFadeDuration` | `lightbox2_image_fade_duration`| `600` |
| `maxWidth` | `lightbox2_max_width`| `None` |
| `maxHeight` | `lightbox2_max_height`| `None` |
| `positionFromTop` | `lightbox2_position_from_top`| `50` |
| `resizeDuration` | `lightbox2_resize_duration`| `700` |
| `showImageNumberLabel` | `lightbox2_show_image_number_label`| `True` |
| `wrapAround` | `lightbox2_wrap_around`| `True` |

<!-- README is only included in documentation until here -->

## Examples

See the examples in the [documentation](https://sphinxcontrib-lightbox2.readthedocs.io/#examples).
