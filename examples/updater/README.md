## Updater Example

In this updater example, we use the `example_updater_config.json`:

```
{
    "definitions": {
        "type": "CsvDefinitionsProvider",
        "filename": "test/example_definitions.csv"
    }
}
```
which defines the set of definitions we are using. The definitions map the filename and their dimensions, dimension_groups, and measures to our desired definitions.

### Running
Run with

```
cd examples/updater/

python ../../run_updater.py --config example_config.json --infile example.view.lkml --outfile example_outfile.view.lkml
```

The input `example.view.lkml` is a simple LookML view file:

```
view: dim_geography {
 sql_table_name: `BQDW.DimGeography` ;;

  dimension: city_code {
    type: string
    description: "this
    is
    an
    exsiting
    multiline
    description"
    sql: ${TABLE}.CityCode ;;
  }

  measure: count {
    type: count
    drill_fields: [detail*]
  }
}
```

The definitions provide the correct definitions:

```
file,type,name,definition
example.lkml,dimension,city_code,"This
is
the
correct
description"
example.lkml,measure,count,this is the count description
```

What is produced is a new file `example_outfile.view.lkml` with the correct definitions:

```
view: dim_geography {
 sql_table_name: `BQDW.DimGeography` ;;

  dimension: city_code {
    type: string
    description: "This
is
the
correct
description"	# programmatically added by LookML modifier
    sql: ${TABLE}.CityCode ;;
  }

  measure: count {
    description: "this is the count description"	# programmatically added by LookML modifier
    type: count
    drill_fields: [detail*]
  }
}
```
