def top_five_pickup_zones(trips):
    zone_counts = {}

    # Count trips per zone
    for trip in trips:
        zone = trip["pickup_zone_id"]

        if zone in zone_counts:
            zone_counts[zone] += 1
        else:
            zone_counts[zone] = 1

    top_five = []

    # Manual selection of top 5
    for i in range(5):
        max_zone = None
        max_count = 0

        for zone in zone_counts:
            if zone_counts[zone] > max_count:
                max_zone = zone
                max_count = zone_counts[zone]

        if max_zone is not None:
            top_five.append((max_zone, max_count))
            zone_counts[max_zone] = -1

    return top_five
