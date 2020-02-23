import gui


def main():
    width = '390' if platform == 'win32' else '450'
    gui.Gui('Work Time Saver', f'{width}x150').mainloop()


if __name__ == '__main__': main()
