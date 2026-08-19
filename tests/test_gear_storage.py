import gear_storage


def test_save_and_load_gear(tmp_path, monkeypatch):
    test_file = tmp_path / "gear.json"
    temp_file = tmp_path / "gear.tmp"

    monkeypatch.setattr(
        gear_storage,
        "GEAR_FILE",
        test_file,
    )

    monkeypatch.setattr(
        gear_storage,
        "TEMP_FILE",
        temp_file,
    )

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

    gear_storage.save_gear(gear)

    loaded_gear = gear_storage.load_gear()

    assert loaded_gear == gear


def test_load_gear_file_not_found(tmp_path, monkeypatch):
    test_file = tmp_path / "missing.json"

    monkeypatch.setattr(
        gear_storage,
        "GEAR_FILE",
        test_file,
    )

    result = gear_storage.load_gear()

    assert result == []