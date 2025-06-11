def traffic_signal_control():
    while True:
        # Get the number of vehicles on each side
        vehicles_A = int(input("Enter the number of vehicles on side A: "))
        vehicles_B = int(input("Enter the number of vehicles on side B: "))

        # Determine the traffic signal state
        if vehicles_A == 0:
            print("Side B has green signal.")
        elif vehicles_B == 0:
            print("Side A has green signal.")
        elif vehicles_B > vehicles_A:
            print("Side B has green signal.")
        else:
            print("Side A has green signal.")

        # You can add a delay here to simulate the signal duration
        # For example:
        # import time
        # time.sleep(10)  # Wait for 10 seconds

if __name__ == "__main__":
    traffic_signal_control()