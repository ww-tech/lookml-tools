
include: "*.view.lkml"
explore: some_explore {
    from: some_view
    join: some_other_view {
        from: some_other_view
    }
}
