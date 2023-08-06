def _psgui_parse_file_pattern(pattern):
    pattern_list = pattern.split(';')
    result = []
    for p in pattern_list:
        if p.startswith('*.'):
            result.append(p[1:])
    return result


def _psgui_adjust_save_path(path, pattern):
    suffix_list = _psgui_parse_file_pattern(pattern)
    if len(suffix_list) == 0:
        return path
    for s in suffix_list:
        if path.endswith(s):
            return path
    return path + suffix_list[0]


def psgui_get_file_name_to_open(parent=None,
                                pattern='*.*',
                                width=50,
                                message='Please specify the file to open',
                                title='Open File',
                                verb='Open',
                                old_value=None):
    import PySimpleGUI as sg
    import os
    keep_on_top = True
    if parent:
        keep_on_top = False
        parent.Hide()
    # print(keep_on_top)
    initial_folder = None
    if old_value:
        if old_value.strip() == '':
            initial_folder = os.path.expanduser('~')
        else:
            old_value = os.path.abspath(old_value).replace('\\', '/')
            initial_folder = os.path.dirname(old_value)
    else:
        initial_folder = os.path.expanduser('~')
    filename = ''
    while True:
        event, values = sg.Window(title,
                                  [[sg.Text(message)],
                                   [sg.Input(filename, size=(width, 1), key='-PATH-'),
                                    sg.FileBrowse('Browse', file_types=((pattern, pattern),),
                                                  initial_folder=initial_folder)],
                                   [sg.Open(verb, key='-DOIT-'), sg.Cancel('Cancel', key='-CANCEL-')]],
                                  keep_on_top=keep_on_top).read(close=True)
        # print(event, values)
        filename = None
        if event == '-DOIT-':
            filename = values['-PATH-']
            filename = filename.strip()
            if filename == '':
                sg.popup('File name is empty')
                continue
            else:
                abspath = os.path.abspath(filename).replace('\\', '/')
                if filename != abspath:
                    filename = abspath
                    finished = False
                    continue
                if os.path.isfile(filename):
                    break
                else:
                    sg.popup('File "{}" does not exist'.format(filename))
                    continue
        else:
            break
    if parent:
        parent.UnHide()
    return None if not filename else filename.replace('\\', '/')


def psgui_get_file_name_to_save(parent=None,
                                pattern='*.*',
                                width=50,
                                message='Please specify the save destination file',
                                title='Save as',
                                verb='Save',
                                old_value=None):
    import PySimpleGUI as sg
    import os
    keep_on_top = True
    if parent:
        keep_on_top = False
        parent.Hide()
    # print(keep_on_top)
    initial_folder = None
    if old_value:
        if old_value.strip() == '':
            initial_folder = os.path.expanduser('~')
        else:
            old_value = os.path.abspath(old_value).replace('\\', '/')
            initial_folder = os.path.dirname(old_value)
    else:
        initial_folder = os.path.expanduser('~')
    filename = ''
    while True:
        event, values = sg.Window(title,
                                  [[sg.Text(message)],
                                   [sg.Input(filename, size=(width, 1), key='-PATH-'),
                                    sg.FileSaveAs('Browse', file_types=((pattern, pattern),),
                                                  initial_folder=initial_folder)],
                                   [sg.Open(verb, key='-DOIT-'), sg.Cancel('Cancel', key='-CANCEL-')]],
                                  keep_on_top=keep_on_top).read(close=True)
        # print(event, values)
        filename = None
        if event == '-DOIT-':
            filename = values['-PATH-']
            filename = filename.strip()
            # if os.path.isfile(filename):
            #     break
            # el
            if filename == '':
                sg.popup('File name is empty')
                continue
            else:
                abspath = os.path.abspath(filename).replace('\\', '/')
                abspath = _psgui_adjust_save_path(abspath, pattern)
                if filename != abspath:
                    filename = abspath
                    finished = False
                    continue
                dirname = os.path.dirname(filename)
                # print(dirname)
                if not os.path.exists(dirname):
                    if sg.popup_yes_no('Folder "{}" does not exist. Create it?'.format(dirname)):
                        try:
                            os.makedirs(dirname)
                            break
                        except Exception:
                            sg.popup('Folder "{}" could not be created'.format(dirname))
                            continue
                    else:
                        break
                else:
                    break
        else:
            break
    if parent:
        parent.UnHide()
    return None if not filename else filename.replace('\\', '/')


def psgui_get_folder_name(parent=None,
                          width=50,
                          message='Please specify a folder',
                          title='Folder selection',
                          verb='Select',
                          old_value=None):
    import PySimpleGUI as sg
    import os
    keep_on_top = True
    if parent:
        keep_on_top = False
        parent.Hide()
    # print(keep_on_top)
    initial_folder = None
    if old_value:
        if old_value.strip() == '':
            initial_folder = os.path.expanduser('~')
        else:
            old_value = os.path.abspath(old_value).replace('\\', '/')
            initial_folder = old_value
    else:
        initial_folder = os.path.expanduser('~')
    filename = ''
    while True:
        event, values = sg.Window(title,
                                  [[sg.Text(message)],
                                   [sg.Input(filename, size=(width, 1), key='-PATH-'),
                                    sg.FolderBrowse('Browse', initial_folder=initial_folder)],
                                   [sg.Open(verb, key='-DOIT-'), sg.Cancel('Cancel', key='-CANCEL-')]],
                                  keep_on_top=keep_on_top).read(close=True)
        # print(event, values)
        filename = None
        if event == '-DOIT-':
            filename = values['-PATH-']
            filename = filename.strip()
            if filename == '':
                sg.popup('Folder name is empty')
                continue
            else:
                abspath = os.path.abspath(filename).replace('\\', '/')
                if filename != abspath:
                    filename = abspath
                    finished = False
                    continue
                dirname = filename
                # print(dirname)
                if not os.path.exists(dirname):
                    if sg.popup_yes_no('Folder "{}" does not exist. Create it?'.format(dirname)):
                        try:
                            os.makedirs(dirname)
                            break
                        except Exception:
                            sg.popup('Folder "{}" could not be created'.format(dirname))
                            continue
                    else:
                        break
                else:
                    break
        else:
            break
    if parent:
        parent.UnHide()
    return None if not filename else filename.replace('\\', '/')
