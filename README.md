# Hiking Tracker

Hiking Tracker is a Python command-line application for logging hikes, reviewing hike details, and analyzing hiking statistics.

The project started as a Boot.dev personal project and is intended to grow into a broader hiking and training application with features for gear management, trip planning, training analysis, and integrations with popular hiking and fitness platforms.

## Current Features

- Log a hike
- View all logged hikes
- View detailed information for an individual hike
- Edit existing hikes
- Delete hikes
- Save hike data in JSON format
- Input validation for dates, times, integers, and decimal values
- All-time hiking statistics
- Monthly hiking statistics
- Pace calculation
- Elevation gain per mile
- Persistent data storage between program runs

## Hike Data

Each hike currently includes:

- Date
- Trail name
- Distance in miles
- Elevation gain in feet
- Total time
- Pack weight

Example:

```json
{
    "date": "2026-08-15",
    "trail": "Example Trail",
    "distance": 6.4,
    "elevation_gain": 1200,
    "total_time": 165,
    "pack_weight": 18.0
}
```

Dates are stored using the `YYYY-MM-DD` format.

Total hike time is stored internally as minutes to simplify calculations and statistics.

## Project Structure

```text
hiking-tracker/
├── main.py
├── hikes.py
├── hike_statistics.py
├── input_utils.py
├── storage.py
├── hikes.json
├── pyproject.toml
└── README.md
```

### `main.py`

Runs the application menu and routes user selections to the appropriate functions.

### `hikes.py`

Contains the primary hike operations, including logging, viewing, editing, and deleting hikes.

### `hike_statistics.py`

Contains calculations and reporting for hiking statistics such as pace, elevation gain per mile, all-time statistics, and monthly statistics.

### `input_utils.py`

Contains reusable input validation and formatting helper functions.

### `storage.py`

Handles loading and saving hike data.

## Running the Application

The project uses Python and `uv`.

From the project directory:

```bash
uv run main.py
```

## Planned Improvements

### Stronger Numeric Validation

The current input helpers verify that numeric input can be converted to an integer or floating-point value.

A future enhancement will also validate whether the number makes sense for the field being entered.

For example, the application should reject values such as:

```text
Distance: -5
Elevation Gain: -900
Pack Weight: -20
```

The input helpers may be expanded to accept optional minimum and maximum values so the same validation logic can be reused throughout the application.

Example concept:

```python
def get_float(prompt, minimum=None):
    ...
```

This could allow calls such as:

```python
distance = get_float("Distance (miles): ", minimum=0)
```

### Safer JSON Data Storage

Hike data is currently written directly to `hikes.json`.

If an error occurs while the file is being written, there is a possibility that the existing JSON file could become incomplete or corrupted.

A future version will use an atomic-save strategy:

1. Write the updated hike data to a temporary file.
2. Confirm that the complete JSON data was written successfully.
3. Replace the existing `hikes.json` file with the temporary file.

This reduces the risk of losing previously stored hiking data if a save operation fails.

### Automated Testing

The project is currently tested primarily through manual application testing.

A future enhancement will introduce automated tests, likely using `pytest`.

Good initial candidates for automated testing include:

```python
calculate_pace()
format_pace()
calculate_elevation_per_mile()
get_hikes_for_month()
```

Future shared statistics functions such as:

```python
calculate_statistics()
```

should also be tested.

Example:

```python
def test_calculate_pace():
    assert calculate_pace(60, 3) == 20
```

Automated testing will make it safer to refactor and expand the application because existing behavior can be verified after each change.

## Longer-Term Ideas

Possible future capabilities include:

- Yearly and custom date-range statistics
- Moving-time tracking
- Training goals and progress tracking
- Gear inventory and pack-weight management
- Trip planning
- Planned versus actual hike comparisons
- AllTrails and other hiking-app imports
- Garmin or Strava integration
- Weather integration
- Trail library
- Notes and trail-condition tracking
- Personal hiking records
- Search and filtering
- Graphical or web-based user interface
- PCT and long-distance hiking training tools

## Development Status

Hiking Tracker is under active development as a Python learning project. Features and architecture will continue to evolve as new programming concepts are introduced.
