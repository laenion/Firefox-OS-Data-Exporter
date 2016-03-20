# Firefox OS Data Exporter

This website was developed as part of the article [Exporting the Firefox OS Offline Calendar] (http://digitalimagecorp.de/flatpress/?x=entry:entry151212-222444), but the HTML file can also be used as a general tool for exporting IndexedDB databases. In contrast to Mozilla's [Storage Inspector](https://developer.mozilla.org/en-US/docs/Tools/Storage_Inspector) this script will dump the databases in text format so that it can be copy / pasted and further processed in other programs if needed.

## Motivation

Firefox stores the contents of a IndexedDB database into a SQLite database, but unfortunately only *serialized* data representations. As a result you cannot just view this database with SQLite itself, but you will need Firefox to deserialize those strings again to make any sense of it - which is exactly what this page does.

## What does that have to do with Firefox OS?

Firefox OS and it's applications store a lot of their user data as IndexedDB databases, but do not provide any application or API to access it (e.g. the Offline Calendar data). The only option to backup or export that data is to actually work with the database files themselves.

See http://digitalimagecorp.de/software/firefox-os-data-exporter/ffosexporter.html for a live version of the website and http://digitalimagecorp.de/flatpress/index.php/category/firefox-os/ for instructions how to get the data.
