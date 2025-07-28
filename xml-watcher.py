import os
import shutil
import time
import itertools
import base64
import argparse
import xml.etree.ElementTree as ET
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

TARGET_TYPE_VALUE = "type_test"  # Change this to your expected <type> content


class XMLHandler(FileSystemEventHandler):
    def __init__(self, src_dir, dest_dir):
        self.src_dir = src_dir
        self.dest_dir = dest_dir

    def on_created(self, event):
        if event.is_directory:
            return

        print(f"[INFO] New Event: {event.src_path}")
        file_path = event.src_path

        handlers = {
            ".txt": self.process_txt,
            ".xml": self.process_xml,
        }

        for ext, handler in handlers.items():
            if file_path.endswith(ext):
                try:
                    print(f"[INFO] New file detected: {file_path}")
                    handler(file_path)
                except Exception as e:
                    print(f"[ERROR] Failed to process {file_path}: {e}")
                break  # Stop after first match

    def process_txt(self, file_path):
        base_filename = os.path.basename(file_path)
        dest_file = os.path.join(self.dest_dir, base_filename)
        print(f"Move {file_path} to {dest_file}")
        shutil.move(file_path, dest_file)

    def process_xml(self, file_path):

        base_filename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(base_filename)[0]
        output_base_filename = name_without_ext + ".part"

        tree = ET.parse(file_path)
        root = tree.getroot()

        for part in root.find("Parts").findall("Part"):
            type = part.find("Type").text
            filename = part.find("Filename").text
            body = part.find("Body").text

            decoded_data = base64.b64decode(body)

            if type in ["text/plain"] or "mytext" in type:
                print(f"[INFO] writing type {type} as text")
                with open(
                    os.path.join(self.dest_dir, output_base_filename + ".txt"), "wb"
                ) as f:
                    output = stripText(
                        decoded_data.decode("utf-8", errors="replace")
                    ).encode("utf-8")
                    f.write(output)
                    print(f"[INFO] Decoded file written to: {os.path.abspath(f.name)}")
            else:
                print(f"[INFO] writing type {type} as binary")
                with open(
                    os.path.join(
                        self.dest_dir, f"{output_base_filename}_{filename}.data"
                    ),
                    "wb",
                ) as f:
                    f.write(decoded_data)
                    print(f"[INFO] Decoded file written to: {os.path.abspath(f.name)}")

        os.remove(file_path)
        print(f"[INFO] Removed processed XML: {file_path}")


def onstart(src_dir, event_handler):
    for filename in os.listdir(src_dir):
        file_path = os.path.join(src_dir, filename)
        if os.path.isfile(file_path) and (
            filename.endswith(".xml") or filename.endswith(".txt")
        ):
            print(f"[INFO] Found existing file at startup: {file_path}")
            try:
                if filename.endswith(".xml"):
                    event_handler.process_xml(file_path)
                elif filename.endswith(".txt"):
                    event_handler.process_txt(file_path)
            except Exception as e:
                print(f"[ERROR] Failed to process {file_path} on startup: {e}")


def stripText(input: str):
    cleaned_lines = list(
        itertools.dropwhile(lambda x: not x.strip(), input.splitlines())
    )
    return "\n".join(cleaned_lines)


def start_service(src_dir, dest_dir):
    print(f"[INFO] Watching for XML files in: {src_dir}")
    print(f"[INFO] Decoded files will be saved to: {dest_dir}")

    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(dest_dir, exist_ok=True)

    event_handler = XMLHandler(src_dir, dest_dir)

    observer = Observer()
    observer.schedule(event_handler, src_dir, recursive=False)
    observer.start()

    onstart(src_dir, event_handler)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[INFO] Stopping service...")
        observer.stop()
    observer.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Watch XML files, decode <Body> if <type> matches"
    )
    parser.add_argument(
        "--src", default="/data/input", help="Source directory to monitor for XML files"
    )
    parser.add_argument(
        "--dest",
        default="/data/input",
        help="Destination directory to write decoded files",
    )
    args = parser.parse_args()

    start_service(args.src, args.dest)
