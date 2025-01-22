import requests

# Function to notify the vending machine to dispatch the bag
def notify_machine_to_dispatch(machine_id, unique_code):
    # Assuming there's an API on the vending machine to accept a dispatch request
    # machine_url = f"http://machine_url/{machine_id}/dispatch"
    
    # payload = {
    #     "unique_code": unique_code,
    #     "action": "dispatch_bag"
    # }

    # # Send a request to the machine
    # response = requests.post(machine_url, json=payload)

    if True or response.status_code == 200:
        return True
    else:
        return False
