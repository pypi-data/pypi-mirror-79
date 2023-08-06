def clean_data(in_data, is_dict=False):
    if isinstance(in_data, (list, tuple)):
        out_data = []
        for data in in_data:
            out_data.append(convert_string(data))
        if not is_dict:
            out_data = tuple(out_data)
    else:
        out_data = convert_string(in_data)
        if is_dict:
            temp_data = list()
            temp_data.append(out_data)
            out_data = temp_data
    return out_data


def convert_string(data):
    if is_number(data):
        if "." in data:
            data = float(data)
        else:
            data = int(data)
    if data == 'True' or data == 'on':
        data = True
    if data == 'False':
        data = False
    return data


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_boolean(s):
    if str(s).lower() in ['true', 'false']:
        return True
    else:
        return False


def is_checkbox(s):
    if str(s).lower() in ['__checkbox_end__', '__checkbox_begin__']:
        return True
    else:
        return False


def get_dataframe_name(s):
    # Return list with variable_name, and dataframe_name if the type is dataframe.
    if s[-2:] == "__":
        s = s[:-2]
        dataframe_name = s.split("___")[-1]
        variable_name = s.split("___")[0]
        return variable_name, dataframe_name
    else:
        return False


def remove_item_tuple(data, index):
    list_data = list(data)
    del list_data[index]
    new_tuple = tuple(list_data)
    return new_tuple


def update_item_tuple(data, index, value):
    list_data = list(data)
    list_data[index] = value
    new_tuple = tuple(list_data)
    return new_tuple
