

# Grapher Example

The grapher tools parses a set of LookML files, typically a whole repo, and produces a digram of the relationships (the graph) among models, explores, and views.

## Input Repo
The example `myrepo` contains a set of trivial files to illustrate the tool's functionality. It contains 2 models (`model1` and `model2`), three views (`view1`, `view2`, and `view3`) as well one additional orphaned view (`orphan`), not referenced by any explores.

## Config File
The `example_grapher_config.json` is simple:

```
{
    "parser": "lookml-parser",

    "infile_globs": [
        "myrepo/*.*.lkml"
    ],

    "tmp_file": "parsed_lookml.json",

    "output": "graph.png"
}
```
specifiying the parser binary (`lookml-parser`), the files to process (`myrepo/*.*.lkml`), the temporary file that the LookML files are parsed to (`parsed_lookml.json`), and the output filename (`graph.png`).

## Running
To run, 

```
cd examples/grapher/

python ../../run_grapher.py --config example_grapher_config.json
```

You should see something like:

```
python ../../run_grapher.py --config example_grapher_config.json
2019-05-05 20:28:47,360 INFO lookml_grapher.py process_file: Processing myrepo/orphan.view.lkml
2019-05-05 20:28:47,361 INFO lookml.py parse_repo: running lookml-parser --input='myrepo/orphan.view.lkml' --whitespace=2 > parsed_lookml.json
2019-05-05 20:28:47,763 INFO lookml_grapher.py process_file: Processing myrepo/view1.view.lkml
2019-05-05 20:28:47,763 INFO lookml.py parse_repo: running lookml-parser --input='myrepo/view1.view.lkml' --whitespace=2 > parsed_lookml.json
2019-05-05 20:28:47,963 INFO lookml_grapher.py process_file: Processing myrepo/model1.model.lkml
2019-05-05 20:28:47,963 INFO lookml.py parse_repo: running lookml-parser --input='myrepo/model1.model.lkml' --whitespace=2 > parsed_lookml.json
2019-05-05 20:28:48,156 INFO lookml_grapher.py process_file: Processing myrepo/view2.view.lkml
2019-05-05 20:28:48,157 INFO lookml.py parse_repo: running lookml-parser --input='myrepo/view2.view.lkml' --whitespace=2 > parsed_lookml.json
2019-05-05 20:28:48,349 INFO lookml_grapher.py process_file: Processing myrepo/model2.model.lkml
2019-05-05 20:28:48,350 INFO lookml.py parse_repo: running lookml-parser --input='myrepo/model2.model.lkml' --whitespace=2 > parsed_lookml.json
2019-05-05 20:28:48,544 INFO lookml_grapher.py process_file: Processing myrepo/view3.view.lkml
2019-05-05 20:28:48,545 INFO lookml.py parse_repo: running lookml-parser --input='myrepo/view3.view.lkml' --whitespace=2 > parsed_lookml.json
2019-05-05 20:28:49,324 INFO lookml_grapher.py plot_graph: Graph written to graph.png
```

The resulting `graph.png` shows the relationships among the models (blue), explores (green), and views (purple). It also shows that there is a single, orphaned view, shown in orange.

![](graph.png)
