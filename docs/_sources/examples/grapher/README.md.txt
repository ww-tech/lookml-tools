

# Grapher Example

The grapher tools parses a set of LookML files, typically a whole repo, and produces a digram of the relationships (the graph) among models, explores, and views.

## Input Repo
The example `myrepo` contains a set of trivial files to illustrate the tool's functionality. It contains 2 models (`model1` and `model2`), three views (`view1`, `view2`, and `view3`) as well one additional orphaned view (`orphan`), not referenced by any explores.

## Config File
The `example_grapher_config.json` is simple:

```
{
    "infile_globs": [
        "myrepo/*.*.lkml"
    ],

    "output": "graph.png"
}
```
specifiying the files to process (`myrepo/*.*.lkml`) and the output filename (`graph.png`).

## Running
To run, 

```
cd examples/grapher/

python ../../run_grapher.py --config example_grapher_config.json
```

You should see something like:

```
python ../../run_grapher.py --config example_grapher_config.json
2019-07-17 09:15:41,709 INFO lookml_grapher.py extract_graph_info: Processing myrepo/orphan.view.lkml
2019-07-17 09:15:41,710 INFO lookml_grapher.py extract_graph_info: Processing myrepo/view1.view.lkml
2019-07-17 09:15:41,710 INFO lookml_grapher.py extract_graph_info: Processing myrepo/model1.model.lkml
2019-07-17 09:15:41,711 INFO lookml_grapher.py extract_graph_info: Processing myrepo/view2.view.lkml
2019-07-17 09:15:41,712 INFO lookml_grapher.py extract_graph_info: Processing myrepo/model2.model.lkml
2019-07-17 09:15:41,712 INFO lookml_grapher.py extract_graph_info: Processing myrepo/view3.view.lkml
2019-07-17 09:15:41,713 INFO lookml_grapher.py run: Setting the following options: {'g': <networkx.classes.digraph.DiGraph object at 0x108537ac8>, 'filename': 'graph.png', 'title': 'myrepo/*.*.lkml as of 2019-07-17'}
2019-07-17 09:15:42,252 INFO lookml_grapher.py plot_graph: Graph written to graph.png
```

The resulting `graph.png` shows the relationships among the models (blue), explores (green), and views (purple). It also shows that there is a single, orphaned view, shown in orange.

![](graph.png)
