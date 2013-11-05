from flask import Flask
app = Flask(__name__)

import penult.artist
import penult.album
import penult.song
import penult.auth
import penult.user
import penult.playlist
