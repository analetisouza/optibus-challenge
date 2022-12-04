class Schedule: 
    def __init__(self, stops, trips, vehicles, duties):
        self.stops = stops
        self.trips = trips
        self.vehicles = vehicles
        self.duties = duties 

    def find_vehicle_event(self, duty_id, vehicle_event_sequence):
        for item in self.vehicles:
            for event in item['vehicle_events']:
                #print('{} {} {} {}'.format(event['duty_id'], duty_id, event['vehicle_event_sequence'], vehicle_event_sequence))
                #print('{} {} {} {}'.format(type(event['duty_id']), type(duty_id), type(event['vehicle_event_sequence']), type(vehicle_event_sequence)))
                if event['duty_id'] == duty_id and event['vehicle_event_sequence'] == str(vehicle_event_sequence):
                    return event

        return 'raise error'
        

    def get_time(self, event, position, duty_id):
        if position == 'first':
            if event['duty_event_type'] == 'vehicle_event':
                vehicle_event = self.find_vehicle_event(duty_id, event['vehicle_event_sequence'])
                time = vehicle_event['start_time']
            else:
                time = event['start_time']
        elif position == 'last': 
            if event['duty_event_type'] == 'vehicle_event':
                vehicle_event = self.find_vehicle_event(duty_id, event['vehicle_event_sequence'])
                time = vehicle_event['end_time']
            else:
                time = event['end_time']
        else:
            time = 'raise error'

        return time

    def find_stop(self, stop_id):
        for stop in self.stops:
            if stop['stop_id'] == stop_id:
                return stop

        return 'raise error'

    def get_stop(self, event, position, duty_id):
        if position == 'first':
            if event['duty_event_type'] == 'vehicle_event':
                vehicle_event = self.find_vehicle_event(duty_id, event['vehicle_event_sequence'])
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
                stop_id = vehicle_event['destination_stop_id']
                stop = self.find_stop(stop_id)
                stop_name = stop['stop_name']
            else:
                stop_id = event['destination_stop_id']
                stop = self.find_stop(stop_id)
                stop_name = stop['stop_name']
        else:
            stop_name = 'raise error'

        return stop_name

    def find_trip(self, trip_id):
        for trip in self.trips:
            if trip['trip_id'] == trip_id:
                return trip

        return 'raise error'

