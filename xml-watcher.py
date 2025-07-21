import os
import time
import base64
import argparse
import xml.etree.ElementTree as ET
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class XMLHandler(FileSystemEventHandler):
    def __init__(self, src_dir, dest_dir):
        self.src_dir = src_dir
        self.dest_dir = dest_dir

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.xml'):
            try:
                print(f"[INFO] New file detected: {event.src_path}")
                self.process_file(event.src_path)
            except Exception as e:
                print(f"[ERROR] Failed to process {event.src_path}: {e}")

    def process_file(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        filename_elem = root.find(".//Filename")
        body_elem = root.find(".//Body")

        if filename_elem is None or body_elem is None:
            raise ValueError("Missing <Filename> or <Body> in XML")

        filename = filename_elem.text.strip()
        base64_data = body_elem.text.strip()

        output_path = os.path.join(self.dest_dir, filename)
        decoded_data = base64.b64decode(base64_data)

        with open(output_path, 'wb') as out_file:
            out_file.write(decoded_data)
            print(f"[INFO] Decoded file written to: {output_path}")

        os.remove(file_path)
        print(f"[INFO] Removed processed XML: {file_path}")

def start_service(src_dir, dest_dir):
    print(f"[INFO] Watching for XML files in: {src_dir}")
    print(f"[INFO] Decoded files will be saved to: {dest_dir}")

    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(dest_dir, exist_ok=True)

    event_handler = XMLHandler(src_dir, dest_dir)
    observer = Observer()
    observer.schedule(event_handler, src_dir, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[INFO] Stopping service...")
        observer.stop()
    observer.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Watch for XML files, decode <Body> content, write to <Filename>")
    parser.add_argument("--src", default="/data/input", help="Source directory to monitor for XML files")
    parser.add_argument("--dest", default="/data/input", help="Destination directory to write decoded files")
    args = parser.parse_args()

    start_service(args.src, args.dest)
