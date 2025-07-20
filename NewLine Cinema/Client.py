import socket
import json
import tkinter as tk
from tkinter import messagebox, ttk

class CinemaClient:
    def __init__(self, root):
        self.root = root
        root.title("Cinema Ticket System")
        
        # Server connection
        self.server_host = 'localhost'
        self.server_port = 5000
        
        # Create UI
        tk.Label(root, text="Select Movie:").grid(row=0, column=0, padx=10, pady=5)
        self.movie_combobox = ttk.Combobox(root, state="readonly")
        self.movie_combobox.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(root, text="Your Name:").grid(row=1, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(root, text="Number of Tickets:").grid(row=2, column=0, padx=10, pady=5)
        self.tickets_entry = tk.Entry(root)
        self.tickets_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Button(root, text="Buy Tickets", command=self.buy_tickets).grid(row=3, columnspan=2, pady=10)
        tk.Button(root, text="Refresh Movies", command=self.load_movies).grid(row=4, columnspan=2)
        
        self.load_movies()

    def send_request(self, message):
        """Send request to server"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.server_host, self.server_port))
                s.send(message.encode())
                return s.recv(1024).decode()
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {e}")
            return None

    def load_movies(self):
        """Load available movies from server"""
        response = self.send_request("GET_MOVIES")
        if response:
            try:
                movies = json.loads(response)["movies"]
                self.movie_combobox["values"] = [
                    f"{m['id']}: {m['title']} (Room {m['room']}) - ${m['price']}" 
                    for m in movies
                ]
                if movies:
                    self.movie_combobox.current(0)
            except:
                messagebox.showerror("Error", "Could not load movies")

    def buy_tickets(self):
        """Handle ticket purchase"""
        selection = self.movie_combobox.get()
        name = self.name_entry.get().strip()
        tickets = self.tickets_entry.get().strip()
        
        if not all([selection, name, tickets]):
            messagebox.showerror("Error", "Please fill all fields")
            return
            
        try:
            movie_id = int(selection.split(":")[0])
            tickets = int(tickets)
            
            response = self.send_request(f"BOOK:{movie_id}:{tickets}")
            if response:
                if response.startswith("BOOKED:"):
                    messagebox.showinfo("Success", response[7:])
                    self.load_movies()
                else:
                    messagebox.showerror("Error", response[6:])
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

if __name__ == '__main__':
    root = tk.Tk()
    app = CinemaClient(root)
    root.mainloop()