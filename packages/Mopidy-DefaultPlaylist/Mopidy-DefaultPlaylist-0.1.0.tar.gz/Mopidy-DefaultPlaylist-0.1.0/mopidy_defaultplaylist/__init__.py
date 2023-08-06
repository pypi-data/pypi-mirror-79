import logging
import pathlib

import pkg_resources

from mopidy import config, ext

__version__ = pkg_resources.get_distribution("Mopidy-DefaultPlaylist").version

# TODO: If you need to log, use loggers named after the current Python module
logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = "Mopidy-DefaultPlaylist"
    ext_name = "defaultplaylist"
    version = __version__

    def get_default_config(self):
        return config.read(pathlib.Path(__file__).parent / "ext.conf")

    def get_config_schema(self):
        schema = super().get_config_schema()
        schema["defaultplaylist_name"] = config.String()
        schema["autoplay"] = config.Boolean()
        schema["shuffle"] = config.Boolean()

        return schema

    def setup(self, registry):
        # You will typically only implement one of the following things
        # in a single extension.

        from .frontend import DefaultPlaylistFrontend

        registry.add("frontend", DefaultPlaylistFrontend)
