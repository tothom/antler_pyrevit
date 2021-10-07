import System.Drawing



def lighten_color(color, factor=0.5):
    r, g, b = color.R, color.G, color.B
    return System.Drawing.Color.FromArgb(r, g, b)

def random_color(seed):
    pass
