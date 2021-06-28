import plotly
import multiprocessing
from multiprocessing import Process, freeze_support
import plotly.express
import imageio
import time
from Pixel import *
from tkinter import filedialog
import tkinter
import math

color_wheel_dim = (361,256,256)
non_color = -1
non_color_index = 360
step_area = 300
HUE_Threshold = 14 / 255
three_dim_output = (30,30,25)

value_special_color = {
    0:"Red",
    15:"Coral/OrangeRed",
    30:"Brown/Copper",
    45:"Amber",
    60:"Olive/Yellow",
    75:"Lime",
    90:"Chartreuse green",
    105:"Erin/Emerald",
    120:"Green",
    135:"Erin",
    150:"Spring green",
    165:"Jungle green",
    180:"Cyan",
    195:"Cerulean",
    210:"Azure",
    225:"Persian blue",
    240:"Navy blue",
    255:"Ultramarine",
    270:"Violet",
    285:"Lilac",
    300:"Magenta",
    315:"Magenta rose",
    330:"Rose",
    345:"Burgundy",
    }#end of DICT : listed special color in EN

"""
#TODO: 
1.Need parallelism optimization
2.Need SAVE/LOAD function        

"""


def UI_ask_img(var=None):
    file_path = None
    file_path = filedialog.askopenfilename()
    print(file_path)
    var = file_path
    return file_path
    #END of method : ask using UI return file_path

def Button_UI(var=None):
    app = tkinter.Tk()
    labelExample = tkinter.Button(app, text="0")

    buttonExample = tkinter.Button(app, text="Increase", width=30,
                              command=UI_ask_img(var))

    buttonExample.pack()
    labelExample.pack()

    app.mainloop()
    return None
    #END of method : UI with Button for testing

def img_TO_Colorwheel_parallel(img):
    color_wheel_toReturn = numpy.zeros(color_wheel_dim, dtype=numpy.longlong)

    manager = multiprocessing.Manager()
    return_dict = manager.list()
    jobs = []

    start = time.time()

    split_num = math.ceil(img.shape[0]*img.shape[1] / (step_area**2) + 1)
    img_divided = numpy.array_split(img,split_num)
    #print(len(img_divided))

    for i in img_divided:
        p = multiprocessing.Process(target=img_TO_Colorwheel, args=(i, return_dict))
        jobs.append(p)

    #END of FOR : add and begin process

    for p in jobs:
        p.start()


    for proc in jobs:
        proc.join()
    #END of FOR: letting all process ends

    while(return_dict):
        toMerge = return_dict.pop()
        color_wheel_toReturn = merge_Colorwheel(color_wheel_toReturn,toMerge)
    #END of while : merge data from different section of IMG


    end = time.time()

    print("Total TIME:" + str(end - start))
    print("Avg time per step area:" + str((end - start)/split_num))

    return color_wheel_toReturn
#END of method : COLOR WHEEL


def img_TO_Colorwheel(img,toReturn = []):

    color_wheel_toReturn = numpy.zeros(color_wheel_dim, dtype=numpy.uint)

    for i in img:
        for j in i:
            loc = color_wheel_location(j[0], j[1], j[2])
            color_wheel_toReturn[loc] = color_wheel_toReturn[loc] + 1
    # end of nested FOR: increament COUNT in color wheel

    toReturn.append(color_wheel_toReturn)

    return color_wheel_toReturn
    #END of method : parallel calculating color wheel from IMG !!! NO parallelism


def merge_Colorwheel(array1,array2):
    if numpy.array_equal(color_wheel_dim, array1.shape) & numpy.array_equal(color_wheel_dim, array2.shape):
        return numpy.add(array1,array2)
    else:
        print("ERROR: NOT 2 color wheel to be added")
        return
    #end of merger color wheel

def img_TO_Colorwheel_non_parallel(img):

    color_wheel_toReturn = numpy.zeros(color_wheel_dim, dtype=numpy.uint)

    for i in img:
        for j in i:
            loc = color_wheel_location(j[0], j[1], j[2])
            color_wheel_toReturn[loc] = color_wheel_toReturn[loc] + 1
    # end of nested FOR: increament COUNT in color wheel

    return color_wheel_toReturn
    # END of method : parallel calculating color wheel from IMG !!! NO parallelism


class Frame:


    def __init__(self):
        self.full_ColWheel = numpy.zeros(color_wheel_dim,dtype=numpy.uint)
        self.HUE_LIST = []
        self.SAT_LIST = []
        self.LUM_LIST = []

    #END of constructor : take in NO-PARAMETER


    def __init__(self,arr_pixel, merge_mode = False):
        self.full_ColWheel = numpy.zeros(color_wheel_dim)

        if merge_mode:
            print("COLORWHEEL")
            self.full_ColWheel = merge_Colorwheel(self.full_ColWheel,arr_pixel)
            return
        #IF :

        print("NON_ColorWheel")

        if arr_pixel.shape[2] != 3:
            print(arr_pixel.shape)
            return "ERROR : NOT standard RGB IMG"

        for i in arr_pixel:
            for j in i:
                loc = color_wheel_location(j[0], j[1], j[2])
                self.full_ColWheel[loc] = self.full_ColWheel[loc] + 1
        #end of nested FOR: increament COUNT in color wheel
    #end of CONSTRUCTOR : take-in array


    def get_HUE(self):
        HUE_list = numpy.array(self.full_ColWheel.sum(axis=(1,2)))
        return HUE_list
    #END of method get_HUE : return a HUE count list


    def get_HUE_Normalize(self):
        HUE_list = numpy.array(self.full_ColWheel.sum(axis=(1,2)))
        HUE_list = numpy.divide(HUE_list,self.full_ColWheel.sum())
        HUE_list = HUE_list[0:360]
        return HUE_list
    #END of method get_HUE : return a HUE count list


    def get_Lum(self):
        Lum_list = numpy.array(self.full_ColWheel.sum(axis=(0,1)))
        return Lum_list
    #END of method get_HUE : return a HUE count list


    def get_Sat(self):
        Sat_list = numpy.array(self.full_ColWheel.sum(axis=(0,2)))
        return Sat_list
    #END of method get_HUE : return a HUE count list


    def UpdatetToPlot(self):
        self.HUE_LIST = self.get_HUE()
        self.SAT_LIST = self.get_Sat()
        self.LUM_LIST = self.get_Lum()


    def toString(self):
        return "TO DO: FrameAnalyzer.toString()"


    def toString_SAVE(self):
        return "TO DO: FrameAnalyzer.toString_SAVE()"


    def color_ICON(self):
        ICON = []
        for i in range(0,color_wheel_dim[0]-1):
            if i in value_special_color:
                ICON.append(value_special_color[i])
            else:
                ICON.append(str(i))
        #end of FOR create a list of ICON
        return ICON;
    #end of method color_ICON : return a list of color legend


    def toGetThreeDimArray(self):

        count = numpy.zeros(three_dim_output,dtype=numpy.uint)
        hue = numpy.zeros(three_dim_output)
        HSV_Label = numpy.chararray(three_dim_output,itemsize=16)

        toplot = {
            "x": [],
            "y": [],
            "z": [],
            "color": [],
            "size": [],
            "HSV_Label":[]
        }

        for i in range(color_wheel_dim[0]):

            print("1st merge " + str(math.floor(i / color_wheel_dim[0] * 100)) + " %completed")

            for j in range(color_wheel_dim[1]):

                for k in range(color_wheel_dim[2]):

                    curr_coor = calu_color_spaceCoor(i,j,k,three_dim_output[0]/2,three_dim_output[1]/2,three_dim_output[2])

                    hue[(math.floor(curr_coor[0] + three_dim_output[0]/2),math.floor(curr_coor[1] + three_dim_output[1]/2),math.floor(curr_coor[2]))] = curr_coor[3]

                    HSV_Label[(math.floor(curr_coor[0] + three_dim_output[0]/2),math.floor(curr_coor[1] + three_dim_output[1]/2),math.floor(curr_coor[2]))] = "H=" + str(curr_coor[3]) + " S=" + str(curr_coor[4]) + " V=" + str(curr_coor[5])

                    count[(math.floor(curr_coor[0] + three_dim_output[0]/2),math.floor(curr_coor[1] + three_dim_output[1]/2),math.floor(curr_coor[2]))] = self.full_ColWheel[i,j,k] + count[(math.floor(curr_coor[0] + three_dim_output[0]/2),math.floor(curr_coor[1] + three_dim_output[1]/2),math.floor(curr_coor[2]))]

        # end of triple for loop : pre-process data for display

        for i in range(three_dim_output[0]):

            print("2nd merge " + str(math.floor(i / color_wheel_dim[0]*100)) + " %completed")

            for j in range(three_dim_output[1]):

                for k in range(three_dim_output[2]):

                    toplot["x"].append(math.floor(i - three_dim_output[0]/2))
                    toplot["y"].append(math.floor(j - three_dim_output[1]/2))
                    toplot["z"].append(k)
                    toplot["color"].append(hue[i,j,k])
                    toplot["size"].append(count[i,j,k])
                    toplot["HSV_Label"].append(str(HSV_Label[i,j,k])[1:])
                    #print("i " + str(i) + "j " + str(j) + "k " + str(k) + str(count[i,j,k]))

        return toplot
    #end of method to Get the DICT for creating a 3D


    def toDraw_3D(self,toplot,str_title = "色域空間"):

        print("DRAWING Matrix")

        fig = plotly.express.scatter_3d(toplot, x='x', y='y', z='z', size='size', color='color',

                                        color_continuous_scale=plotly.colors.cyclical.HSV,

                                        labels={"color":"色相HUEの値"},

                                        hover_data = {"x":False,
                                                      "y":False,
                                                      "z":False,
                                                      "color":False,
                                                      "HSV_Label":True
                                                      }
                                        )

        # fig.update_layout(scene_zaxis_type="log")

        fig.update_layout(title=str_title,
                          scene=dict(xaxis=dict(title='⇕彩度：中心点(0,0,0)からの水平距離\n近い：薄い❘遠い：濃い', titlefont_color='black'),
                                     yaxis=dict(title='↺色相：中心点への直線とX軸(Y=0,X>0)の角度\n右：赤❘上：緑❘左：青❘下：紫', titlefont_color='black'),
                                     zaxis=dict(title='⤆明度：中心点(0,0,0)からの垂直距離\n上：明るい❘下：暗い', titlefont_color='black'),
                                     bgcolor='rgb(255, 255, 255)',
                                     ))

        #This section setting the visual of the graph

        fig.show()

        return None
    #end of method : Draw para:toplot


    def toDraw_HUE(self):
        self.UpdatetToPlot()
        toPlot = dict(r=self.get_HUE_Normalize(),theta=self.color_ICON(),
                                      strength = numpy.arange(self.full_ColWheel.shape[0]-1),
                                       )

        print(len(toPlot["r"]), len(toPlot["theta"]), len(toPlot["strength"]))
        fig = plotly.express.line_polar(toPlot, r='r', theta='theta',
                                        color="strength",
                                        template="plotly_dark",
                                        line_close=True,
                                        )

        fig.show()
    #end of method : Draw Hue out
#
# def run():
#     freeze_support()
#     file_name = UI_ask_img()
#     img = imageio.imread(file_name)
#     var = img_TO_Colorwheel_parallel(img)
#     var = Frame(var, True)
#     print("Calculation Completed")
#     var.toDraw_3D(var.toGetThreeDimArray(), str(file_name + "の色域空間"))
#     input()
#     exit(0)


if __name__ == '__main__':
    freeze_support()
    file_name = None
    file_name = UI_ask_img()
    #file_name = Button_UI(file_name)
    img = imageio.imread(file_name)
    var = img_TO_Colorwheel_parallel(img)
    var = Frame(var,True)
    print("Calculation Completed, now merging data.")
    var.toDraw_3D(var.toGetThreeDimArray(), str(file_name + "の色域空間"))

    input()
