connection: "some_db_connection"

include: "*.view"

explore: some_explore {
  from: some_view  
  join: enrollment_date {
    from: some_other_view
    type: inner
    relationship: many_to_one
    sql_on: ${membership.enrollment_date_id} =${enrollment_date.date_id} ;;
  }
}