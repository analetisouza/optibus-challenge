import json

def main():
    with open('mini_json_dataset.json') as json_file:
        data = json_file.read()
    parsed_data = json.loads(data)
    stops = parsed_data['stops']
    trips = parsed_data['trips']
    vehicles = parsed_data['vehicles']
    duties = parsed_data['duties']

    for duty in range(len(duties)):
        #print((duties[duty].keys()))
        current_duty = duties[duty]
        last_event_position = len(current_duty['duty_events']) - 1
        first_event = current_duty['duty_events'][0]
        last_event = current_duty['duty_events'][last_event_position]
        print(current_duty['duty_id'])
        print(get_time(first_event, 'first'))
        print(get_time(last_event, 'last'))

    return

def get_time(event, position):
    if position == 'first':
        if event['duty_event_type'] == 'vehicle_event':
            time = 'will be here'
        else:
            time = event['start_time']
    elif position == 'last': 
        if event['duty_event_type'] == 'vehicle_event':
            time = 'will be here'
        else:
            time = event['end_time']
    else:
        time = 'raise error'

    return time

def find_vehicle_event():
    return

if __name__ == "__main__":
    main()

