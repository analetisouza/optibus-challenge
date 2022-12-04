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

    option = 0
    print("""
    Type the number according to the desired report:
            1 - Start and End Time
            2 - Start and End Stop Name
            3 - Breaks
            """)
    option = int(input())
    if option == 1:
        step_one(schedule)
    elif option == 2:
        step_two(schedule)
    elif option == 3:
        step_three(schedule)
    else:
        print("You typed an invalid option. Please try again.")

    return

def step_one(schedule):
    print("Duty ID | Start Time | End Time")
    for duty in range(len(schedule.duties)):
        current_duty = schedule.duties[duty]
        last_event_position = len(current_duty['duty_events']) - 1
        first_event = current_duty['duty_events'][0]
        last_event = current_duty['duty_events'][last_event_position]
        print('{} | {} | {}'.format(current_duty['duty_id'], 
                                    schedule.get_time(first_event, 'first', current_duty['duty_id'])[2:], 
                                    schedule.get_time(last_event, 'last', current_duty['duty_id'])[2:]))

    return

def step_two(schedule):
    print("Duty Id | Start Time | End time | Start Stop Description | End Stop Description")
    for duty in range(len(schedule.duties)):
        current_duty = schedule.duties[duty]
        first_stop = schedule.get_service_stop(current_duty)
        current_duty['duty_events'].reverse()
        last_stop = schedule.get_service_stop(current_duty)

        last_event_position = len(current_duty['duty_events']) - 1
        first_event = current_duty['duty_events'][0]
        last_event = current_duty['duty_events'][last_event_position]

        print('{} | {} | {} | {} | {}'.format(current_duty['duty_id'], 
                                    schedule.get_time(first_event, 'first', current_duty['duty_id'])[2:], 
                                    schedule.get_time(last_event, 'last', current_duty['duty_id'])[2:], 
                                    first_stop['stop_name'], 
                                    last_stop['stop_name']))

    return

def step_three(schedule):
    print("Duty Id | Start Time | End time | Start Stop Description | End Stop Description | Break Start Time | Break Duration | Break Stop Name")
    for duty in range(len(schedule.duties)):
        current_duty = schedule.duties[duty]
        breaks = [] 

        for duty_event in range(len(current_duty['duty_events']) - 1):
            break_start = schedule.get_time(current_duty['duty_events'][duty_event], 'last', current_duty['duty_id'])
            break_end = schedule.get_time(current_duty['duty_events'][duty_event + 1], 'first', current_duty['duty_id'])
            break_duration = schedule.calculate_break_duration(break_start, break_end)
            if break_duration > 15:
                stop = schedule.get_stop(current_duty['duty_events'][duty_event], 'last', current_duty['duty_id'])
                breaks.append({'start': break_start, 'duration': int(break_duration), 'stop': stop})


        first_stop = schedule.get_service_stop(current_duty)
        current_duty['duty_events'].reverse()
        last_stop = schedule.get_service_stop(current_duty)

        last_event_position = len(current_duty['duty_events']) - 1
        first_event = current_duty['duty_events'][0]
        last_event = current_duty['duty_events'][last_event_position]

        for break_info in breaks:
            print('{} | {} | {} | {} | {} | {} | {} | {}'.format(current_duty['duty_id'], 
                                    schedule.get_time(first_event, 'first', current_duty['duty_id'])[2:], 
                                    schedule.get_time(last_event, 'last', current_duty['duty_id'])[2:], 
                                    first_stop['stop_name'], 
                                    last_stop['stop_name'],
                                    break_info['start'][2:],
                                    break_info['duration'],
                                    break_info['stop']))

    return

if __name__ == "__main__":
    main()

