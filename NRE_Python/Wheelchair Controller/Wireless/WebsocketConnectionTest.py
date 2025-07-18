import socket
import time
import keyboard

print("Listening for W/A/S/D. Press ESC to stop.")


arduino_ip = '10.0.0.23'  # Replace with your Arduino's IP
arduino_port = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((arduino_ip, arduino_port))
'''
while True:
    ''''''
    user_input = input("Enter a prompt (type 'exit' to quit): ")
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    '''
user_input = 'S'  # Default value to avoid uninitialized variable warning
while True:
    if keyboard.is_pressed('w'):
        user_input='F'
        print("W key pressed")
    elif keyboard.is_pressed('a'):
        user_input='L'
        print("A key pressed")
    elif keyboard.is_pressed('s'):
        user_input='S'
        print("S key pressed")
    elif keyboard.is_pressed('d'):
        user_input='R'
        print("D key pressed")

    print(f"You entered: {user_input}")
    s.sendall(bytes(user_input, encoding='utf-8'))
    time.sleep(0.5)  # Wait for a short period to ensure the message is sent