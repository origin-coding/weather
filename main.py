from utils import process_state, process_city
from network.retrive_data import get_city_id, get_current_air_data, get_history_air_data
from visualize import visualize_current_data, visualize_history_data


def main():
    city_id: str = get_city_id(process_state(input("state:")), process_city(input("city:")))
    if len(city_id) == 0:
        print("City doesn't exist!")
        exit(0)
    print(city_id)
    current_data = get_current_air_data(city_id)
    history_data = get_history_air_data(city_id)
    print(history_data)
    visualize_current_data(current_data)
    visualize_history_data(history_data)


if __name__ == '__main__':
    main()
