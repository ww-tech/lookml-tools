# Developer Notes

## Linter
There are currently three types of rules:

 - **Field-level rules**: these are rules that apply to an individual `dimension`, `dimension_group`, or `measure`. An example is the `DescriptionRule` that specifies that these field should contain a description.
 - **File-level rules**: these are rules that apply to the file as a whole, such as there should only be one view per file (`OneViewPerFileRule`) or that files should specify a data source with `sql_table_name` or `derived_table` (`DataSourceRule`).
 - **Other rules**: the third category are other rules. The only, current example is the `NoOrphansRule` that says that each view should be referenced by at least one explore. While it sounds like a file-level rule, the code can only assess whether the rule is passed once it has parsed *all* of the files, and not from a single file. Thus, it has to be handled differently than the file-level rules.

### Rule Interface
The rule interface for field-level and file-level rules is simple. They must implement the single method:
 
 ```
     def run(self, json_data):
        '''
        run the rule

        Returns:
            whether rule was relevant: true/false
            whether it passed: (True) or failed (False) the rule
        '''
 ```
 which is in `lkmltools.rules.rule` file. 
 
 Rules must always return two Boolean flags:
 
 - **Relevant**: was the rule relevant for this fragment. So, if a rule that only applies to `measures` is fed JSON from a `dimension_group`, it should return `False`.
 - **Passed**: did the rule pass. If it was not relevant, it should return `None`. 
 
For file-level rules, the `json_data` is the parsed JSON of the whole file and for field-level rules, it is the JSON for an individual `dimension`, `dimension_group`, or `measure`.
 
For instance, for the `DrillDownRule`, which only applies to measures, the implementation is:

```
     def run(self, json_data):
     
        if json_data['_type'] != 'measure':
            return False, None

        if not 'drill_fields' in json_data or json_data['drill_fields'] == []:
            return True, False
        return True, True
```
which should be relatively easy to understand. 

You should examine the parsed JSON of some LookML files to see the structure. For instance,  dimension's JSON for a dimension `city_code` is relatively intuitive:

```
{
      "type": "string",
      "description": "this is a description",
      "sql": "${TABLE}.CityCode ",
      "_dimension": "city_code",
      "_type": "dimension",
      "_n": 0,
      "_view": "dim_geography"
}
```

As well as implementing the rule, it will also needs to be added to added to the `lkmltools.linter.rule_factory`.
