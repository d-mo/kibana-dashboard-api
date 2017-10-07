
def bottoms(panels):
    """
    Finds bottom lines of all panels
    :param panels:
    :return: sorted by row list of tuples representing lines (col, row , col + len, row)
    """
    bottom_lines = [(p['col'], p['row'] + p['size_y'], p['col'] + p['size_x'], p['row'] + p['size_y']) for p in panels]
    return sorted(bottom_lines, key=lambda l: l[1], reverse=True)


def find_shape(bottom_lines, max_len):
    """
    Finds a shape of lowest horizontal lines with step=1
    :param bottom_lines:
    :param max_len:
    :return: list of levels (row values), list indexes are columns
    """
    shape = [1] * max_len
    for i in range(max_len):
        for line in bottom_lines:
            if line[0] <= i + 1 < line[2]:
                shape[i] = line[1]
                break
    return shape


def longest_lines(shape):
    """
    Creates lines from shape
    :param shape:
    :return: list of dictionaries with col,row,len fields
    """
    lines = []
    for level in set(shape):
        count = 0
        for i in range(len(shape)):
            if shape[i] <= level:
                count += 1
            elif count:
                lines.append({'row': level, 'col': i - count + 1, 'len': count})
                count = 0
        if count:
            lines.append({'row': level, 'col': i - count + 2, 'len': count})

    return sorted(lines, key=lambda l: l['row'])


def find_place(lines, size_x):
    """
    Finds the highest place at the left for a panel with size_x
    :param lines:
    :param size_x:
    :return: line with row, col, len
    """
    for line in lines:
        if line['len'] >= size_x:
            return line


def append_panel(panels, size_x, size_y, max_col=12):
    """
    Appends a panel to the list of panels. Finds the highest palce at the left for the new panel.
    :param panels:
    :param size_x:
    :param size_y:
    :param max_col:
    :return: a new panel or None if it is not possible to place a panel with such size_x
    """
    bottom_lines = bottoms(panels)
    shape = find_shape(bottom_lines, max_col)
    lines = longest_lines(shape)
    line = find_place(lines, size_x)
    if not line:
        return
    panel = {
        'col': line['col'],
        'row': line['row'],
        'size_x': size_x,
        'size_y': size_y,
    }
    panels.append(panel)
    return panel
