from dis import dis
from string import digits
from textgrid import *

EPSILON = 0.1 #error tolerance in time (s) for when two labels should be aligned but did not use auto-align

boundary_tones = set(['L-L%','L-H%','H-H%','H-L%','!H-L%'])
all_breaks = set(['0','1','2','3','4'])
relevant_cues = set(['ps','pr','jp'])

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

def count_cues_for_breaks(cues_tier, breaks_tier, cues=relevant_cues, breaks=all_breaks):
    breaks_cues_dict = {}

    #make a dict with keys as breaks, values as new dicts for which keys are cues, values are counts of the cues just before that break
    for break_num in breaks: 
        breaks_cues_dict[break_num] = {}
        for cue in cues:
            breaks_cues_dict[break_num][cue] = 0

    for break_point in breaks_tier: 
        #don't care about breaks that don't have a number, like %r
        break_num = break_point.mark
        if break_num == '' or break_num[0] not in breaks:
            continue
        for cue_point in cues_tier:
            cue_group = cue_point.mark
            #don't care about cues far away from the break we're looking at
            if not (break_point.time - EPSILON <= cue_point.time <= break_point.time + EPSILON):
                continue
            indiv_cues = cue_group.split(",")
            for indiv_cue in indiv_cues:
                if indiv_cue in cues:
                    breaks_cues_dict[break_num[0]][indiv_cue] += 1
                elif indiv_cue[0:-1] in cues and indiv_cue[-1] == '?':
                    breaks_cues_dict[break_num[0]][indiv_cue[0:-1]] += 0.5
    
    return breaks_cues_dict


def count_cues_for_tones(cues_tier, tones_tier, cues=relevant_cues, tones=boundary_tones): 
    tones_cues_dict = {}

    #make a dict with keys as the relevant tones, values as new dicts for which keys are cues, values are counts of the cues just before that break
    for tone in tones: 
        tones_cues_dict[tone] = {}
        for cue in cues:
            tones_cues_dict[tone][cue] = 0

    for tone_point in tones_tier: 
        tone = tone_point.mark
        #don't care about tones that are not relevant
        if tone not in tones:
            continue
        for cue_point in cues_tier:
            cue_group = cue_point.mark
            #don't care about cues far away from the break we're looking at
            if not (tone_point.time - EPSILON <= cue_point.time <= tone_point.time + EPSILON):
                continue
            indiv_cues = cue_group.split(",")
            for indiv_cue in indiv_cues:
                if indiv_cue in cues:
                    tones_cues_dict[tone][indiv_cue] += 1
                elif indiv_cue[0:-1] in cues and indiv_cue[-1] == '?':
                    tones_cues_dict[tone][indiv_cue[0:-1]] += 0.5
    
    return tones_cues_dict

filenames = ["conv8_EW_apr25.TextGrid","conv2_EW_apr25.TextGrid","conv3_EW_apr25.TextGrid","conv5_EW_apr25.TextGrid"]


for i in range(len(filenames)):
    file = TextGrid.load(filenames[i])
    tones_list = file.tiers[1].make_point_list() #1 is tone tier
    breaks_list = file.tiers[2].make_point_list() #2 is break tier
    cues_list = file.tiers[3].make_point_list() #3 is cues tier

    #make the point lists the same length
    uniform_len = min(tones_list[-1].time, breaks_list[-1].time, cues_list[-1].time)
    all_lists = [tones_list,breaks_list,cues_list]
    for lst in all_lists:
        for point in lst:
            if point.time > uniform_len:
                lst.remove(point)
    
    f = open(filenames[i][0:5]+'_data.txt','w')

    f.write('tones:\n'+str(count_tone_labels(tones_list,i))+'\n')

    breaks_disfs = count_break_disf_labels(breaks_list,i)
    f.write('breaks:\n'+str(breaks_disfs[0])+'\n')
    f.write('disfs:\n'+str(breaks_disfs[1])+'\n')

    f.write('cues:\n'+str(count_cue_labels(cues_list,i))+'\n')

    f.write('cues for each type of break:\n'+str(count_cues_for_breaks(cues_list,breaks_list))+'\n')

    f.write('cues for each type of boundary tones:\n'+str(count_cues_for_tones(cues_list,tones_list))+'\n')

    f.close()