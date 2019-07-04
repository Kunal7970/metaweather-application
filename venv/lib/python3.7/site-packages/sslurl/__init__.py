# -*- coding: utf-8 -*-

"""
################################################################################
#                                                                              #
# sslurl                                                                       #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is a URL HTTP to HTTPS redirection website.                     #
#                                                                              #
# copyright (C) 2018 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################

usage:
    program [options]

options:
    -h, --help  display help message
    --version   display version and exit
"""

import docopt
import logging
import sys

from flask import (
  Flask,
  make_response,
  redirect,
  render_template,
  request
)
import technicolor

name        = "sslurl"
__version__ = "2018-08-15T1701Z"

log = logging.getLogger(name)
log.addHandler(technicolor.ColorisingStreamHandler())
log.setLevel(logging.DEBUG)

log.info(name + " " + __version__)

app = Flask(__name__)

def WSGI(argv = []):
    global options
    options = docopt.docopt(__doc__, argv = argv)
    return app

def main():
    global options
    options = docopt.docopt(__doc__)
    app.run(
        host     = "0.0.0.0",
        port     = 80,
        debug    = False,
        threaded = True
    )
    sys.exit()

@app.route("/robots.txt", methods = ["GET"])
def robots():
    try:
      response = make_response("User-agent: *\nDisallow: /")
      response.headers["Content-type"] = "text/plain"
      return response
    except:
      pass

@app.route("/")
@app.route("/<path>")
def redirect_URL(path = None):
    URL = request.url
    if URL.startswith("http://"):
        URL = URL.replace("http://", "https://")
    log.info("redirect from {request_URL} to {URL}".format(
        request_URL = request.url,
        URL         = URL
    ))
    return redirect(URL)

if __name__ == "__main__":
  main()
