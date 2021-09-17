import glob
import os
from lunr import lunr
# from frontmatter import Frontmatter
import frontmatter
import json
import nbformat
from nbconvert import HTMLExporter
import jupytext


html_exporter = HTMLExporter()
# html_exporter.template_name = 'classic'

files = glob.glob('docs/*.ipynb')

article_db = []

index_items = ''

for f in files:
    # print(article)
    pathname, extension = os.path.splitext(f)
    basename = pathname.split('/')[-1]
    fileid = basename + ".html"
    with open(pathname+'.ipynb', 'r') as nb:
        notebook = nbformat.read(nb, as_version=4)
        (body, resources) = html_exporter.from_notebook_node(notebook)
        with open(f'build/{fileid}', 'w') as out:
            out.write(body)
        try:
            article = frontmatter.load(pathname + '.md')
        except:
            print(f"Warning: {pathname}.md doesn't exist!\nConverting {pathname}.ipynb to myst markdown.")
            article = frontmatter.loads(jupytext.writes(notebook, fmt='myst'))

    article_db.append({"id": fileid, "title": basename, "tag": "", "summary": article.content, "content": article.content})
    index_items += f'  <li><a href="{fileid}">{basename}</a></li>\n'

summary_db = [dict(filter(lambda entry: entry[0] != "content", x.items())) for x in article_db]


# json.dump(article_db, 'documents.json')
json.dump(summary_db, open('build/lunr-summary.json', 'w'))


idx = lunr(ref='id', fields=('title', 'content'), documents = article_db)

json.dump(idx.serialize(), open('build/lunr-index.json', 'w'))


index_html = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Index</title>

<script src="https://unpkg.com/lunr/lunr.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
* {box-sizing: border-box;}

body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
}

.topnav {
  overflow: hidden;
  background-color: #e9e9e9;
}

.topnav a {
  float: left;
  display: block;
  color: black;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 17px;
}

.topnav a:hover {
  background-color: #ddd;
  color: black;
}

.topnav a.active {
  background-color: #2196F3;
  color: white;
}

.topnav .search-container {
  float: right;
}

.topnav input[type=text] {
  padding: 6px;
  margin-top: 8px;
  font-size: 17px;
  border: none;
}

.topnav .search-container button {
  float: right;
  padding: 6px 10px;
  margin-top: 8px;
  margin-right: 16px;
  background: #ddd;
  font-size: 17px;
  border: none;
  cursor: pointer;
}

.topnav .search-container button:hover {
  background: #ccc;
}

@media screen and (max-width: 600px) {
  .topnav .search-container {
    float: none;
  }
  .topnav a, .topnav input[type=text], .topnav .search-container button {
    float: none;
    display: block;
    text-align: left;
    width: 100%;
    margin: 0;
    padding: 14px;
  }
  .topnav input[type=text] {
    border: 1px solid #ccc;  
  }
}
</style>
</head>

<body>

  <div class="topnav">
    <a class="active" href="index.html">Home</a>
    <div class="search-container">
      <form action="search.html">
        <input type="text" placeholder="Search.." name="q">
        <button type="submit"><i class="fa fa-search"></i></button>
      </form>
    </div>
  </div>

<h1>Articles</h1>

<ul>
MY_DOCS
</ul>

</body>
</html>
"""

index_items += f'  <li><a href="search.html">Search</a></li>'


with open('build/index.html', 'w') as f:
    f.write(index_html.replace('MY_DOCS', index_items))