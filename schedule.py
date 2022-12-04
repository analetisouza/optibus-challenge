from datetime import timedelta
class Schedule: 
    def __init__(self, stops, trips, vehicles, duties):
        self.stops = stops
        self.trips = trips
        self.vehicles = vehicles
        self.duties = duties 

    def find_vehicle_event(self, duty_id, vehicle_event_sequence):
        for item in self.vehicles:
            for event in item['vehicle_events']:
                if event['duty_id'] == duty_id and event['vehicle_event_sequence'] == str(vehicle_event_sequence):
                    return event
        raise DataNotFoundError(message="The vehicle event was not found.")      

    def get_time(self, event, position, duty_id):
        if position == 'first':
            if event['duty_event_type'] == 'vehicle_event':
                vehicle_event = self.find_vehicle_event(duty_id, event['vehicle_event_sequence'])
                if vehicle_event['vehicle_event_type'] == 'service_trip':
                    trip = self.find_trip(vehicle_event['trip_id'])
                    time = trip['departure_time']
                else:
                    time = vehicle_event['start_time']
            else:
                time = event['start_time']
        elif position == 'last': 
            if event['duty_event_type'] == 'vehicle_event':
                vehicle_event = self.find_vehicle_event(duty_id, event['vehicle_event_sequence'])
                if vehicle_event['vehicle_event_type'] == 'service_trip':
                    trip = self.find_trip(vehicle_event['trip_id'])
                    time = trip['arrival_time']
                else:
                    time = time = vehicle_event['start_time']
            else:
                time = event['end_time']
        else:
            raise OptionInvalidError()
        return time

    def find_stop(self, stop_id):
        for stop in self.stops:
            if stop['stop_id'] == stop_id:
                return stop
        raise DataNotFoundError(message="The stop was not found")

    def get_stop(self, event, position, duty_id):
        if position == 'first':
            if event['duty_event_type'] == 'vehicle_event':
                vehicle_event = self.find_vehicle_event(duty_id, event['vehicle_event_sequence'])
                if vehicle_event['vehicle_event_type'] == 'service_trip':
                    trip = self.find_trip(vehicle_event['trip_id'])
                    stop_id = trip['origin_stop_id']
                    stop = self.find_stop(stop_id)
                    stop_name = stop['stop_name']
                else:
                    stop_id = vehicle_event['origin_stop_id']
                    stop = self.find_stop(stop_id)
                    stop_name = stop['stop_name']
            else:
                stop_id = event['origin_stop_id']
                stop = self.find_stop(stop_id)
                stop_name = stop['stop_name']

        elif position == 'last': 
            if event['duty_event_type'] == 'vehicle_event':
                vehicle_event = self.find_vehicle_event(duty_id, event['vehicle_event_sequence'])
                if vehicle_event['vehicle_event_type'] == 'service_trip':
                    trip = self.find_trip(vehicle_event['trip_id'])
                    stop_id = trip['destination_stop_id']
                    stop = self.find_stop(stop_id)
                    stop_name = stop['stop_name']
                else:
                    stop_id = vehicle_event['destination_stop_id']
                    stop = self.find_stop(stop_id)
                    stop_name = stop['stop_name']
            else:
                stop_id = event['destination_stop_id']
                stop = self.find_stop(stop_id)
                stop_name = stop['stop_name']
        else:
            raise OptionInvalidError()
        return stop_name

    def find_trip(self, trip_id):
        for trip in self.trips:
            if trip['trip_id'] == trip_id:
                return trip
        raise DataNotFoundError(message="The trip was not found.")

    def get_service_stop(self, duty):
        for event in duty['duty_events']:
            if event['duty_event_type'] == 'vehicle_event': 
                vehicle_event = self.find_vehicle_event(duty['duty_id'], event['vehicle_event_sequence'])
                if vehicle_event['vehicle_event_type'] == 'service_trip':
                    trip = self.find_trip(vehicle_event['trip_id'])    
                    stop = self.find_stop(trip['origin_stop_id'])
                    return stop
        raise DataNotFoundError(message="A service stop was not found.")

    def calculate_break_duration(self, start_time, end_time):
        start_time = timedelta(days= int(start_time[0]), hours=int(start_time[2:4]), minutes=int(start_time[5:]))
        end_time = timedelta(days= int(end_time[0]), hours=int(end_time[2:4]), minutes=int(end_time[5:]))
        duration = end_time - start_time
        return int(duration.total_seconds() / 60)

class Error(Exception):
    pass

class DataNotFoundError(Error):
    def __init__(self, message="The data was not found."):
        self.message = message
        super().__init__(self.message)

class OptionInvalidError(Error):
    def __init__(self, message="The argument provided is invalid."):
        self.message = message
        super().__init__(self.message)