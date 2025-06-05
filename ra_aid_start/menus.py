from .preset_manager import load_presets, add_preset, delete_preset
import os

def _print_menu_item(text, content_width, indent=""):
    """Helper function to print a menu item within the box, handling padding."""
    print(f"{indent}│ {text:<{content_width}} │")

def _print_menu_header(title, menu_width, content_width, indent=""):
    """Prints the top border and title of a menu."""
    print(f"\n{indent}┌" + "─" * (menu_width - 2) + "┐")
    print(f"{indent}│ {title:^{content_width}} │")
    print(f"{indent}├" + "─" * (menu_width - 2) + "┤")

def _print_menu_footer(menu_width, indent=""):
    """Prints the bottom border of a menu."""
    print(f"{indent}└" + "─" * (menu_width - 2) + "┘")

def _get_user_choice(prompt="Choose an option: ", indent=""):
    """Gets user input, indented consistently with the menu."""
    return input(f"{indent}{prompt}")

def show_main_menu():
    menu_width = 40
    content_width = menu_width - 4
    
    _print_menu_header("MAIN MENU", menu_width, content_width)
    _print_menu_item("1. Select preset", content_width)
    _print_menu_item("2. Configure presets", content_width)
    _print_menu_item("3. Exit", content_width)
    _print_menu_footer(menu_width)
    return _get_user_choice()

def show_select_preset_menu():
    presets = load_presets()
    menu_width = 60
    content_width = menu_width - 4

    _print_menu_header("SELECT PRESET", menu_width, content_width)

    if not presets:
        _print_menu_item("No presets configured.", content_width)
    else:
        for i, (name, cmd) in enumerate(presets.items(), 1):
            max_name_len = 20
            remaining_space = content_width - len(f"{i}. ") - len(name if len(name) <= max_name_len else name[:max_name_len-3]+"...") - len(": ")
            max_cmd_len = remaining_space - 3 
            
            display_name = name if len(name) <= max_name_len else name[:max_name_len-3] + "..."
            display_cmd = cmd if len(cmd) <= max_cmd_len else cmd[:max_cmd_len-3] + "..."
            
            preset_line = f"{i}. {display_name}: {display_cmd}"
            _print_menu_item(preset_line, content_width)
    
    _print_menu_item("0. Back", content_width)
    _print_menu_footer(menu_width)
    choice = _get_user_choice("Choose the preset number: ")
    return choice, list(presets.items())

def show_configure_menu():
    menu_width = 40
    content_width = menu_width - 4

    _print_menu_header("CONFIGURE PRESETS", menu_width, content_width)
    _print_menu_item("1. Add new preset", content_width)
    _print_menu_item("2. Delete existing preset", content_width)
    _print_menu_item("3. Back", content_width)
    _print_menu_footer(menu_width)
    return _get_user_choice()

def _prompt_enter_to_continue():
    input("\nPress Enter to continue...")

def _clear_screen():
    pass

def main_menu():
    _clear_screen()
    while True:
        choice = show_main_menu()
        _clear_screen()
        
        if choice == "1":
            preset_choice, presets_list = show_select_preset_menu()
            if preset_choice == "0":
                _clear_screen()
                continue
            try:
                index = int(preset_choice) - 1
                if 0 <= index < len(presets_list):
                    name, command = presets_list[index]
                    _clear_screen()
                    print(f"\n🚀 Running preset '{name}'...")
                    print(f"   Command: {command}")
                    os.system(command)
                    print(f"\n✅ Preset '{name}' completed.")
                else:
                    print("⚠️ Invalid option.")
            except ValueError:
                print("⚠️ Invalid input. Please enter a number.")
            except IndexError: 
                print("⚠️ Option out of range.")
            _prompt_enter_to_continue()
            _clear_screen()
            
        elif choice == "2":
            config_choice = show_configure_menu()
            _clear_screen()
            if config_choice == "1":
                print("\n--- Add New Preset ---")
                name = input("Preset name: ")
                command = input("Full command: ")
                if name and command:
                    add_preset(name, command)
                    print(f"\n✅ Preset '{name}' added!")
                else:
                    print("\n⚠️ Name and command cannot be empty.")
                _prompt_enter_to_continue()
                _clear_screen()
                
            elif config_choice == "2":
                print("\n--- Delete Existing Preset ---")
                presets = load_presets()
                if not presets:
                    print("No presets to delete.")
                else:
                    preset_names = list(presets.keys())
                    for idx, p_name in enumerate(preset_names, 1):
                        print(f"{idx}. {p_name}")
                    print("0. Cancel")
                    
                    try:
                        delete_idx_str = _get_user_choice("Choose the preset number to delete: ")
                        if delete_idx_str == "0":
                            _clear_screen()
                            continue
                        delete_idx = int(delete_idx_str) -1
                        if 0 <= delete_idx < len(preset_names):
                            target_name = preset_names[delete_idx]
                            confirm = input(f"Are you sure you want to delete preset '{target_name}'? (y/N): ").strip().lower()
                            if confirm == 'y':
                                delete_preset(target_name)
                                print(f"\n❌ Preset '{target_name}' deleted!")
                            else:
                                print("\nDeletion cancelled.")
                        else:
                            print("⚠️ Invalid number.")
                    except ValueError:
                        print("⚠️ Invalid input. Please enter a number.")
                _prompt_enter_to_continue()
                _clear_screen()

            elif config_choice == "3":
                _clear_screen()
                continue
            else:
                if config_choice:
                    print("⚠️ Invalid configuration option.")
                    _prompt_enter_to_continue()
                _clear_screen()

        elif choice == "3":
            print("\n👋 Exiting... Goodbye!")
            break
        else:
            if choice:
                print("⚠️ Invalid option. Try again.")
                _prompt_enter_to_continue()
            _clear_screen()

if __name__ == '__main__':
    main_menu()