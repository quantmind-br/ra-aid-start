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

def _get_user_choice(prompt="Escolha uma opção: ", indent=""):
    """Gets user input, indented consistently with the menu."""
    return input(f"{indent}{prompt}")

def show_main_menu():
    menu_width = 40
    content_width = menu_width - 4
    
    _print_menu_header("MENU PRINCIPAL", menu_width, content_width)
    _print_menu_item("1. Selecionar preset", content_width)
    _print_menu_item("2. Configurar presets", content_width)
    _print_menu_item("3. Sair", content_width)
    _print_menu_footer(menu_width)
    return _get_user_choice()

def show_select_preset_menu():
    presets = load_presets()
    menu_width = 60
    content_width = menu_width - 4

    _print_menu_header("SELECIONAR PRESET", menu_width, content_width)

    if not presets:
        _print_menu_item("Nenhum preset configurado.", content_width)
    else:
        for i, (name, cmd) in enumerate(presets.items(), 1):
            max_name_len = 20
            remaining_space = content_width - len(f"{i}. ") - len(name if len(name) <= max_name_len else name[:max_name_len-3]+"...") - len(": ")
            max_cmd_len = remaining_space - 3 
            
            display_name = name if len(name) <= max_name_len else name[:max_name_len-3] + "..."
            display_cmd = cmd if len(cmd) <= max_cmd_len else cmd[:max_cmd_len-3] + "..."
            
            preset_line = f"{i}. {display_name}: {display_cmd}"
            _print_menu_item(preset_line, content_width)
    
    _print_menu_item("0. Voltar", content_width)
    _print_menu_footer(menu_width)
    choice = _get_user_choice("Escolha o número do preset: ")
    return choice, list(presets.items())

def show_configure_menu():
    menu_width = 40
    content_width = menu_width - 4

    _print_menu_header("CONFIGURAR PRESETS", menu_width, content_width)
    _print_menu_item("1. Adicionar novo preset", content_width)
    _print_menu_item("2. Excluir preset existente", content_width)
    _print_menu_item("3. Voltar", content_width)
    _print_menu_footer(menu_width)
    return _get_user_choice()

def _prompt_enter_to_continue():
    input("\nPressione Enter para continuar...")

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
                    print(f"\n🚀 Executando preset '{name}'...")
                    print(f"   Comando: {command}")
                    os.system(command)
                    print(f"\n✅ Preset '{name}' concluído.")
                else:
                    print("⚠️ Opção inválida.")
            except ValueError:
                print("⚠️ Entrada inválida. Por favor, insira um número.")
            except IndexError: 
                print("⚠️ Opção fora do intervalo.")
            _prompt_enter_to_continue()
            _clear_screen()
            
        elif choice == "2":
            config_choice = show_configure_menu()
            _clear_screen()
            if config_choice == "1":
                print("\n--- Adicionar Novo Preset ---")
                name = input("Nome do preset: ")
                command = input("Comando completo: ")
                if name and command:
                    add_preset(name, command)
                    print(f"\n✅ Preset '{name}' adicionado!")
                else:
                    print("\n⚠️ Nome e comando não podem ser vazios.")
                _prompt_enter_to_continue()
                _clear_screen()
                
            elif config_choice == "2":
                print("\n--- Excluir Preset Existente ---")
                presets = load_presets()
                if not presets:
                    print("Nenhum preset para excluir.")
                else:
                    preset_names = list(presets.keys())
                    for idx, p_name in enumerate(preset_names, 1):
                        print(f"{idx}. {p_name}")
                    print("0. Cancelar")
                    
                    try:
                        delete_idx_str = _get_user_choice("Escolha o número do preset para excluir: ")
                        if delete_idx_str == "0":
                            _clear_screen()
                            continue
                        delete_idx = int(delete_idx_str) -1
                        if 0 <= delete_idx < len(preset_names):
                            target_name = preset_names[delete_idx]
                            confirm = input(f"Tem certeza que deseja excluir o preset '{target_name}'? (s/N): ").strip().lower()
                            if confirm == 's':
                                delete_preset(target_name)
                                print(f"\n❌ Preset '{target_name}' excluído!")
                            else:
                                print("\nExclusão cancelada.")
                        else:
                            print("⚠️ Número inválido.")
                    except ValueError:
                        print("⚠️ Entrada inválida. Por favor, insira um número.")
                _prompt_enter_to_continue()
                _clear_screen()

            elif config_choice == "3":
                _clear_screen()
                continue
            else:
                if config_choice:
                    print("⚠️ Opção de configuração inválida.")
                    _prompt_enter_to_continue()
                _clear_screen()

        elif choice == "3":
            print("\n👋 Saindo... Até logo!")
            break
        else:
            if choice:
                print("⚠️ Opção inválida. Tente novamente.")
                _prompt_enter_to_continue()
            _clear_screen()

if __name__ == '__main__':
    main_menu()