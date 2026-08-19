from gear import (
    create_gear_item,
    get_next_gear_id,
    add_gear,
    view_gear,
    view_gear_details,
    select_category,
    select_optional_category,
    select_subcategory,
    select_optional_subcategory,
    select_status,
    select_optional_status,
    get_optional_rating,
    edit_gear,
    delete_gear,
)


def test_create_gear_item():
    gear = create_gear_item(
        item_id=1,
        category="Water",
        subcategory="Filter",
        brand_model="Sawyer Squeeze",
        weight_oz=3.0,
        cost=45.99,
        durability=5,
        ease_of_use=4,
        owned=True,
        quantity_owned=1,
        tested=True,
        status="Active",
    )

    assert gear["id"] == 1
    assert gear["category"] == "Water"
    assert gear["subcategory"] == "Filter"
    assert gear["brand_model"] == "Sawyer Squeeze"
    assert gear["weight_oz"] == 3.0
    assert gear["cost"] == 45.99
    assert gear["owned"] is True
    assert gear["quantity_owned"] == 1
    assert gear["tested"] is True
    assert gear["status"] == "Active"


def test_get_next_gear_id_empty():
    assert get_next_gear_id([]) == 1


def test_get_next_gear_id_existing():
    gear = [
        {"id": 1},
        {"id": 3},
        {"id": 2},
    ]

    assert get_next_gear_id(gear) == 4


def test_add_gear(monkeypatch):
    gear = []

    responses = iter([
        "6",                 # Category -> Water
        "1",                 # Subcategory -> Filter
        "Sawyer Squeeze",    # Brand / Model
        "3.0",               # Weight
        "45.99",             # Cost
        "4",                 # Comfort
        "5",                 # Durability
        "4",                 # Ease of Use
        "3",                 # Protection / Warmth
        "y",                 # Owned
        "1",                 # Quantity owned
        "y",                 # Tested
        "3",                 # Status -> Active
        "",                  # Source URL
        "Primary filter",    # Notes
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(responses),
    )

    save_called = {"value": False}

    def fake_save_gear(items):
        save_called["value"] = True

    monkeypatch.setattr(
        "gear.save_gear",
        fake_save_gear,
    )

    add_gear(gear)

    assert len(gear) == 1

    item = gear[0]

    assert item["id"] == 1
    assert item["category"] == "Water"
    assert item["subcategory"] == "Filter"
    assert item["brand_model"] == "Sawyer Squeeze"
    assert item["weight_oz"] == 3.0
    assert item["cost"] == 45.99
    assert item["owned"] is True
    assert item["quantity_owned"] == 1
    assert item["tested"] is True
    assert item["status"] == "Active"

    assert save_called["value"] is True


def test_add_gear_unowned_sets_quantity_zero(monkeypatch):
    gear = []

    responses = iter([
        "2",                    # Category -> Shelter
        "1",                    # Subcategory -> Tent
        "Durston X-Mid 1",      # Brand / Model
        "28.0",                 # Weight
        "240.00",               # Cost
        "4",                    # Comfort
        "4",                    # Durability
        "4",                    # Ease of Use
        "4",                    # Protection / Warmth
        "n",                    # Owned
        "n",                    # Tested
        "2",                    # Status -> Considering
        "",                     # Source URL
        "Potential PCT tent",   # Notes
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(responses),
    )

    monkeypatch.setattr(
        "gear.save_gear",
        lambda items: None,
    )

    add_gear(gear)

    item = gear[0]

    assert item["owned"] is False
    assert item["quantity_owned"] == 0
    assert item["tested"] is False
    assert item["status"] == "Considering"


def test_view_gear(capsys):
    gear = [
        {
            "id": 1,
            "category": "Water",
            "subcategory": "Filter",
            "brand_model": "Sawyer Squeeze",
            "weight_oz": 3.0,
            "cost": 45.99,
            "comfort": None,
            "durability": 5,
            "ease_of_use": 4,
            "protection_warmth": None,
            "owned": True,
            "quantity_owned": 1,
            "tested": True,
            "status": "Active",
            "source_url": "",
            "notes": "",
        }
    ]

    view_gear(gear)

    output = capsys.readouterr().out

    assert "GEAR INVENTORY" in output
    assert "Water" in output
    assert "Sawyer Squeeze" in output
    assert "3.0 oz" in output
    assert "Owned" in output
    assert "Active" in output


def test_view_gear_empty(capsys):
    view_gear([])

    output = capsys.readouterr().out

    assert "No gear added yet." in output


def test_view_gear_details(monkeypatch, capsys):
    gear = [
        {
            "id": 1,
            "category": "Water",
            "subcategory": "Filter",
            "brand_model": "Sawyer Squeeze",
            "weight_oz": 3.0,
            "cost": 45.99,
            "comfort": None,
            "durability": 5,
            "ease_of_use": 4,
            "protection_warmth": None,
            "owned": True,
            "quantity_owned": 1,
            "tested": True,
            "status": "Active",
            "source_url": "https://example.com",
            "notes": "Primary water filter",
        }
    ]

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "1",
    )

    view_gear_details(gear)

    output = capsys.readouterr().out

    assert "GEAR DETAILS" in output
    assert "Category: Water" in output
    assert "Subcategory: Filter" in output
    assert "Brand / Model: Sawyer Squeeze" in output
    assert "Weight: 3.0 oz" in output
    assert "Cost: $45.99" in output
    assert "Durability: 5" in output
    assert "Ease of Use: 4" in output
    assert "Owned: Yes" in output
    assert "Quantity Owned: 1" in output
    assert "Tested: Yes" in output
    assert "Status: Active" in output
    assert "Primary water filter" in output


def test_view_gear_details_empty(capsys):
    view_gear_details([])

    output = capsys.readouterr().out

    assert "No gear added yet." in output


def test_view_gear_details_invalid_number(monkeypatch, capsys):
    gear = [
        {
            "id": 1,
            "category": "Water",
            "subcategory": "Filter",
            "brand_model": "Sawyer Squeeze",
            "weight_oz": 3.0,
            "cost": 45.99,
            "comfort": None,
            "durability": 5,
            "ease_of_use": 4,
            "protection_warmth": None,
            "owned": True,
            "quantity_owned": 1,
            "tested": True,
            "status": "Active",
            "source_url": "",
            "notes": "",
        }
    ]

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "2",
    )

    view_gear_details(gear)

    output = capsys.readouterr().out

    assert "Invalid gear item number." in output


def test_select_category(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "6",
    )

    category = select_category()

    assert category == "Water"


def test_select_subcategory(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "1",
    )

    subcategory = select_subcategory("Water")

    assert subcategory == "Filter"


def test_select_status(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "3",
    )

    status = select_status()

    assert status == "Active"


def test_select_optional_category_keeps_current(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "",
    )

    result = select_optional_category("Water")

    assert result == "Water"


def test_select_optional_category_changes_value(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "2",
    )

    result = select_optional_category("Water")



def test_select_optional_category_retries_invalid(monkeypatch):
    responses = iter([
        "99",
        "bad",
        "6",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(responses),
    )

    result = select_optional_category("Pack")

    assert result == "Water"


def test_select_optional_subcategory_keeps_current(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "",
    )

    result = select_optional_subcategory(
        "Water",
        "Filter",
    )

    assert result == "Filter"


def test_select_optional_subcategory_changes_value(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "2",
    )

    result = select_optional_subcategory(
        "Water",
        "Filter",
    )

    assert result == "Bottle"


def test_select_optional_subcategory_requires_new_value(
    monkeypatch,
):
    responses = iter([
        "",
        "1",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(responses),
    )

    result = select_optional_subcategory(
        "Shelter",
        "Filter",
    )

    assert result == "Tent"


def test_select_optional_status_keeps_current(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "",
    )

    result = select_optional_status("Active")

    assert result == "Active"


def test_select_optional_status_changes_value(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "4",
    )

    result = select_optional_status("Active")

    assert result == "Retired"


def test_select_optional_status_retries_invalid(monkeypatch):
    responses = iter([
        "99",
        "bad",
        "2",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(responses),
    )

    result = select_optional_status("Researching")

    assert result == "Considering"


def test_edit_gear_changes_brand_model(monkeypatch):
    gear = [
        {
            "id": 1,
            "category": "Water",
            "subcategory": "Filter",
            "brand_model": "Sawyer Squeeze",
            "weight_oz": 3.0,
            "cost": 45.99,
            "comfort": None,
            "durability": 5,
            "ease_of_use": 4,
            "protection_warmth": None,
            "owned": True,
            "quantity_owned": 1,
            "tested": True,
            "status": "Active",
            "source_url": "",
            "notes": "",
        }
    ]

    responses = iter([
        "1",                 # choose item
        "",                  # keep category
        "",                  # keep subcategory
        "Sawyer Squeeze 2",  # change brand/model
        "",                  # keep weight
        "",                  # keep cost
        "",                  # keep comfort
        "",                  # keep durability
        "",                  # keep ease
        "",                  # keep protection
        "",                  # keep owned
        "",                  # keep quantity
        "",                  # keep tested
        "",                  # keep status
        "",                  # keep URL
        "",                  # keep notes
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(responses),
    )

    monkeypatch.setattr(
        "gear.save_gear",
        lambda gear: None,
    )

    edit_gear(gear)

    assert gear[0]["brand_model"] == "Sawyer Squeeze 2"


def test_edit_gear_changes_category_and_ownership(monkeypatch):
    gear = [
        {
            "id": 1,
            "category": "Water",
            "subcategory": "Filter",
            "brand_model": "Sawyer Squeeze",
            "weight_oz": 3.0,
            "cost": 45.99,
            "comfort": None,
            "durability": 5,
            "ease_of_use": 4,
            "protection_warmth": None,
            "owned": True,
            "quantity_owned": 1,
            "tested": True,
            "status": "Active",
            "source_url": "",
            "notes": "",
        }
    ]

    responses = iter([
        "1",   # choose item
        "2",   # category -> Shelter
        "1",   # subcategory -> Tent
        "",    # keep brand/model
        "",    # keep weight
        "",    # keep cost
        "",    # keep comfort
        "",    # keep durability
        "",    # keep ease
        "",    # keep protection
        "n",   # owned -> No
        "",    # keep tested
        "2",   # status -> Considering
        "",    # keep URL
        "",    # keep notes
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(responses),
    )

    monkeypatch.setattr(
        "gear.save_gear",
        lambda gear: None,
    )

    edit_gear(gear)

    item = gear[0]

    assert item["category"] == "Shelter"
    assert item["subcategory"] == "Tent"
    assert item["owned"] is False
    assert item["quantity_owned"] == 0
    assert item["status"] == "Considering"


def test_edit_gear_empty(capsys):
    edit_gear([])

    output = capsys.readouterr().out

    assert "No gear added yet." in output


def test_edit_gear_invalid_number(monkeypatch, capsys):
    gear = [
        {
            "id": 1,
            "category": "Water",
            "subcategory": "Filter",
            "brand_model": "Sawyer Squeeze",
            "weight_oz": 3.0,
            "cost": 45.99,
            "comfort": None,
            "durability": 5,
            "ease_of_use": 4,
            "protection_warmth": None,
            "owned": True,
            "quantity_owned": 1,
            "tested": True,
            "status": "Active",
            "source_url": "",
            "notes": "",
        }
    ]

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "2",
    )

    edit_gear(gear)

    output = capsys.readouterr().out

    assert "Invalid gear item number." in output


def test_delete_gear(monkeypatch):
    gear = [
        {
            "id": 1,
            "category": "Water",
            "subcategory": "Filter",
            "brand_model": "Sawyer Squeeze",
            "weight_oz": 3.0,
            "cost": 45.99,
            "comfort": None,
            "durability": 5,
            "ease_of_use": 4,
            "protection_warmth": None,
            "owned": True,
            "quantity_owned": 1,
            "tested": True,
            "status": "Active",
            "source_url": "",
            "notes": "",
        }
    ]

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "1",
    )

    save_called = {"value": False}

    def fake_save_gear(items):
        save_called["value"] = True

    monkeypatch.setattr(
        "gear.save_gear",
        fake_save_gear,
    )

    delete_gear(gear)

    assert gear == []
    assert save_called["value"] is True


def test_delete_gear_empty(capsys):
    delete_gear([])

    output = capsys.readouterr().out

    assert "No gear added yet." in output


def test_delete_gear_invalid_number(monkeypatch, capsys):
    gear = [
        {
            "id": 1,
            "category": "Water",
            "subcategory": "Filter",
            "brand_model": "Sawyer Squeeze",
            "weight_oz": 3.0,
            "cost": 45.99,
            "comfort": None,
            "durability": 5,
            "ease_of_use": 4,
            "protection_warmth": None,
            "owned": True,
            "quantity_owned": 1,
            "tested": True,
            "status": "Active",
            "source_url": "",
            "notes": "",
        }
    ]

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "2",
    )

    delete_gear(gear)

    output = capsys.readouterr().out

    assert "Invalid gear item number." in output
    assert len(gear) == 1