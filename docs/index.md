<!-- markdownlint-disable MD041 -->

:::{include} ../README.md
:end-before: "## Examples"
:::

## Examples

These examples show how the *lightbox2*  applied to the images look. Click on any of the images to see the effect.

### Figure

The following diagram is a normal figure included using the standard `figure` directive.

:::::{dropdown} Syntax
::::{tab-set-code}

```` markdown
```{figure} large-diagram.drawio.svg
Diagram with multiple components
```
````

``` rst
.. figure:: large-diagram.drawio.svg
   Diagram with multiple components

```

::::
:::::

:::{figure} large-diagram.drawio.svg
Diagram with multiple components
:::

### Image

Use a normal image directive to add the behavior to images.

:::::{dropdown} Syntax
::::{tab-set-code}

```` markdown
```{image} large-diagram.drawio.svg
```
````

``` rst
.. image:: large-diagram.drawio.svg
```

::::
:::::

:::{image} large-diagram.drawio.svg
:::

### PlantUML diagram

::: {warning}
The lightbox does not work with the *plantuml_output_format* `svg_obj`. All other formats are supported.
:::

Use the `uml` directive from the `sphinxcontrib.plantuml` extension to add the effect to PlantUML diagrams.

:::::{dropdown} Syntax
::::{tab-set-code}

```` markdown
```{uml} sequence-chart.puml
:caption: Caption with **bold** and *italic*
```
````

``` rst
.. uml:: large-diagram.drawio.svg
```

::::
:::::

:::{uml} sequence-chart.puml
:caption: Caption with **bold** and *italic*
:::
