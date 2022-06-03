from PIL import Image
import math

def generate_suffixes(rel_tones, rel_breaks, tones = True, breaks = True, disfs = True, cues = True):
    suffixes = []
    if tones: suffixes.append('_tones')
    if breaks: suffixes.append('_breaks')
    if disfs: suffixes.append('_disfs')
    if cues: suffixes.append('_cues')

    for rel in rel_tones + rel_breaks:
        suffixes.append('_cues_cond_'+rel)
    return suffixes

prefixes = ['conv2', 'conv8', 'conv3', 'conv5']
suffixes = generate_suffixes(['L-L%','L-H%','H-H%','H-L%','!H-L%'], ['0','1','2','3','4'])
width = 640
height = 480

for suffix in suffixes:
    collage = Image.new("RGBA",(width * 2, height * math.ceil(len(prefixes)/2)))
    for i in range(len(prefixes)):
        filepath = './figs/' + prefixes[i] + suffix + '.png'
        collage.paste(Image.open(filepath),((i%2)*640, i//2*480))
    outputfile = './figs/comp' + suffix + '.png'
    collage.save(outputfile)