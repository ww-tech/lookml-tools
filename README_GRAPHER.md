# LookML Grapher

As part of this tool suite, we include a LookML grapher--a tool that shows a "network diagram" of the `model - explore - view` relationships. The code will also identify any `orphans` i.e. views not referenced by any models or explores.

For instance, in this output diagram

![](img/graph.png)

where the nodes are colored as follows:

- *models*: blue
- *explores*: green
- *views*: purple
- *orphans*: orange,

we can see that the `membership_facts` model has 5 explores. The first explore (`engagement`) references 4 views: `fact_engagement`, `dim_product`, `dim_date`, and `dim_member`. We can also see that there is one orphaned view (called `orphan` in this fake example).

## Installation
```

## Running the tool
Simply run:

```
	python run_grapher.py --config config/grapher/config_grapher.json
```

where the config file has the following fields:

```
{
    "infile_globs": [
        "../somerepo/*.lkml"
    ],

    "output": "graph.png",

    "options": {
        "node_size": 500,
        "label_font_size": 18,
        "text_angle": 30,
        "image_width": 24,
        "image_height" : 16
    }
}
```

## Limitations
While this tool might create a network diagram for any valid `lkml` input repo, it is not guaranteed to be understandable or useful. YMMV. As the network gets large, overplotting of nodes can occur and makes them unreadable. Or, if your LookML is a mess and bunch of views and no models there won;t be any structure to see. 

You may be able to fix some of these visualiztion issues by narrowing the file globs or you many need to modify the font size or image size (currently hard coded in `lkmltools.grapher.lookml_grapher` class and not exposed in the config file. We could make this more configurable if useful.) 
