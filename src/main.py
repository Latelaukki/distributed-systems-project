import tkinter as tk
import requests

url = "http://localhost:"
window = tk.Tk()
window.geometry("500x500")

def get_maze(server_port):
    try: 
        destination_url = f"{url}{server_port}/get-maze"
        print(f'Sending request to {destination_url}')
        response = requests.get(destination_url)
        print(f'Response from {destination_url} was {response.json()}')
        return response.json
    except:
        print('Check that the backend is running')

maze1_button = tk.Button(
    text="enter maze 1", command= lambda: get_maze(81)
)

maze2_button = tk.Button(
    text="enter maze 2", command= lambda: get_maze(82)
)

maze3_button = tk.Button(
    text="enter maze 3", command= lambda: get_maze(83)
)

maze1_button.pack(side=tk.TOP)
maze2_button.pack(side=tk.LEFT)
maze3_button.pack(side=tk.RIGHT)

window.mainloop()