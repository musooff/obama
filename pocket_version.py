#!/usr/bin/python

from os import environ, path


from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

MODELDIR = "../test"
DATADIR = "en-us-orig"

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(DATADIR, 'en-us'))
config.set_string('-lm', path.join(MODELDIR, 'syllables.lm.bin'))
config.set_string('-dict', path.join(MODELDIR, 'new_dict.dict'))
decoder = Decoder(config)

print decoder.lookup_word("something")

