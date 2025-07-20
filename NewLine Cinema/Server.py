import socket
import threading
import json

class CinemaServer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.movies = [
            {"id": 1, "title": "The Avengers", "room": 1, "tickets": 100, "price": 12.50},
            {"id": 2, "title": "Inception", "room": 2, "tickets": 80, "price": 10.00},
            {"id": 3, "title": "Jurassic Park", "room": 3, "tickets": 120, "price": 9.50},
            {"id": 4, "title": "The Dark Knight", "room": 1, "tickets": 90, "price": 11.00},
            {"id": 5, "title": "Interstellar", "room": 2, "tickets": 70, "price": 10.50}
        ]

    def handle_client(self, client_socket):
        """Handle client connections"""
        try:
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                    
                if data == "GET_MOVIES":
                    response = json.dumps({"movies": self.movies})
                    client_socket.send(response.encode())
                elif data.startswith("BOOK:"):
                    parts = data.split(":")
                    movie_id = int(parts[1])
                    tickets = int(parts[2])
                    
                    for movie in self.movies:
                        if movie["id"] == movie_id:
                            if movie["tickets"] >= tickets:
                                movie["tickets"] -= tickets
                                total = tickets * movie["price"]
                                response = f"BOOKED:{tickets} tickets for {movie['title']}. Total: ${total:.2f}"
                            else:
                                response = "ERROR:Not enough tickets available"
                            break
                    else:
                        response = "ERROR:Movie not found"
                        
                    client_socket.send(response.encode())
                    
        except Exception as e:
            print(f"Client error: {e}")
        finally:
            client_socket.close()

    def start(self):
        """Start the server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            print(f"Server running on {self.host}:{self.port}")
            print("Available movies:")
            for movie in self.movies:
                print(f"{movie['id']}: {movie['title']} (Room {movie['room']}) - ${movie['price']} - Tickets: {movie['tickets']}")

            while True:
                client_socket, addr = self.server_socket.accept()
                print(f"Connection from {addr}")
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket,)
                )
                client_thread.start()

        except KeyboardInterrupt:
            print("\nShutting down server...")
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()

if __name__ == '__main__':
    server = CinemaServer()
    server.start()