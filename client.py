import xmlrpc.client

# Create XML-RPC client
server = xmlrpc.client.ServerProxy("http://localhost:8000")

while True:
    
    print("1. Add note")
    print("2. Query Wikipedia")
    print("3. Get notes by topic")
    print("4. Quit")
    choice = input("Enter your choice: ")

    if choice == "1":
        
        topic = input("Enter topic: ")
        text = input("Enter note text: ")
        response = server.process_request(topic, text)
        print(response)
    elif choice == "2":
        
        topic = input("Enter search term: ")
        response = server.query_wikipedia(topic)
        print(response)
    elif choice == "3":
        
        topic = input("Enter topic: ")
        notes = server.get_notes(topic)
        if notes != "No notes found for the given topic.":
            for note in notes:
                print("Text:", note["text"])
                print("Timestamp:", note["timestamp"])
        else:
            print(notes)
    elif choice=="4":
        print("Quit successful")
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
