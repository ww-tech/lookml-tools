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

  dimension_group: current_week_start {
    type: time
    timeframes: [
      date,
      week,
      month,
    ]
    convert_tz: no
    datatype: date
    sql: ${TABLE}.CurrentWeekStart ;;
  }

  measure: count {
    type: count
    drill_fields: [detail*]
  }
}