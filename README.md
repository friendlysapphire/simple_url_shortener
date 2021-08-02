# Simple URL Shortener

Simple URL Shortener is an extremely basic URL shortening service written in Python using [Bottle](https://bottlepy.org),
the [bottle-sqlite plugin](https://pypi.org/project/bottle-sqlite/), and [Hashids](https://hashids.org/python/).

## Routes

It supports the following routes:

    * / and /new/
        Loads the page to create a new short URL.

    * /stats/
        Shows information about existing short URLs, including the option to delete.
        Also shows the live host and port information.

    * /<short url>
        Redirects to the full URL associated with the supplied short URL.

    * /delete/
        Used internally to support deletion from the stats/ route.

## Configuration

The code is all contained within url_shortener.py and various configuration options can be set in the beginning of the file.

## General Notes

The code was developed and tested using Python 3.8.5, 3.9.4, and 3.9.6. As of this writing it hasn't been tested with other versions, although I suspect Python 3.6+ should work.

This project was a learning exercise and isn't meant to be production-ready code.

## License

Code and documentation are available according to the MIT License.
