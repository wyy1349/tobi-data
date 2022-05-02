from textgrid import *

def count_tone_labels(point_list,i):
    """
    @returns a dict with keys as the possible point values, and the values as count of them in that point list
    """
    label_dict = {}
    allowed_labels = set(['H*','!H*','L*','L+H*','L+!H*','L*+H','L*+!H','H+!H*','H-','L-','!H-','L-L%','L-H%','H-H%','H-L%','!H-L%'])
    for point in point_list:
        if point.mark not in allowed_labels:
            print("file "+str(i)+" error "+str(point.time)+' '+point.mark+"\n")
        if point.mark not in label_dict:
            label_dict[point.mark] = 1
        else:
            label_dict[point.mark] += 1
    return label_dict



filenames = ["conv8_EW_apr25.TextGrid","conv2_EW_apr25.TextGrid","conv3_EW_apr25.TextGrid","conv5_EW_apr25.TextGrid"]


for i in range(len(filenames)):
    file = TextGrid.load(filenames[i])
    tones_list = file.tiers[1].make_point_list() #1 is tone tier
    f = open(filenames[i][0:5]+'_data.txt','w')
    f.write(str(count_tone_labels(tones_list,i)))
    f.close()