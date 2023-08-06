import pykka
import logging

from mopidy import core

logger = logging.getLogger(__name__)

class DefaultPlaylistFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(DefaultPlaylistFrontend, self).__init__()
        self.core = core
        self.config = config['defaultplaylist']
        self.defaultplaylist_name = self.config['defaultplaylist_name']
        self.autoplay = self.config['autoplay']
        self.shuffle = self.config['shuffle']

    # Your frontend implementation
    def on_start(self):
        logger.debug("on_start")
        playlists = self.core.playlists.as_list().get()
        playlist_dictionary = {ref.name : ref.uri for ref in playlists}
        logger.debug("Playlist-Mapping: {}".format(playlist_dictionary))
        uri = playlist_dictionary.get(self.defaultplaylist_name, None)
        if uri:
            self.core.tracklist.clear()
            tracks = self.core.playlists.get_items(uri).get()
            logger.info(tracks)
            track_uris = [track.uri for track in tracks]
            logger.info("Tracks: {0}".format(track_uris))
            self.core.tracklist.add(uris=track_uris)
            self.core.tracklist.set_random(self.shuffle)
            if self.autoplay:
                logger.info("Loaded Playlist {}, autoplay on --> start playing tracklist, shuffle-mode {}".format(self.defaultplaylist_name, self.shuffle))
                self.core.playback.play()
            else:
                logger.info("Loaded Playlist {}, shuffle-mode {}".format(self.defaultplaylist_name, self.shuffle))
        else:
            logger.warning("No playlist with name {} found!".format(self.defaultplaylist))

    def playlist_changed(self, playlist):
        logger.info("playlist_changed: {}".format(playlist))
        
    def tracklist_changed(self):
        logger.info("tracklist_changed")