import importlib.metadata
import pathlib
from docutils import nodes
import urllib.parse
import posixpath
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.util import display, osutil
from sphinx.util.typing import ExtensionMetadata
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.writers.html5 import HTML5Translator

try:
    import sphinxcontrib.plantuml

    __PLANTUML_AVAILABLE__ = True

except ImportError:
    __PLANTUML_AVAILABLE__ = False

try:
    # Poetry requires the version to be defined in pyproject.toml, load the version from the metadata,
    # this is the recommended approach https://github.com/python-poetry/poetry/pull/2366#issuecomment-652418094
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:  # pragma: no cover
    # No metadata is available, this could be because the tool is running from source
    __version__ = "unknown"

STATIC_FILES = (
    pathlib.Path("assets/images/close.png"),
    pathlib.Path("assets/images/next.png"),
    pathlib.Path("assets/images/prev.png"),
    pathlib.Path("assets/images/loading.gif"),
    pathlib.Path("assets/js/lightbox-plus-jquery.min.js"),
    pathlib.Path("assets/js/lightbox-plus-jquery.min.map"),
    pathlib.Path("assets/css/lightbox.min.css"),
)


def start_lightbox_anchor(self: HTML5Translator, uri: str):
    """
    Write the start of a lightbox anchor to the body
    """
    self.body.append(f"""<a href="{uri}" data-lightbox="image-set">\n""")


def end_lightbox_anchor(self: HTML5Translator, node: nodes.Element):
    self.body.append("</a>\n")


def install_static_files(app: Sphinx, env: BuildEnvironment) -> None:
    static_dir = pathlib.Path(app.builder.outdir) / app.config.html_static_path[0]
    dest_path = pathlib.Path(static_dir)

    for source_file_path in display.status_iterator(
        STATIC_FILES,
        "Copying static files for sphinxcontrib-lightbox2...",
        "brown",
        len(STATIC_FILES),
    ):
        dest_file_path = dest_path / source_file_path.relative_to(*source_file_path.parts[:1])
        osutil.ensuredir(dest_file_path.parent)

        source_file_path = pathlib.Path(__file__).parent / source_file_path
        osutil.copyfile(source_file_path, dest_file_path)

        if dest_file_path.suffix == ".js":
            app.add_js_file(str(dest_file_path.relative_to(static_dir)))
        elif dest_file_path.suffix == ".css":
            app.add_css_file(str(dest_file_path.relative_to(static_dir)))


def html_visit_plantuml(self: HTML5Translator, node: nodes.Element):

    if "html_format" in node:
        fmt = node["html_format"]
    else:
        fmt = self.builder.config.plantuml_output_format

    with sphinxcontrib.plantuml._prepare_html_render(self, fmt, node) as (fileformats, _):
        refnames = [sphinxcontrib.plantuml.generate_name(self, node, fileformat)[0] for fileformat in fileformats]

    self.body.append(f"""<a href="{refnames[0]}" data-lightbox="image-set">\n""")
    try:
        sphinxcontrib.plantuml.html_visit_plantuml(self, node)
    except nodes.SkipNode:
        # Catch the SkipNode exception so that the depart_* function is not entered
        raise
    finally:
        # But the anchor element still needs to be closed
        end_lightbox_anchor(self, node)


def html_visit_image(self: HTML5Translator, node: nodes.Element) -> None:

    olduri = node["uri"]
    # Rewrite the URI if the environment knows about it
    if olduri in self.builder.images:
        node["uri"] = posixpath.join(self.builder.imgpath, urllib.parse.quote(self.builder.images[olduri]))
    start_lightbox_anchor(self, node["uri"])
    HTML5Translator.visit_image(self, node)


def html_depart_image(self: HTML5Translator, node: nodes.Element) -> None:
    HTML5Translator.depart_image(self, node)
    end_lightbox_anchor(self, node)


def setup(app: Sphinx) -> ExtensionMetadata:
    app.require_sphinx("7.0")

    if __PLANTUML_AVAILABLE__:
        # sphinxcontrib.plantuml is available, override require the extension to be setup before we continue
        app.setup_extension("sphinxcontrib.plantuml")
        # Get the translation handler for plantuml and replace it with our wrapper
        app.add_node(sphinxcontrib.plantuml.plantuml, override=True, html=(html_visit_plantuml, None))

    app.add_node(nodes.image, override=True, html=(html_visit_image, html_depart_image))

    app.connect("env-updated", install_static_files)

    return {"version": __version__, "parallel_read_safe": True, "parallel_write_safe": True}
