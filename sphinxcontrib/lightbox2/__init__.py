import dataclasses
import hashlib
import importlib.metadata
import json
import pathlib
import posixpath
import urllib.parse
from typing import Any, Generic, TypeVar

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.environment import BuildEnvironment
from sphinx.util import display, osutil
from sphinx.util.typing import ExtensionMetadata
from sphinx.writers.html5 import HTML5Translator

try:
    import sphinxcontrib.plantuml  # type: ignore

    __PLANTUML_AVAILABLE__ = True

except ImportError:
    __PLANTUML_AVAILABLE__ = False


try:
    import sphinxcontrib.mermaid  # type: ignore

    __MERMAID_AVAILABLE__ = True

except ImportError:
    __MERMAID_AVAILABLE__ = False

try:
    # Poetry requires the version to be defined in pyproject.toml, load the version from the metadata,
    # this is the recommended approach https://github.com/python-poetry/poetry/pull/2366#issuecomment-652418094
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:  # pragma: no cover
    # No metadata is available, this could be because the tool is running from source
    __version__ = "unknown"

T = TypeVar("T")
STATIC_FILES = (
    pathlib.Path("assets/images/close.png"),
    pathlib.Path("assets/images/next.png"),
    pathlib.Path("assets/images/prev.png"),
    pathlib.Path("assets/images/loading.gif"),
    pathlib.Path("assets/js/lightbox-plus-jquery.min.js"),
    pathlib.Path("assets/js/lightbox-plus-jquery.min.map"),
    pathlib.Path("assets/css/lightbox.min.css"),
)


@dataclasses.dataclass
class Lightbox2ConfigOption(Generic[T]):
    name: str
    default: T

    def sphinx_config_name(self) -> str:
        return "lightbox2_" + self.name

    def js_config_name(self) -> str:
        return snake_to_camel(self.name)


CONFIG_OPTIONS: tuple[Lightbox2ConfigOption[Any], ...] = (
    Lightbox2ConfigOption("always_show_nav_on_touch_devices", False),
    Lightbox2ConfigOption("album_label", "Image %1 of %2"),
    Lightbox2ConfigOption("disable_scrolling", False),
    Lightbox2ConfigOption("fade_duration", 600),
    Lightbox2ConfigOption("fit_images_in_viewport", True),
    Lightbox2ConfigOption("image_fade_duration", 600),
    Lightbox2ConfigOption("max_width", None),
    Lightbox2ConfigOption("max_height", None),
    Lightbox2ConfigOption("position_from_top", 50),
    Lightbox2ConfigOption("resize_duration", 700),
    Lightbox2ConfigOption("show_image_number_label", True),
    Lightbox2ConfigOption("wrap_around", True),
)


def snake_to_camel(snake_str: str) -> str:
    """Translate a snake_case string to camelCase"""
    components = snake_str.split("_")
    # Capitalize the first letter of each component except the first one
    return components[0] + "".join(x.title() for x in components[1:])


def render_lightbox2_option_method_call(config: Config) -> str:
    """Render the lightbox.options method call with the configured options to a string"""
    lightbox_options = {}

    for option in CONFIG_OPTIONS:
        val = getattr(config, option.sphinx_config_name(), None)
        if val is None:
            continue
        lightbox_options[option.js_config_name()] = val
    return f"lightbox.option({json.dumps(lightbox_options)})"


def start_lightbox_anchor(self: HTML5Translator, uri: str) -> None:
    """Write the start of a lightbox anchor to the body"""
    self.body.append(f"""<a href="{uri}" data-lightbox="image-set">\n""")


def end_lightbox_anchor(self: HTML5Translator, node: nodes.Element) -> None:
    """Close the lightbox2 anchor element"""
    self.body.append("</a>\n")


def install_static_files(app: Sphinx, env: BuildEnvironment) -> None:
    """Install the static lightbox2 files and configuration options"""
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

        abs_source_file_path = pathlib.Path(__file__).parent / source_file_path
        osutil.copyfile(abs_source_file_path, dest_file_path)

        if dest_file_path.suffix == ".js":
            app.add_js_file(str(dest_file_path.relative_to(static_dir)))
        elif dest_file_path.suffix == ".css":
            app.add_css_file(str(dest_file_path.relative_to(static_dir)))

    lightbox_options_path = dest_path / "js" / "lightbox2-options.js"
    lightbox_options_path.write_text(render_lightbox2_option_method_call(env.config))
    app.add_js_file(str(lightbox_options_path.relative_to(static_dir)))


def html_visit_plantuml(self: HTML5Translator, node: nodes.Element) -> None:
    """Node visitor that wraps the ``html_visit_plantuml`` visitor from the `sphinxcontrib.plantuml` extension."""

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
        # But the anchor element still needs to be closed
        end_lightbox_anchor(self, node)
        raise


def html_visit_image(self: HTML5Translator, node: nodes.Element) -> None:
    """
    Node visitor for image nodes. This adds the lightbox2 anchor element before the image and calls
    ``HTML5Translator.visit_image`` afterwards.
    """
    olduri = node["uri"]
    # Rewrite the URI if the environment knows about it
    if olduri in self.builder.images:
        node["uri"] = posixpath.join(self.builder.imgpath, urllib.parse.quote(self.builder.images[olduri]))
    start_lightbox_anchor(self, node["uri"])
    HTML5Translator.visit_image(self, node)


def html_depart_image(self: HTML5Translator, node: nodes.Element) -> None:
    """Node departer for image nodes. This closes the lightbox2 anchor element after departing the image the image"""
    try:
        HTML5Translator.depart_image(self, node)
    finally:
        end_lightbox_anchor(self, node)


def html_visit_mermaid(self: HTML5Translator, node: nodes.Element) -> None:
    """
    Node visitor that wraps the ``html_visit_mermaid`` visitor from the `sphinxcontrib.mermaid` extension.

    This is only done if the format is configured to be png.
    """
    _fmt = self.builder.config.mermaid_output_format

    if _fmt != "png":
        sphinxcontrib.mermaid.html_visit_mermaid(self, node)
        return

    code = node["code"]
    options = node["options"]
    prefix = "mermaid"

    hashkey = (code + str(options) + str(self.builder.config.mermaid_sequence_config)).encode("utf-8")
    basename = f"{prefix}-{hashlib.sha1(hashkey).hexdigest()}"  # noqa: S324
    fname = f"{basename}.{_fmt}"
    relfn = posixpath.join(self.builder.imgpath, fname)

    self.body.append(f"""<a href="{relfn}" data-lightbox="image-set">\n""")

    try:
        sphinxcontrib.mermaid.html_visit_mermaid(self, node)
    except nodes.SkipNode:
        # Catch the SkipNode exception so that the depart_* function is not entered
        # But the anchor element still needs to be closed
        end_lightbox_anchor(self, node)
        raise


def setup(app: Sphinx) -> ExtensionMetadata:
    app.require_sphinx("7.0")

    for option in CONFIG_OPTIONS:
        app.add_config_value(
            option.sphinx_config_name(), default=option.default, rebuild="env", types=type(option.default)
        )

    if __PLANTUML_AVAILABLE__:
        # sphinxcontrib.plantuml is available, require the extension to be setup before we continue
        app.setup_extension("sphinxcontrib.plantuml")
        # Get the translation handler for plantuml and replace it with our wrapper
        app.add_node(sphinxcontrib.plantuml.plantuml, override=True, html=(html_visit_plantuml, None))

    if __MERMAID_AVAILABLE__:
        app.setup_extension("sphinxcontrib.mermaid")
        app.add_node(sphinxcontrib.mermaid.mermaid, override=True, html=(html_visit_mermaid, None))

    app.add_node(nodes.image, override=True, html=(html_visit_image, html_depart_image))

    app.connect("env-updated", install_static_files)

    return {"version": __version__, "parallel_read_safe": True, "parallel_write_safe": True}
