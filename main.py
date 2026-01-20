from ui_ux import greeting, menu

def main():
    """ Main function"""
    greeting()

    while True:
        if not menu():
            break


if __name__ == "__main__":
    main()