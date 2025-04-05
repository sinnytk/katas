from flatten_dict import flatten


def test_flattens_dict():
    # single level nesting
    assert flatten({"name": "tarun"}) == {"name": "tarun"}
    assert flatten(dict()) == {}
    # lists
    assert flatten({"list_items": [1, 2, 3]}) == {
        "list_items_0": 1,
        "list_items_1": 2,
        "list_items_2": 3,
    }
    # lists with dicts
    assert flatten(
        {
            "places_visited": [
                {"city": "karachi", "country": "pakistan"},
                {"city": "islamabad", "country": "pakistan"},
                {"city": "milan", "country": "italy"},
                {"city": "amsterdam", "country": "netherlands"},
            ]
        }
    ) == {
        "places_visited_0.city": "karachi",
        "places_visited_0.country": "pakistan",
        "places_visited_1.city": "islamabad",
        "places_visited_1.country": "pakistan",
        "places_visited_2.city": "milan",
        "places_visited_2.country": "italy",
        "places_visited_3.city": "amsterdam",
        "places_visited_3.country": "netherlands",
    }
    # dict
    assert flatten({"details": {"firstname": "tarun", "lastname": "kumar"}}) == {
        "details.firstname": "tarun",
        "details.lastname": "kumar",
    }
    assert flatten(
        {
            "details": {
                "name": {"firstname": "tarun", "lastname": "kumar"},
                "address": {"city": "amsterdam", "country": "netherlands"},
                "countries_visited": ["pakistan", "india", "qatar", "uae"],
            }
        }
    ) == {
        "details.name.firstname": "tarun",
        "details.name.lastname": "kumar",
        "details.address.city": "amsterdam",
        "details.address.country": "netherlands",
        "details.countries_visited_0": "pakistan",
        "details.countries_visited_1": "india",
        "details.countries_visited_2": "qatar",
        "details.countries_visited_3": "uae",
    }
