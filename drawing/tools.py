import cv2

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def color_to_bgr(rgb):
    return (rgb[2], rgb[1], rgb[0])

def draw_line(canvas, start, end, color, size):
    cv2.line(canvas, start, end, color, size)

def draw_circle(canvas, center, radius, color, size):
    cv2.circle(canvas, center, radius, color, size)

def draw_rectangle(canvas, start, end, color, size):
    cv2.rectangle(canvas, start, end, color, size)

def draw_text(canvas, text, position, color, font_scale=1):
    cv2.putText(canvas, text, position, cv2.FONT_HERSHEY_SIMPLEX, 
                font_scale, color, 2, cv2.LINE_AA)