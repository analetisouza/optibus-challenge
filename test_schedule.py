from schedule import Schedule

def test_find_vehicle_event():
    vehicles = [{"vehicle_id": "1",
			     "vehicle_events": [
				{
					"vehicle_event_sequence": "0",
					"vehicle_event_type": "pre_trip",
					"start_time": "0.03:15",
					"end_time": "0.03:35",
					"origin_stop_id": "Pomona",
					"destination_stop_id": "Pomona",
					"duty_id": "110"
				}]}]
    stops, trips, duties = [], [], []
    vehicle_event = {
					"vehicle_event_sequence": "0",
					"vehicle_event_type": "pre_trip",
					"start_time": "0.03:15",
					"end_time": "0.03:35",
					"origin_stop_id": "Pomona",
					"destination_stop_id": "Pomona",
					"duty_id": "110"
				}
    schedule = Schedule(stops, trips, vehicles, duties)
    assert schedule.find_vehicle_event("110", "0") == vehicle_event

def test_get_time():
    vehicles = [{"vehicle_id": "1",
			     "vehicle_events": [
				{
					"vehicle_event_sequence": "0",
					"vehicle_event_type": "pre_trip",
					"start_time": "0.03:15",
					"end_time": "0.03:35",
					"origin_stop_id": "Pomona",
					"destination_stop_id": "Pomona",
					"duty_id": "110"
				}]}]
    stops, trips, duties = [], [], []
    duty_event = {
					"duty_event_sequence": "0",
					"duty_event_type": "vehicle_event",
					"vehicle_event_sequence": 0,
					"vehicle_id": "2"
				}
    schedule = Schedule(stops, trips, vehicles, duties)
    assert schedule.get_time(duty_event, 'first', "110") == "0.03:15"

def test_find_stop():
    stops = [{
			"stop_id": "Pomona",
			"stop_name": "Pomona Yard",
			"latitude": 34.057907,
			"longitude": -117.723094,
			"is_depot": True
		}]
    vehicles, trips, duties = [], [], []
    schedule = Schedule(stops, trips, vehicles, duties)
    assert schedule.find_stop("Pomona") == stops[0]

def test_get_stop():
    vehicles = [{"vehicle_id": "1",
			     "vehicle_events": [
				{
					"vehicle_event_sequence": "0",
					"vehicle_event_type": "pre_trip",
					"start_time": "0.03:15",
					"end_time": "0.03:35",
					"origin_stop_id": "Pomona",
					"destination_stop_id": "Pomona",
					"duty_id": "110"
				}]}]
    stops = [{
			"stop_id": "Pomona",
			"stop_name": "Pomona Yard",
			"latitude": 34.057907,
			"longitude": -117.723094,
			"is_depot": True
		}]
    trips, duties = [], []
    duty_event = {
					"duty_event_sequence": "0",
					"duty_event_type": "vehicle_event",
					"vehicle_event_sequence": 0,
					"vehicle_id": "2"
				}
    schedule = Schedule(stops, trips, vehicles, duties)
    assert schedule.get_stop(duty_event, 'first', "110") == "Pomona Yard"

def test_find_trip():
    trips = [		{
			"trip_id": "5306808",
			"route_number": "492",
			"origin_stop_id": "EMS",
			"destination_stop_id": "MTC",
			"departure_time": "0.07:45",
			"arrival_time": "0.09:10"
		}]
    stops, vehicles, duties = [], [], []
    schedule = Schedule(stops, trips, vehicles, duties)
    assert schedule.find_trip("5306808") == trips[0]

def test_get_service_stop():
    duties = [{"duty_id": "110",
			   "duty_events": [
				{
					"duty_event_sequence": "2",
					"duty_event_type": "vehicle_event",
					"vehicle_event_sequence": 2,
					"vehicle_id": "1"
				}]}]
    vehicles = [{"vehicle_id": "1",
			     "vehicle_events": [{
					"vehicle_event_sequence": "2",
					"vehicle_event_type": "service_trip",
					"trip_id": "5301431",
					"duty_id": "110"
				}]}]
    trips = [{
			"trip_id": "5301431",
			"route_number": "488",
			"origin_stop_id": "CiGL",
			"destination_stop_id": "EMS",
			"departure_time": "0.04:10",
			"arrival_time": "0.05:22"
		}]
    stops = [{
			"stop_id": "CiGL",
			"stop_name": "Citrus Gold Line Station",
			"latitude": 34.135898,
			"longitude": -117.88926,
			"is_depot": False
		}]
    schedule = Schedule(stops, trips, vehicles, duties)
    assert schedule.get_service_stop(duties[0]) == stops[0]

def test_calculate_break_duration():
    stops, trips, vehicles, duties = [], [], [], []
    schedule = Schedule(stops, trips, vehicles, duties)
    start_time = "0.20.30"
    end_time = "0.21.00"
    assert schedule.calculate_break_duration(start_time, end_time) == 30

def test_calculate_break_duration_overnight():
    stops, trips, vehicles, duties = [], [], [], []
    schedule = Schedule(stops, trips, vehicles, duties)
    start_time = "0.23.30"
    end_time = "1.00.30"
    assert schedule.calculate_break_duration(start_time, end_time) == 60