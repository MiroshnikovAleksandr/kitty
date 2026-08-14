from kitty.tab_bar import as_rgb, draw_title
from kitty.utils import color_as_int


def draw_tab(draw_data, screen, tab, before, max_tab_length, index, is_last, extra_data):
    if extra_data.next_tab is not None:
        next_bg = draw_data.tab_bg(extra_data.next_tab)
    else:
        next_bg = color_as_int(draw_data.default_bg)
    next_bg_hex = format(next_bg & 0xFFFFFF, '06x')

    new_title_template = draw_data.title_template.replace('_ffffff', f'_{next_bg_hex}')
    new_active_title_template = None
    if draw_data.active_title_template is not None:
        new_active_title_template = draw_data.active_title_template.replace('_ffffff', f'_{next_bg_hex}')
    draw_data = draw_data._replace(
        title_template=new_title_template,
        active_title_template=new_active_title_template,
    )

    if draw_data.leading_spaces:
        screen.draw(' ' * draw_data.leading_spaces)
    draw_title(draw_data, screen, tab, index, max_tab_length)
    trailing_spaces = min(max_tab_length - 1, draw_data.trailing_spaces)
    max_tab_length -= trailing_spaces
    extra = screen.cursor.x - before - max_tab_length
    if extra > 0:
        screen.cursor.x -= extra + 1
        screen.draw('…')
    if trailing_spaces:
        screen.draw(' ' * trailing_spaces)
    end = screen.cursor.x
    screen.cursor.bold = screen.cursor.italic = False
    screen.cursor.fg = 0
    if not is_last:
        screen.cursor.bg = as_rgb(color_as_int(draw_data.inactive_bg))
        screen.draw(draw_data.sep)
    screen.cursor.bg = 0
    return end
