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