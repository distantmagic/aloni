# demo app

This is a demo app that showcases the use of the intention library.

## Usage

To run the demo app, use [Poetry](https://python-poetry.org/). 

First, install the dependencies:

```shell
poetry install
```

Then, enter the project's shell:

```shell
poetry shell
```

Finally, run the demo app with [Granian](https://github.com/emmett-framework/granian) (available from inside the project shell):

```shell
granian --interface rsgi ./app_rsgi.py
```

Alternatively, if you have make installed, you can run the demo app with:

```shell
make start.rsgi
```
