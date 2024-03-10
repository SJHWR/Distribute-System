import xml.etree.ElementTree as ET
import datetime
import requests
from xmlrpc.server import SimpleXMLRPCServer

# XML database file name
XML_DB_FILE = "cc.xml"

# Handle client requests, check if the topic exists, and if not, create a new topic
def process_request(topic, text):
    
    tree = ET.parse(XML_DB_FILE)
    root = tree.getroot()

    
    topic_found = False
    for topic_elem in root.findall('topic'):
        if topic_elem.attrib['name'] == topic:
            
            topic_found = True
            note_elem = ET.SubElement(topic_elem, 'note', name="Note {}".format(len(topic_elem.findall('note')) + 1))
            text_elem = ET.SubElement(note_elem, 'text')
            text_elem.text = text
            timestamp_elem = ET.SubElement(note_elem, 'timestamp')
            timestamp_elem.text = str(datetime.datetime.now())
            break

    
    if not topic_found:
        topic_elem = ET.SubElement(root, 'topic', name=topic)
        note_elem = ET.SubElement(topic_elem, 'note', name="Note 1")
        text_elem = ET.SubElement(note_elem, 'text')
        text_elem.text = text
        timestamp_elem = ET.SubElement(note_elem, 'timestamp')
        timestamp_elem.text = str(datetime.datetime.now())

    
    tree.write(XML_DB_FILE)

    
    return "Note added successfully."

# Query the Wikipedia API and return relevant information
def query_wikipedia(topic):
    
    response = requests.get("https://en.wikipedia.org/w/api.php",
                            params={"action": "opensearch", "search": topic, "format": "json"})
    data = response.json()

    
    if len(data) >= 2 and len(data[1]) >= 1:
        return data[3][0]  
    else:
        return "No relevant information found on Wikipedia."

# Get notes on a specific topic
def get_notes(topic):
    
    tree = ET.parse(XML_DB_FILE)
    root = tree.getroot()

    
    notes = []
    for topic_elem in root.findall('topic'):
        if topic_elem.attrib['name'] == topic:
            for note_elem in topic_elem.findall('note'):
                note_text = note_elem.find('text').text
                timestamp = note_elem.find('timestamp').text
                notes.append({"text": note_text, "timestamp": timestamp})
            break

    if notes:
        return notes
    else:
        return "No notes found for the given topic."


server = SimpleXMLRPCServer(("localhost", 8000))
print("Server is running on port 8000...")

# Register a function to handle requests
server.register_function(process_request, "process_request")
server.register_function(query_wikipedia, "query_wikipedia")
server.register_function(get_notes, "get_notes")

# run
server.serve_forever()
