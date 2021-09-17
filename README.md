# dochub-example

This is a simple static site generator for a collection of jupyter notebooks.
It creates a simple index page with links to all the articles.
It also uses [lunr.js](https://lunrjs.com/)/[lunr.py](https://lunr.readthedocs.io/en/latest/index.html) to perform client-side full-text searching.

## Getting Started

The notebooks are stored with [`git-lfs`](https://git-lfs.github.com/) to avoid versioning them. 
You'll need to have it installed before cloning this repo.
```
conda install git-lfs
```
Next, clone this repo and add/edit notebooks in the `docs/` directory.
You can use `jupytext` paired notebooks to create and version myst markdown representations of the notebooks.
The search index actually uses the contents of the myst files (the builder will generate this on the fly if they don't already exist).

When you are ready to build the site, install the dependencies and run the `build.py` script in the root of the this repo.
```
conda env create -f environment.yml # Only needs to be run once.
conda activate dochub-example
python build.py
```

Finally, you can serve the `build/` directory with your favorite http server.
For example, with python:
```
python -m http -d build/ 1234
# Open http://localhost:1234 in a browser
```
Alternatively, you can upload the zipped build directory to a docat instance.
```
docker run --rm -d  -p 8000:80 randombenj/docat
(cd build && zip -r ../site.zip .)
curl -X POST -F "file=@site.zip" http://localhost:8000/api/dochub-example/1.0.0
# Open http://localhost:8000/#/dochub-example/1.0.0 in a browser
```


## TODO

- [ ] Extract `title`, `summary`, and `tags` from notebook metadata.
- [ ] Add top bar to nbconvert template.
- [ ] Polish everything.
