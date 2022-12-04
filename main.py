from schedule import Schedule
import json

def main():
    with open('mini_json_dataset.json') as json_file:
        data = json_file.read()
    parsed_data = json.loads(data)
    stops = parsed_data['stops']
    trips = parsed_data['trips']
    vehicles = parsed_data['vehicles']
    duties = parsed_data['duties']

    schedule = Schedule(stops, trips, vehicles, duties)
    #step_one(schedule)
    step_two(schedule)
    return

def step_one(schedule):
    for duty in range(len(schedule.duties)):
        #print((duties[duty].keys()))
        current_duty = schedule.duties[duty]
        last_event_position = len(current_duty['duty_events']) - 1
        first_event = current_duty['duty_events'][0]
        last_event = current_duty['duty_events'][last_event_position]
        print('{} | {} | {}'.format(current_duty['duty_id'], 
                                    schedule.get_time(first_event, 'first', current_duty['duty_id'])[2:], 
                                    schedule.get_time(last_event, 'last', current_duty['duty_id'])[2:]))

    return

def step_two(schedule):
    for duty in range(len(schedule.duties)):
        #print((duties[duty].keys()))
        current_duty = schedule.duties[duty]
        for duty_event in current_duty['duty_events']:
            if duty_event['duty_event_type'] == 'vehicle_event': 
                first_vehicle_event = schedule.find_vehicle_event(current_duty['duty_id'], duty_event['vehicle_event_sequence'])
                if first_vehicle_event['vehicle_event_type'] == 'service_trip':
                    first_trip = schedule.find_trip(first_vehicle_event['trip_id'])    
                    first_stop = schedule.find_stop(first_trip['origin_stop_id'])
                    break
        current_duty['duty_events'].reverse()
        for duty_event in current_duty['duty_events']:
            if duty_event['duty_event_type'] == 'vehicle_event': 
                last_vehicle_event = schedule.find_vehicle_event(current_duty['duty_id'], duty_event['vehicle_event_sequence'])
                if last_vehicle_event['vehicle_event_type'] == 'service_trip':
                    last_trip = schedule.find_trip(last_vehicle_event['trip_id'])    
                    last_stop = schedule.find_stop(last_trip['origin_stop_id'])
                    break

        last_event_position = len(current_duty['duty_events']) - 1
        first_event = current_duty['duty_events'][0]
        last_event = current_duty['duty_events'][last_event_position]
        print('{} | {} | {} | {} | {}'.format(current_duty['duty_id'], 
                                    schedule.get_time(first_event, 'first', current_duty['duty_id'])[2:], 
                                    schedule.get_time(last_event, 'last', current_duty['duty_id'])[2:], 
                                    first_stop['stop_name'], 
                                    last_stop['stop_name']))

    return

if __name__ == "__main__":
    main()

