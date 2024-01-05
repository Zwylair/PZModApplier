import dearpygui.dearpygui as dpg


def open_processing_window():
    dpg.delete_item('done_window')
    with dpg.window(width=350, height=50, tag='done_window',
                    no_title_bar=True, no_resize=True, no_close=True):
        dpg.add_text('Processing', tag='processing_text_item')


def split_string_into_parts(input_string: str, part_limit: int) -> list[str]:
    words = input_string.split()
    parts, current_part = [], []

    for word in words:
        if len(' '.join(current_part + [word])) <= part_limit:
            current_part.append(word)
        else:
            parts.append(' '.join(current_part))
            current_part = [word]

    if current_part:
        parts.append(' '.join(current_part))

    return parts
