import numpy
import cv2
import math

RGB_limit = 255;
Lum_limit = 255;
Hue_limit = 359;
Sat_limit = 255;
HUE_Threshold = 14; # put -1 to disable this feature
Sat_XYZ_Threshold = 5 / Sat_limit
no_Color = 0


#Section class variables

def sat_Calu(R, G, B):
    r = R / RGB_limit;
    g = G / RGB_limit;
    b = B / RGB_limit;
    rgb_max = max(r, g, b)
    rgb_min = min(r, g, b)
    max_index = numpy.argmax([r, g, b])

    if (rgb_max == rgb_min):
        return (float)(0.0);
    # end of if : return 0 if is shade of GREY

    L = min(r, g, b) + max(r, g, b)
    L /= 2

    if (L <= 0.5):
        return int(((rgb_max - rgb_min) / (rgb_max + rgb_min) + 0.0) * Lum_limit)
    else:
        return int(((rgb_max - rgb_min) / (2.0 - rgb_max - rgb_min) + 0.0) * Lum_limit);


# end of function pixel_handler : return hue info

def color_wheel_location(r, g, b):
    return (int(hue_Calu(r, g, b)),int(sat_Calu(r, g, b)),int(lumiance_Calu(r,g,b)))



def hue_Calu(R, G, B):
    r = R / RGB_limit;
    g = G / RGB_limit;
    b = B / RGB_limit;

    rgb_max = max(r, g, b)
    rgb_min = min(r, g, b)
    max_index = numpy.argmax([r, g, b])

    if rgb_max - rgb_min <= HUE_Threshold / RGB_limit:
        return no_Color;

    if max_index == 0:
        return int(((g - b) / (rgb_max - rgb_min) * 60) % Hue_limit)
    elif max_index == 1:
        return int((((b - r) / (rgb_max - rgb_min) + 2.0) * 60 % Hue_limit))
    elif max_index == 2:
        return int((((r - g) / (rgb_max - rgb_min) + 4.0) * 60 % Hue_limit))
    else:
        return "ERROR"


# end of function pixel_handler : return hue info

def lumiance_Calu(R, G, B):
    r = R / RGB_limit;
    g = G / RGB_limit;
    b = B / RGB_limit;
    rgb_max = max(r, g, b)
    rgb_min = min(r, g, b)
    max_index = numpy.argmax([r, g, b])

    L = min(r, g, b) + max(r, g, b)
    L /= 2

    return (int)((L + 0.0) * Lum_limit)

def calu_color_spaceCoor(H,S,V,max_x,max_y,max_z):
    max_dis = min(max_x,max_y)

    xy_dis = S / Sat_limit

    if xy_dis<Sat_XYZ_Threshold:
        xy_dis = 0
    else:
        xy_dis = max_dis * xy_dis

    x_coor = min(xy_dis,max_x - 1) * math.sin(math.radians(H))
    y_coor = min(xy_dis,max_y - 1) * math.cos(math.radians(H))

    z_coor = min(V / Lum_limit * max_z,max_z-1)

    return [math.floor(x_coor),math.floor(y_coor),math.floor(z_coor),H,S,V]

class Pixel:

    def __init__(self, R, G, B,HSV = False):
        if HSV == False:
            self.r = R
            self.g = G
            self.b = B
            self.hue = hue_Calu(R, G, B)
            self.saturation = sat_Calu(R, G, B)
            self.lumiance = lumiance_Calu(R, G, B)
        else:
            self.hue = R
            self.saturation = G
            self.lumiance = B

    # end of function pixel handler : return L as Lumince

    def toString(self):
        print("R:" + str(self.r) + " G:" + str(self.g) + " B:" + str(self.b)
              + " HUE " + str(self.hue) + " Lum " + str(self.lumiance) + " Sat " + str(self.saturation)
              )

    def get_HSV_Colorwheel_Location (self):
        return [hue_Calu(self.r,self.g,self.b),sat_Calu(self.r,self.g,self.b),lumiance_Calu(self.r,self.g,self.b)]


if __name__ == '__main__':

    print(color_wheel_location(20, 10, 30))
    print(color_wheel_location(20, 10, 200))