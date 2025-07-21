import os
import time
import base64
import argparse
import xml.etree.ElementTree as ET
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

TARGET_TYPE_VALUE = "target_value"  # Change this to your expected <type> content

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

        # Check <type> tag existence and content
        type_elem = root.find(".//type")
        if type_elem is None:
            print(f"[INFO] Skipping file (missing <type>): {file_path}")
            return
        if type_elem.text is None or type_elem.text.strip() != TARGET_TYPE_VALUE:
            print(f"[INFO] Skipping file (<type> != '{TARGET_TYPE_VALUE}'): {file_path}")
            return

        # Check <Body> existence and non-empty
        body_elem = root.find(".//Body")
        if body_elem is None or not body_elem.text or not body_elem.text.strip():
            print(f"[INFO] Skipping file (<Body> missing or empty): {file_path}")
            return

        base64_data = body_elem.text.strip()

        # Create output filename by replacing the .xml extension with .part
        base_filename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(base_filename)[0]
        output_filename = name_without_ext + ".part"
        output_path = os.path.join(self.dest_dir, output_filename)

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
    parser = argparse.ArgumentParser(description="Watch XML files, decode <Body> if <type> matches")
    parser.add_argument("--src", default="/data/input", help="Source directory to monitor for XML files")
    parser.add_argument("--dest", default="/data/input", help="Destination directory to write decoded files")
    args = parser.parse_args()

    start_service(args.src, args.dest)
