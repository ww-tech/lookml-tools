connection: "datawarehouse"
    
include: "*.view.lkml"

explore: explore1 {
    from: view1
    join: view2 {
        from: view2
    }
}