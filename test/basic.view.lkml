view: wins_balance_intl_tiers {
  label: "Wins Balance Tiers (Intl)"
  view_label: "Wins Balance Tiers Intl"
  derived_table: {
    datagroup_trigger: rewards_daily
    sql: #standardsql
        select stuff from table ;;
        }

  dimension: country {
    type: string
    map_layer_name: countries
    sql: ${TABLE}.country ;;
  }

  measure: members       {
    type: sum
    sql: ${TABLE}.members ;;
  }

  dimension: tier {
    type: number
    description: "this 
    is 
    a 
    multiline
    description"
    sql: ${TABLE}.Tier ;;
  }

  dimension: min_wins {
    type: number
    sql: ${TABLE}.min_wins ;;
  }

  dimension: wins_range {
    type: string
    sql: ${TABLE}.wins_range ;;
  }

  measure: count {
    type: count
    drill_fields: []
  }
}
