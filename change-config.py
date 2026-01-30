import os
import base64
import json

def add_field_to_file(file_path, field_name, field_value, config_key_value):
    # Read file content
    with open(file_path, 'r') as file:
        encoded_data = file.read()

        # Decode base64
        try:
            decoded_data = base64.b64decode(encoded_data)
            json_data = json.loads(decoded_data)
        except Exception as e:
            print(f"Cannot decode file {os.path.basename(file_path)}: {e}")
            return
        
        # Check if configKey matches the provided value
        if json_data.get('configKey') == config_key_value:
            print(f"Adding field '{field_name}' with value '{field_value}' to file {os.path.basename(file_path)}...")
            json_data[field_name] = field_value

            # Encode again and save to file
            updated_json_str = json.dumps(json_data, separators=(',', ':'))
            updated_encoded_data = base64.b64encode(updated_json_str.encode()).decode()

            with open(file_path, 'w') as file:
                file.write(updated_encoded_data)
            print(f"File {os.path.basename(file_path)} has been updated.")

def delete_field_from_file(file_path, field_name, config_key_value):
    # Read file content
    with open(file_path, 'r') as file:
        encoded_data = file.read()

        # Decode base64
        try:
            decoded_data = base64.b64decode(encoded_data)
            json_data = json.loads(decoded_data)
        except Exception as e:
            print(f"Cannot decode file {os.path.basename(file_path)}: {e}")
            return
        
        # Check if configKey matches the provided value
        if json_data.get('configKey') == config_key_value:
            if field_name in json_data:
                del json_data[field_name]

                # Encode again and save to file
                updated_json_str = json.dumps(json_data, separators=(',', ':'))
                updated_encoded_data = base64.b64encode(updated_json_str.encode()).decode()

                with open(file_path, 'w') as file:
                    file.write(updated_encoded_data)
                print(f"File {os.path.basename(file_path)} has been updated.")

def process_files(folder_path, field_name, field_value, action, config_key_value):
    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            
            if action == "add":
                add_field_to_file(file_path, field_name, field_value, config_key_value)
            elif action == "delete":
                delete_field_from_file(file_path, field_name, config_key_value)
            elif action == "edit":
                # Read and edit field as per old logic if it's "edit"
                with open(file_path, 'r') as file:
                    encoded_data = file.read()

                    # Decode base64
                    try:
                        decoded_data = base64.b64decode(encoded_data)
                        json_data = json.loads(decoded_data)
                    except Exception as e:
                        print(f"Cannot decode file {file_path}: {e}")
                        continue
                    
                    print("Check file:", os.path.basename(file_path))

                    # Check and change field value if needed
                    if field_name in json_data and 'configKey' in json_data and json_data['configKey'] == config_key_value:
                    # if field_name in json_data and json_data['configKey'] == config_key_value:
                        json_data[field_name] = field_value

                        # Encode again and save to file
                        updated_json_str = json.dumps(json_data, separators=(',', ':'))
                        updated_encoded_data = base64.b64encode(updated_json_str.encode()).decode()

                        with open(file_path, 'w') as file:
                            file.write(updated_encoded_data)
                        print(f"File {os.path.basename(file_path)} has been updated.")

def main():

    folder_path = input("Enter the config folder: ").strip()

    if len(folder_path) == 0:
        folder_path = '/Users/now/Desktop/configs/all-in-one-363'

    print(f"Config folder: {folder_path}")

    if not os.path.isdir(folder_path):
        print(f"The path '{folder_path}' is not valid!")
        return

    key_options = {
        "S": "S_GAME_CONFIG",
        "X": "X_GAME_CONFIG",
        "M": "MAN_GAME_CONFIG",
        "G": "GEM_CONFIG"
    }

    key_choice = input("Enter brand (S/X/M/G): ").strip().upper()

    if key_choice not in key_options:
        print("Invalid choice for brand!")
        return

    config_key_value = key_options[key_choice]

    print(f"Selected config key: {config_key_value}")
        
    action = input("Choose action (add/edit/delete): ").strip().lower()
    if action not in ["add", "edit", "delete"]:
        print("Invalid action!")
        return

    field_name = input("Enter the field name to modify: ").strip()
    field_value = input("Enter the value of the field: ").strip()

    process_files(folder_path, field_name, field_value, action, config_key_value)


if __name__ == "__main__":
    main()
