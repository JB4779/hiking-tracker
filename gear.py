from input_utils import (
    get_int,
    get_float,
    get_optional_float,
    get_optional_int,
    get_optional_rating,
)

from gear_storage import save_gear

from config_loader import load_gear_config

GEAR_CONFIG = load_gear_config()
DEFAULT_GEAR_STATUS = GEAR_CONFIG["default_status"]
GEAR_SUBCATEGORIES = GEAR_CONFIG["categories"]
GEAR_CATEGORIES = list(GEAR_SUBCATEGORIES.keys())
GEAR_STATUSES = GEAR_CONFIG["statuses"]


def select_category():
    print("\nGEAR CATEGORIES")

    for index, category in enumerate(GEAR_CATEGORIES, start=1):
        print(f"{index}. {category}")

    while True:
        choice = get_int(
            "Select category: ",
            minimum=1,
        )

        if choice <= len(GEAR_CATEGORIES):
            return GEAR_CATEGORIES[choice - 1]

        print(
            f"Invalid category. Please choose 1-{len(GEAR_CATEGORIES)}."
        )


def select_optional_category(current_category):
    print("\nGEAR CATEGORIES")
    print(f"Current: {current_category}")

    for index, category in enumerate(GEAR_CATEGORIES, start=1):
        print(f"{index}. {category}")

    while True:
        choice = input(
            "Select category or press Enter to keep current: "
        )

        if choice == "":
            return current_category

        try:
            choice = int(choice)

            if 1 <= choice <= len(GEAR_CATEGORIES):
                return GEAR_CATEGORIES[choice - 1]

            print(
                f"Invalid category. "
                f"Please choose 1-{len(GEAR_CATEGORIES)}."
            )

        except ValueError:
            print(
                f"Invalid category. "
                f"Please choose 1-{len(GEAR_CATEGORIES)}."
            )


def select_subcategory(category):
    subcategories = GEAR_SUBCATEGORIES[category]

    print(f"\n{category.upper()} SUBCATEGORIES")

    for index, subcategory in enumerate(subcategories, start=1):
        print(f"{index}. {subcategory}")

    while True:
        choice = get_int(
            "Select subcategory: ",
            minimum=1,
        )

        if choice <= len(subcategories):
            return subcategories[choice - 1]

        print(
            f"Invalid subcategory. "
            f"Please choose 1-{len(subcategories)}."
        )


def select_optional_subcategory(category, current_subcategory):
    subcategories = GEAR_SUBCATEGORIES.get(category)

    if subcategories is None:
        print(f"Unknown gear category: {category}")
        return current_subcategory

    print(f"\n{category.upper()} SUBCATEGORIES")

    if current_subcategory in subcategories:
        print(f"Current: {current_subcategory}")
    else:
        print(
            f"Current: {current_subcategory} "
            f"(not valid for {category})"
        )

    for index, subcategory in enumerate(subcategories, start=1):
        print(f"{index}. {subcategory}")

    while True:
        choice = input(
            "Select subcategory or press Enter to keep current: "
        )

        if choice == "":
            if current_subcategory in subcategories:
                return current_subcategory

            print(
                "Current subcategory is not valid for this category. "
                "Please choose a new subcategory."
            )
            continue

        try:
            choice = int(choice)

            if 1 <= choice <= len(subcategories):
                return subcategories[choice - 1]

            print(
                f"Invalid subcategory. "
                f"Please choose 1-{len(subcategories)}."
            )

        except ValueError:
            print(
                f"Invalid subcategory. "
                f"Please choose 1-{len(subcategories)}."
            )


def select_status():
    print("\nGEAR STATUS")

    for index, status in enumerate(GEAR_STATUSES, start=1):
        print(f"{index}. {status}")

    while True:
        choice = get_int(
            "Select status: ",
            minimum=1,
        )

        if choice <= len(GEAR_STATUSES):
            return GEAR_STATUSES[choice - 1]

        print(
            f"Invalid status. "
            f"Please choose 1-{len(GEAR_STATUSES)}."
        )


def select_optional_status(current_status):
    print("\nGEAR STATUS")
    print(f"Current: {current_status}")

    for index, status in enumerate(GEAR_STATUSES, start=1):
        print(f"{index}. {status}")

    while True:
        choice = input(
            "Select status or press Enter to keep current: "
        )

        if choice == "":
            return current_status

        try:
            choice = int(choice)

            if 1 <= choice <= len(GEAR_STATUSES):
                return GEAR_STATUSES[choice - 1]

            print(
                f"Invalid status. "
                f"Please choose 1-{len(GEAR_STATUSES)}."
            )

        except ValueError:
            print(
                f"Invalid status. "
                f"Please choose 1-{len(GEAR_STATUSES)}."
            )


def create_gear_item(
    item_id,
    category,
    subcategory,
    brand_model,
    weight_oz,
    cost,
    comfort=None,
    durability=None,
    ease_of_use=None,
    protection_warmth=None,
    owned=False,
    quantity_owned=0,
    tested=False,
    status=DEFAULT_GEAR_STATUS,
    source_url="",
    notes="",
):
    return {
        "id": item_id,
        "category": category,
        "subcategory": subcategory,
        "brand_model": brand_model,
        "weight_oz": weight_oz,
        "cost": cost,
        "comfort": comfort,
        "durability": durability,
        "ease_of_use": ease_of_use,
        "protection_warmth": protection_warmth,
        "owned": owned,
        "quantity_owned": quantity_owned,
        "tested": tested,
        "status": status,
        "source_url": source_url,
        "notes": notes,
    }


def get_next_gear_id(gear):
    if not gear:
        return 1

    return max(item["id"] for item in gear) + 1


def add_gear(gear):
    item_id = get_next_gear_id(gear)

    category = select_category()
    subcategory = select_subcategory(category)
    brand_model = input("Brand / Model: ")

    weight_oz = get_float("Weight (oz): ", minimum=0)
    cost = get_float("Cost ($): ", minimum=0)

    comfort = get_optional_rating(
        "Comfort (1-5, Enter for N/A): "
    )

    durability = get_optional_rating(
        "Durability (1-5, Enter for N/A): "
    )

    ease_of_use = get_optional_rating(
        "Ease of Use (1-5, Enter for N/A): "
    )

    protection_warmth = get_optional_rating(
        "Protection / Warmth (1-5, Enter for N/A): "
    )

    owned_input = input("Owned? (y/n): ").lower()
    owned = owned_input == "y"

    if owned:
        quantity_owned = get_int(
            "Quantity owned: ",
            minimum=1,
        )
    else:
        quantity_owned = 0

    tested_input = input("Tested? (y/n): ").lower()
    tested = tested_input == "y"

    status = select_status()
    source_url = input("Source URL: ")
    notes = input("Notes: ")

    item = create_gear_item(
        item_id=item_id,
        category=category,
        subcategory=subcategory,
        brand_model=brand_model,
        weight_oz=weight_oz,
        cost=cost,
        comfort=comfort,
        durability=durability,
        ease_of_use=ease_of_use,
        protection_warmth=protection_warmth,
        owned=owned,
        quantity_owned=quantity_owned,
        tested=tested,
        status=status,
        source_url=source_url,
        notes=notes,
    )

    gear.append(item)
    save_gear(gear)

    print(f"Added gear: {brand_model}")


def view_gear(gear):
    if not gear:
        print("No gear added yet.")
        return

    print("\nGEAR INVENTORY")

    for index, item in enumerate(gear, start=1):
        owned_text = "Owned" if item["owned"] else "Not Owned"

        print(
            f"{index}. "
            f"{item['category']} - "
            f"{item['brand_model']} - "
            f"{item['weight_oz']:.1f} oz - "
            f"{owned_text} - "
            f"{item['status']}"
        )


def view_gear_details(gear):
    if not gear:
        print("No gear added yet.")
        return

    view_gear(gear)

    index = get_int(
        "Enter the number of the gear item: ",
        minimum=1,
    ) - 1

    if 0 <= index < len(gear):
        item = gear[index]

        owned_text = "Yes" if item["owned"] else "No"
        tested_text = "Yes" if item["tested"] else "No"

        print(f"\nGEAR DETAILS")
        print(f"Category: {item['category']}")
        print(f"Subcategory: {item['subcategory']}")
        print(f"Brand / Model: {item['brand_model']}")
        print(f"Weight: {item['weight_oz']:.1f} oz")
        print(f"Cost: ${item['cost']:.2f}")

        print(f"Comfort: {item['comfort']}")
        print(f"Durability: {item['durability']}")
        print(f"Ease of Use: {item['ease_of_use']}")
        print(f"Protection / Warmth: {item['protection_warmth']}")

        print(f"Owned: {owned_text}")
        print(f"Quantity Owned: {item['quantity_owned']}")
        print(f"Tested: {tested_text}")
        print(f"Status: {item['status']}")

        print(f"Source URL: {item['source_url']}")
        print(f"Notes: {item['notes']}")

    else:
        print("Invalid gear item number.")


def edit_gear(gear):
    if not gear:
        print("No gear added yet.")
        return

    view_gear(gear)

    index = get_int(
        "Enter the number of the gear item to edit: ",
        minimum=1,
    ) - 1

    if not 0 <= index < len(gear):
        print("Invalid gear item number.")
        return

    item = gear[index]

    category = select_optional_category(item["category"])

    subcategory = select_optional_subcategory(
        category,
        item["subcategory"],
    )

    brand_model = input(
        f"Brand / Model [{item['brand_model']}]: "
    )
    if brand_model == "":
        brand_model = item["brand_model"]

    weight_oz = get_optional_float(
        f"Weight (oz) [{item['weight_oz']}]: ",
        item["weight_oz"],
        minimum=0,
    )

    cost = get_optional_float(
        f"Cost ($) [{item['cost']}]: ",
        item["cost"],
        minimum=0,
    )

    comfort = get_optional_rating(
        f"Comfort (1-5) [{item['comfort']}]: "
    )
    if comfort is None:
        comfort = item["comfort"]

    durability = get_optional_rating(
        f"Durability (1-5) [{item['durability']}]: "
    )
    if durability is None:
        durability = item["durability"]

    ease_of_use = get_optional_rating(
        f"Ease of Use (1-5) [{item['ease_of_use']}]: "
    )
    if ease_of_use is None:
        ease_of_use = item["ease_of_use"]

    protection_warmth = get_optional_rating(
        f"Protection / Warmth (1-5) [{item['protection_warmth']}]: "
    )
    if protection_warmth is None:
        protection_warmth = item["protection_warmth"]

    owned_input = input(
        f"Owned? (y/n) [{'y' if item['owned'] else 'n'}]: "
    ).lower()

    if owned_input == "":
        owned = item["owned"]
    else:
        owned = owned_input == "y"

    if owned:
        quantity_owned = get_optional_int(
            f"Quantity Owned [{item['quantity_owned']}]: ",
            item["quantity_owned"],
            minimum=1,
        )
    else:
        quantity_owned = 0

    tested_input = input(
        f"Tested? (y/n) [{'y' if item['tested'] else 'n'}]: "
    ).lower()

    if tested_input == "":
        tested = item["tested"]
    else:
        tested = tested_input == "y"

    status = select_optional_status(item["status"])

    source_url = input(
        f"Source URL [{item['source_url']}]: "
    )
    if source_url == "":
        source_url = item["source_url"]

    notes = input(
        f"Notes [{item['notes']}]: "
    )
    if notes == "":
        notes = item["notes"]

    item.update(
        {
            "category": category,
            "subcategory": subcategory,
            "brand_model": brand_model,
            "weight_oz": weight_oz,
            "cost": cost,
            "comfort": comfort,
            "durability": durability,
            "ease_of_use": ease_of_use,
            "protection_warmth": protection_warmth,
            "owned": owned,
            "quantity_owned": quantity_owned,
            "tested": tested,
            "status": status,
            "source_url": source_url,
            "notes": notes,
        }
    )

    save_gear(gear)

    print(f"Updated gear: {item['brand_model']}")


def delete_gear(gear):
    if not gear:
        print("No gear added yet.")
        return

    view_gear(gear)

    index = get_int(
        "Enter the number of the gear item to delete: ",
        minimum=1,
    ) - 1

    if 0 <= index < len(gear):
        deleted_item = gear.pop(index)

        save_gear(gear)

        print(f"Deleted gear: {deleted_item['brand_model']}")
    else:
        print("Invalid gear item number.")