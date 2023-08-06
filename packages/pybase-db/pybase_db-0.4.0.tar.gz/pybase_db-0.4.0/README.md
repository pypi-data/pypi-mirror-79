# PyBase - DB Manager
[![Downloads](https://pepy.tech/badge/pybase-db)](https://pepy.tech/project/pybase-db)
![Version](https://img.shields.io/pypi/v/pybase-db?color=green&label=version)
![Issues](https://img.shields.io/github/issues/NTBBloodbath/PyBase)
![Forks](https://img.shields.io/github/forks/NTBBloodbath/PyBase)
![License](https://img.shields.io/github/license/NTBBloodbath/PyBase)

![PyBase Logo](./res/pybase-logo.png)

PyBase is a DataBase Manager for JSON, YAML, Bytes and SQLite.

It's focused on the ease and effectiveness for the administration of databases.

> **PyBase is actually on Beta phase, may contain bugs.**

------

## Why PyBase?
If you want to store static data (JSON, YAML) or store a database in SQLite,
the best thing would be to use an administrator that simplifies your tasks and
helps you with a good organization and efficiently.

PyBase does exactly that, allows you to create such databases with
just one method, and simplifies the task of manipulating their data!

------

## Contribuitors
- [Danny2105](https://github.com/Danny2105)

------

# Quick start
## Installation
PyBase requires Python 3.x and can be installed through `pip` with the following command.
```sh
pip install pybase_db
```

## Usage example
This is a brief example of the methods that PyBase currently has.
```py
# Lets import PyBase Class from PyBase Package
from pybase import PyBase

# Lets define our database name and format (with default db_path).
# db_type isn't case sensitive. You can use JSON and json and it'll be valid.
db = PyBase("example", "JSON")  #=> ./example.json

# Lets define and add some content to our database.
pybase_info = {"pybase": "awesomeness", "version": "0.3.0"}

# Lets insert the defined dict inside our database.
db.insert(pybase_info)  #=> {'pybase': 'awesomeness', 'version': '0.3.0'}
print(db.get())

# Lets delete an object inside our database cuz it's useless.
db.delete('pybase')  #=> {'version': '0.3.0'}
print(db.get())

# Lets fetch an object inside our database and display its type.
# It's useful to debug and manipulate the data dynamically.
print(db.fetch('version'))

#Gets the corresponding value according to the specified key
print(db.get("version")) #=> '0.3.0'
```

> **To see SQLite3 usage example, click [here](./examples/pysql_usage.py)**

## Documentation
You can see the PyBase documentation through the `help()` function of the REPL
and through the [official documentation site](https://ntbbloodbath.github.io/PyBase).

------

## License
**PyBase is distributed under MIT License.**

## Contributing
You can see how to contribute [here](./CONTRIBUTING.md)

## Code of Conduct
You can see the code of conduct [here](./CODE_OF_CONDUCT.md)
