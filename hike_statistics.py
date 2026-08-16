from input_utils import format_time

def view_statistics(hikes):
    if not hikes:
        print("No hikes logged yet.")
        return
    
    total_distance = sum(hike['distance'] for hike in hikes)
    total_elevation_gain = sum(hike['elevation_gain'] for hike in hikes)
    total_time = sum(hike['total_time'] for hike in hikes)
    average_distance = total_distance / len(hikes)
    average_pace = calculate_pace(total_time, total_distance)
    average_elevation_gain = total_elevation_gain / len(hikes)
    average_time = total_time / len(hikes)
    longest_hike = max(hikes, key=lambda hike: hike["distance"])
    shortest_hike = min(hikes, key=lambda hike: hike["distance"])

    print(f"Total Hikes: {len(hikes)}")
    print(f"Total Distance: {total_distance:.2f} miles")
    print(f"Total Elevation Gain: {total_elevation_gain} feet")
    print(f"Total Time: {format_time(total_time)}")
    print(f"Average Distance: {average_distance:.2f} miles")
    print(f"Average Pace: {format_pace(average_pace)} / mile")
    print(f"Average Elevation Gain: {average_elevation_gain:.2f} feet")
    print(f"Average Time: {average_time:.2f} minutes")
    print(f"Longest Hike: {longest_hike['trail']} - {longest_hike['distance']:.2f} miles")
    print(f"Shortest Hike: {shortest_hike['trail']} - {shortest_hike['distance']:.2f} miles")


def calculate_pace(total_time, distance):
    if distance == 0:
        return 0
    return total_time / distance

def format_pace(pace):
    if pace == 0:
        return "0:00"
    
    hours = int(pace // 60)
    minutes = int(pace % 60)
    seconds = round((pace - minutes) * 60)
    return f"{minutes}:{seconds:02}"