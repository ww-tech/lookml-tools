connection: "datawarehouse"
    
include: "*.view.lkml"

explore: explore2 {
    from: view3
}