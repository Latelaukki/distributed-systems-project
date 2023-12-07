import tkinter as tk
import requests

game_url    = "http://localhost:7800"
game_port   = "7800"
PLAYER_ID   = "1234"

window = tk.Tk()
window.geometry("500x500")

# Aloitetaan hakemalla pelipalvelimen ip "load balancerilta"
# Palauttaa ip-osoitteen ja portin, josta löytyy pelipalvelin
initial_response = requests.get(game_url)
url = initial_response.text

game_url = 'http://' + url.split(':')[0]
game_port = url.split(':')[1]

print("New game_url:", f"{game_url}:{game_port}")

# Pelin käynnistys

current_maze_display = tk.Text(window, height=5, width=25)

def update_frontend_message(message):
    current_maze_display.delete("1.0", tk.END)
    current_maze_display.insert("1.0", f"{message}")

def get_maze(maze_id):
    try: 
        destination_url = f"{game_url}:{game_port}/get-maze/{maze_id}/{PLAYER_ID}/"
        print(f'Sending request to {destination_url}')
        response = requests.get(destination_url)
        print(f'Response from {destination_url} was {response.json()}')
        update_frontend_message(f"Current maze: {maze_id}")
    except:
        print('Check that the backend is running')

def consume_powerup(power_up):
    try: 
        destination_url = f"{game_url}:{game_port}/consume-powerup/"
        response = requests.post(destination_url, json={"data": power_up})
        update_frontend_message(f"Consumed powerup: {power_up}")
        print(f'Response from {destination_url} was {response.json()}')
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

maze1_button.pack(side=tk.TOP)
maze2_button.pack(side=tk.LEFT)
maze3_button.pack(side=tk.RIGHT)

speed1_button.pack(side=tk.TOP)

current_maze_display.pack()

window.mainloop()