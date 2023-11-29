import tkinter as tk
import requests

GAME_URL    = "http://localhost"
GAME_PORT   = "7800"
PLAYER_ID   = "1234"

window = tk.Tk()
window.geometry("500x500")


current_maze_display = tk.Text(window, height=5, width=25)


def update_current_maze(new_maze):
    current_maze_display.delete("1.0", tk.END)
    current_maze_display.insert("1.0", f"Current maze: {new_maze}")

def get_maze(maze_id):
    try: 
        destination_url = f"{GAME_URL}:{GAME_PORT}/get-maze/{maze_id}/{PLAYER_ID}/"
        print(f'Sending request to {destination_url}')
        response = requests.get(destination_url)
        print(f'Response from {destination_url} was {response.json()}')

        update_current_maze(str(maze_id))

        return response.json
    except:
        print('Check that the backend is running')

def consume_powerup(power_up):
    try: 
        destination_url = f"{GAME_URL}:{GAME_PORT}/consume-powerup/"
        print(f'Sending request to {destination_url}')
        response = requests.post(destination_url, json={"data": power_up})
        print(f'Response from {destination_url} was {response.json()}')
        return response.json
    except:
        print('Check that the backend is running')
    

maze1_button = tk.Button(
    text="enter maze 1", command= lambda: get_maze("1")
)

maze2_button = tk.Button(
    text="enter maze 2", command= lambda: get_maze("2")
)

maze3_button = tk.Button(
    text="enter maze 3", command= lambda: get_maze("3")
)

speed1_button = tk.Button(
    text="Speed powerup", command= lambda: consume_powerup("speed")
)
# speed2_button = tk.Button(
#     text="Speed powerup", command= lambda: get_maze("1")
# )
# speed3_button = tk.Button(
#     text="Speed powerup", command= lambda: get_maze("1")
# )

maze1_button.pack(side=tk.TOP)
maze2_button.pack(side=tk.LEFT)
maze3_button.pack(side=tk.RIGHT)

speed1_button.pack(side=tk.TOP)
# speed2_button.pack(side=tk.LEFT)
# speed3_button.pack(side=tk.RIGHT)

current_maze_display.pack()


window.mainloop()