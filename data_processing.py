from dis import dis
from string import digits
from textgrid import *

def count_tone_labels(point_list,filenum):
    """
    prints out a list of illegal labels and files numbers to fix
    @returns a dict with keys as the possible tone labels, and the values as count of them in that point list
    """
    label_dict = {}
    allowed_labels = set(['H*','!H*','L*','L+H*','L+!H*','L*+H','L*+!H','H+!H*','H-','L-','!H-','L-L%','L-H%','H-H%','H-L%','!H-L%'])
    for point in point_list:
        if point.mark not in allowed_labels:
            print("file "+str(filenum)+" error "+str(point.time)+' '+point.mark+"\n")
        if point.mark not in label_dict:
            label_dict[point.mark] = 1
        else:
            label_dict[point.mark] += 1
    return label_dict

def count_break_disf_labels(point_list,filenum):
    """
    prints out a list of illegal labels and files numbers to fix
    @returns a dict with keys as the possible break and disfluency labels, and the values as count of them in that point list
    """
    break_dict = {}
    for point in point_list:
        for i in range(5):
            if str(i) in point.mark:
                if str(i) in break_dict:
                    break_dict[str(i)] += 1
                else:
                    break_dict[str(i)] = 1
    disf_dict = {}
    allowed_disf_labels = set(['ps','psw','e','c','pr','%r','rs','rsw','f','s'])

    for point in point_list:
        disf_labels = re.sub(r'[0-9]+', '', point.mark).split('.')
        if disf_labels == ['']: continue
        for label in disf_labels:
            if label not in allowed_disf_labels:
                print("file "+str(filenum)+" error "+str(point.time)+' '+label+"\n")
            if label not in disf_dict:
                disf_dict[label] = 1
            else:
                disf_dict[label] += 1
    return break_dict, disf_dict

def count_cue_labels(point_list, filenum):
    cue_dict = {}
    allowed_cue_labels = set(['ps','pr','jp'])
    for point in point_list:
        cue_labels = point.mark.split(',')
        for label in cue_labels:
            if label not in allowed_cue_labels and label[0:-1] not in allowed_cue_labels: 
                print("file "+str(filenum)+" error "+str(point.time)+' '+label+"\n")
            if label not in cue_dict:
                if label in allowed_cue_labels:
                    cue_dict[label] = 1 
                else:
                    cue_dict[label[0:-1]] = 0.5 #handles ? as half weight
            else:
                if label in allowed_cue_labels:
                    cue_dict[label] += 1 
                else:
                    cue_dict[label[0:-1]] += 0.5 #handles ? as half weight
    return cue_dict
        

filenames = ["conv8_EW_apr25.TextGrid","conv2_EW_apr25.TextGrid","conv3_EW_apr25.TextGrid","conv5_EW_apr25.TextGrid"]


for i in range(len(filenames)):
    file = TextGrid.load(filenames[i])
    tones_list = file.tiers[1].make_point_list() #1 is tone tier
    breaks_list = file.tiers[2].make_point_list() #2 is break tier
    cues_list = file.tiers[3].make_point_list() #3 is cues tier

    #TODO: make the point lists the same length
    
    f = open(filenames[i][0:5]+'_data.txt','w')

    f.write('tones:\n'+str(count_tone_labels(tones_list,i))+'\n')

    breaks_disfs = count_break_disf_labels(breaks_list,i)
    f.write('breaks:\n'+str(breaks_disfs[0])+'\n')
    f.write('disfs:\n'+str(breaks_disfs[1])+'\n')

    f.write('tones:\n'+str(count_cue_labels(cues_list,i))+'\n')

    f.close()