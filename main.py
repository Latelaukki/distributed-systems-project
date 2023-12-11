import tkinter as tk
import requests

game_url    = "http://localhost:7800"
game_port   = "7800"

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

def get_maze():
    try:
        maze_button.pack_forget()
        back_button.pack(side=tk.TOP)
        speed_button.pack(side=tk.TOP)
        current_maze_display.pack(side=tk.TOP)

        destination_url = f"{game_url}:{game_port}/get-server"
        print(f'Sending request to {destination_url}')
        response = requests.get(destination_url)
        print(f'Response from {destination_url} was {response.json()}')
        update_frontend_message(f"Entered to the maze")
    except:
        print('Check that the backend is running')

def consume_powerup(power_up):
    try: 
        ask_servers(power_up)
        destination_url = f"{game_url}:{game_port}/consume-powerup/"
        response = requests.post(destination_url, json={"data": power_up})
        update_frontend_message(f"Consumed powerup: {power_up}")
        print(f'Response from {destination_url} was {response.json()}')
    except:
        print('Check that the backend is running')
    
def ask_servers(power_up):
    try: 
        destination_url = f"{game_url}:{game_port}/consensus"
        response = requests.post(destination_url, json={"data" : power_up})
        print(f'Response from {destination_url} was {response.json()}')
    except:
        print('Check that the backend is running')

def show_start_view():
    maze_button.pack(side=tk.TOP)
    back_button.pack_forget()
    current_maze_display.pack_forget()
    speed_button.pack_forget()          

maze_button = tk.Button(
    text="enter maze", command= get_maze
)
back_button = tk.Button(
    text="back", command= show_start_view
)
speed_button = tk.Button(
    text="Speed powerup", command= lambda: consume_powerup("Speed")
)

maze_button.pack(side=tk.TOP)
back_button.pack_forget()
speed_button.pack_forget()

current_maze_display.pack_forget()

window.mainloop()