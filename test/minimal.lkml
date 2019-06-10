view: dim_geography {
 sql_table_name: `BQDW.DimGeography` ;;

  dimension: city_code {
    type: string
    sql: ${TABLE}.CityCode ;;
  }

  measure: count {
    type: count
    drill_fields: [detail*]
  }
}