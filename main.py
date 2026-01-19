from ui_ux import greeting, menu

def main():
    """ Main function"""
    greeting()

    while True:
        runagain = menu()
        if not runagain:
            break


if __name__ == "__main__":
    main()