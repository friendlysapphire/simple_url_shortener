#!/usr/bin/env python3

import os
from pathlib import Path
import sqlite3
from bottle import route, install, template, redirect, run, request
from bottle_sqlite import SQLitePlugin
from hashids import Hashids
import re

# CONFIG Section

# database config
DATABASE_FOLDER = Path("database")
DATABASE_FILE = Path("url_db.sqlite")
DATABASE_FULL_PATH = DATABASE_FOLDER / DATABASE_FILE

# our url shortener webserver config
HOST = "localhost"
HOST_PROTOCOL_STR = "http://"
HOST_PORT = 8080
HOST_BASE_URL = HOST_PROTOCOL_STR + HOST + ":" + str(HOST_PORT) + "/"

# hashids config
MIN_SHORT_URL_LENGTH = 4
SALT = "84NAIFHAcy8uj7XhH8qSyU"

# other config

# if the user doesn't supply a protocol when submitting an URL to shorten, apply this default
DEFAULT_PROTOCOL_FOR_LONG_URL = "http://"

# **kwargs we'll pass to bottle.run() when starting the server.
# set RUN_MODE_ARGS to one of these 4.
FULL_DEBUG_MODE_ARGS = {"debug": True, "reloader": True}
FULL_PRODUCTION_MODE_ARGS = {"debug": False, "reloader": False}
RELOAD_NO_DEBUG_ARGS = {"reloader": True, "debug": False}
DEBUG_NO_RELOAD_ARGS = {"debug": True, "reloader": False}

RUN_MODE_ARGS = FULL_DEBUG_MODE_ARGS

# db schema
SCHEMA = """DROP TABLE IF EXISTS urls;

CREATE TABLE urls (

id INTEGER PRIMARY KEY,
long_url TEXT NOT NULL,
uses INTEGER NOT NULL DEFAULT 0,
created_at TEXT DEFAULT CURRENT_TIMESTAMP

);"""

# END Config

# Used to find the :// in strings.
PROTOCOL_MATCH_REGEX = re.compile(".+?(://)", re.IGNORECASE)

def create_db():
    """
    Creates DATABSAE_FILE in DATABASE_FOLDER and sets up schema.

    Note: Expects DATABASE_FOLDER already to exist (see bootstrap())
    """

    db_conn = sqlite3.connect(DATABASE_FULL_PATH)
    db_conn.executescript(SCHEMA)
    db_conn.commit()
    db_conn.close()


def bootstrap():
    """
    Check if the database path and database exists. If not, create.
    """

    if not os.path.exists(DATABASE_FOLDER):
        os.makedirs(DATABASE_FOLDER)
        create_db()

    elif not os.path.exists(DATABASE_FULL_PATH):
        create_db()

@route('/', method='GET')
@route('/new', method='GET')
@route('/new/', method='GET')
def new_short_url_form_display():
    """
    http://HOST/new/ is the route for creating a new short url. GET method shows user the form.
    """
    return template("create_new_short_url")

@route('/new', method='POST')
def create_new_short_url(db):
    """
    http://HOST/new/ is the route for creating a new short url. POST method processes returned form.
    """

    in_long_url = request.forms.get('long_url').strip()

    # Add any initial validation here. Right now it's just looking for null.
    if not in_long_url:
        try_again_url = HOST_BASE_URL + "new/"
        return template("invalid_url_to_shorten", in_long_url=in_long_url, try_again_url=try_again_url)

    # figure out if user supplied the protocol. If not, apply our default. If so, preserve their chosen protocol.
    protocol = PROTOCOL_MATCH_REGEX.match(in_long_url)

    if not (protocol):
        in_long_url = DEFAULT_PROTOCOL_FOR_LONG_URL + in_long_url

    cur = db.cursor()
    id_to_encode = None

    # see if we already have this URL in the db
    cur.execute("SELECT id FROM urls where long_url = ?", (in_long_url,))
    row = cur.fetchone()

    if row and row['id']:
        # we found the url so pull the ID and return it encoded as the short url
        id_to_encode = row['id']

    # we didn't find the given URL in the DB, so add it and pull that new row's id
    # to encode and return to the user
    else:
        # create a new entry in the db with this long url
        cur.execute("INSERT INTO urls (long_url) VALUES (?)", (in_long_url,))
        id_to_encode = cur.lastrowid

    db.commit()
    cur.close()
    hashids = Hashids(salt=SALT, min_length=MIN_SHORT_URL_LENGTH)
    short_url_hash = hashids.encode(id_to_encode)

    # Generate the full short link for display to the user
    full_short_url = HOST_BASE_URL + str(short_url_hash)

    return template("returned_shortened_url",
                    in_long_url=in_long_url,
                    full_short_url=full_short_url
                    )

@route('/delete', method='POST')
def delete_db_row(db):
    """
    http://HOST/delete is the route for deleting an short url via the Delete button on the stats page
    """
    id = request.forms.get('delrow').strip()

    cur = db.cursor()
    cur.execute("DELETE FROM urls WHERE id = ?", (id,))
    db.commit()
    cur.close()

    redirect("/stats")


@route('/stats/')
@route('/stats')
def show_stats(db):
    """
    http://HOST/stats is the route for viewing the database and related information.
    """

    cur = db.cursor()
    cur.execute("SELECT * FROM urls")
    table = cur.fetchall()

    # we don't store short URLs in the db because they're derived from the integer primary key.
    # however for convenience add them into the stats page view.

    # NOTE: The below costs some extra cycles that could be avoided
    #       if performance here ever became a concern.

    # alternative 1: insert the hashids in the template code loop w/o generating this new structure
    # alternative 2: add short urls to the DB

    # generate row structure for template
    # DB is "ID", "Long URL", "Uses", "Created On"
    # the below code inserts short url after long url and
    # the template itself implements the delete column.

    list_of_rows = [[] for _ in range(len(table))]
    hashids = Hashids(salt=SALT, min_length=MIN_SHORT_URL_LENGTH)

    for index in range(len(table)):
        list_of_rows[index] = list(table[index])
        short_url_hash = hashids.encode(list_of_rows[index][0])
        list_of_rows[index].insert(2, short_url_hash)

    cur.close()
    # generate heading structure for template
    headings_list = ["ID", "Long URL", "Short URL Hash", "Uses", "Created On"]
    base_url = HOST_BASE_URL

    return template("stats_page", rows=list_of_rows, headings=headings_list, base_url=base_url)

@route('/<short_url_hash>/')
@route('/<short_url_hash>')
def decode_and_redirect(db, short_url_hash):
    """
    http://HOST/<short_url_hash> is the route for processing <short_url_hash> as a shortened URL
    and issuing a redirect.
    """

    # decode the short URL passed in from the user, turning it back into an id.
    # if hashids can't make sense of the url, report failure to user
    hashids = Hashids(salt=SALT, min_length=MIN_SHORT_URL_LENGTH)
    id = hashids.decode(short_url_hash)
    if not id:
        return template("cant_redirect_no_match", short_url_hash=short_url_hash)
    else:
        # decode returns a tuple  (id,) .. so if id exists (checked above),
        # just extract the actual id
        id = id[0]

    # look up the resulting id in the db, pull out the long_url and the uses fields
    cur = db.cursor()
    cur.execute("SELECT long_url, uses FROM urls where id = ?", (id,))
    row = cur.fetchone()

    if row and row['long_url']:

        # increment the uses field
        new_uses = row['uses'] + 1

        cur.execute("UPDATE urls SET uses = ? where id = ?", (new_uses, id,))
        db.commit()
        cur.close()

        # redirect
        redirect(row['long_url'])

    else:
        # can't find a match, so let the user know.
        return template("cant_redirect_no_match", short_url_hash=short_url_hash)

def main():

    # check for a pre-existing db and if it's not there, create it @ DATABASE_FULL_PATH
    bootstrap()

    # register db w/ sqlite for easy access in callbacks
    install(SQLitePlugin(dbfile=DATABASE_FULL_PATH))

    run(host=HOST, port=HOST_PORT, **RUN_MODE_ARGS)


if __name__ == '__main__':
    main()
