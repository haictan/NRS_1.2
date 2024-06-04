#input nm
#output float 0-1
def wavelength_to_rgb(wavelength, gamma=0.8):
  
    wavelength = float(wavelength)
    if wavelength < 380 or wavelength > 750:
        return (0, 0, 0)  # Black, as it is outside the visible spectrum
    
    if wavelength < 440:
        red = -(wavelength - 440) / (440 - 380)
        green = 0.0
        blue = 1.0
    elif wavelength < 490:
        red = 0.0
        green = (wavelength - 440) / (490 - 440)
        blue = 1.0
    elif wavelength < 510:
        red = 0.0
        green = 1.0
        blue = -(wavelength - 510) / (510 - 490)
    elif wavelength < 580:
        red = (wavelength - 510) / (580 - 510)
        green = 1.0
        blue = 0.0
    elif wavelength < 645:
        red = 1.0
        green = -(wavelength - 645) / (645 - 580)
        blue = 0.0
    else:
        red = 1.0
        green = 0.0
        blue = 0.0

    # Let the intensity fall off near the vision limits
    if wavelength > 700:
        red *= 0.3 + 0.7 * (750 - wavelength) / (750 - 700)
    elif wavelength < 420:
        red *= 0.3 + 0.7 * (wavelength - 380) / (420 - 380)
        blue *= 0.3 + 0.7 * (wavelength - 380) / (420 - 380)

    return (int(red**gamma * 255), int(green**gamma * 255), int(blue**gamma * 255))
    #return (red**gamma, green**gamma, blue**gamma)

# Example: Convert 500 nm to RGB
#rgb_color = wavelength_to_rgb(550)
#print(rgb_color)
