import PySimpleGUI as sg

from kad2gp.converter import convert_kad_number


def main():
    sg.theme('DarkAmber')  # Add a touch of color
    # All the stuff inside your window.
    layout = [[sg.Text('Конвертер данных по форме участка из кадастровой карты в файл для Garden Planner.')],
              [sg.Text('Кадастровый номер'), sg.InputText()],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break
        print('You acted ', event, values)

        prms = type('', (), {})()
        prms.kad_number = values[0]
        convert_kad_number(
            kad_number=prms.kad_number,
        )

    window.close()
