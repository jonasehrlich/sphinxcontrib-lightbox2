<!-- markdownlint-disable MD041 -->

:::{include} ../README.md
:end-before: "## Examples"
:::

## Examples

### Figure

:::{figure} large-diagram.drawio.svg
Diagram with multiple components
:::

### Image

:::{image} large-diagram.drawio.svg
:::

### PlantUML diagram

::: {warning}
The lightbox does not work with the *plantuml_output_format* `svg_obj`. All other formats are supported.
:::

:::{uml} sequence-chart.puml
:caption: Caption with **bold** and *italic*
:::
