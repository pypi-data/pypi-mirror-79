import os
import warnings

from packaging.version import parse as parse_version
from sphinx.errors import ConfigError

from .version import version as __version__

assert __version__

__copyright__ = "2018-2020 Applied Brain Research"
current_dir = os.path.abspath(os.path.dirname(__file__))


def setup(app):
    app.add_html_theme("nengo_sphinx_theme", os.path.join(current_dir, "theme"))

    # validate config
    def validate_config(_, config):
        theme_config = getattr(config, "html_theme_options", {})

        # check nengo_logo config
        html_logo = getattr(config, "html_logo", "")
        nengo_logo = theme_config.get("nengo_logo", None)

        if html_logo and nengo_logo:
            warnings.warn(
                "'html_logo' and 'nengo_logo' are both set; "
                "'nengo_logo' will take precedence"
            )
        elif html_logo:
            warnings.warn(
                "Logo set using 'html_logo', consider using " "'nengo_logo' instead"
            )

        # check versioning config
        html_context = getattr(config, "html_context", {})
        releases = html_context.get("releases", "").split(",")
        building = html_context.get("building_version", "")

        if "latest" in releases:
            raise ConfigError(
                "nengo_sphinx_theme.ext.versions: 'latest' cannot be a "
                "release name (link to the most up-to-date version of the "
                "docs will be added automatically)"
            )

        if building == "":
            warnings.warn("'building_version' not set, versions will not be rendered")

        # check Google Analytics ID
        analytics_id = theme_config.get("analytics_id", None)
        if analytics_id is not None and not analytics_id.startswith("UA-"):
            warnings.warn(
                "'analytics_id' looks strange. It should look like "
                "'UA-000000-2'; got %r" % (analytics_id,)
            )

        # check Google Tag Manager container ID
        tagmanager_id = theme_config.get("tagmanager_id", None)
        if tagmanager_id is not None and not tagmanager_id.startswith("GTM-"):
            warnings.warn(
                "'tagmanager_id' looks strange. It should look like "
                "'GTM-XXXXXXX'; got %r" % (tagmanager_id,)
            )

    app.connect("config-inited", validate_config)

    def add_jinja_filters(app):
        def sort_versions(releases):
            releases = [r for r in releases.split(",") if r.strip() != ""]
            releases.sort(key=parse_version, reverse=True)
            return releases

        def to_root(pagename):
            return "../" * pagename.count("/")

        if app.builder.format == "html":
            app.builder.templates.environment.filters["sort_versions"] = sort_versions
            app.builder.templates.environment.filters["to_root"] = to_root

    app.connect("builder-inited", add_jinja_filters)
