# genbearpages.py
#
# Generate pages for A Bear's Journey from template

import sys
import pdb
import os
import subprocess

instagramfile = r"C:\git\github\sumitsumit.github.io\abearsjourney\assets\instagramlist.txt"
bearstoryfile = r"C:\git\github\sumitsumit.github.io\abearsjourney\assets\bearstory.txt"
templatefile = r"C:\git\github\sumitsumit.github.io\abearsjourney\assets\index_template.html"
outdir = r"C:\git\github\sumitsumit.github.io\abearsjourney"
imgpath = "images/story"


def readlines(filename):
    fp = open(filename)
    lines = []
    while True:
        line = fp.readline()
        if line == "":
            break
        lines.append(line.strip())
    return lines

def replacetext(txt, replacedict):
    for key in replacedict:
        txt = txt.replace(key, replacedict[key])
    return txt

def urlfrompagenum(pagenum):
    if pagenum == 0:
        url = "index.html"
    else:
        url = "index"+str(pagenum)+".html"
    return url

def frame_html(frame_tuple):
    """Takes frame_tuple = (num_str, caption, img_url) and creates HTML for that frame."""
    # see css/main.css for img.bearframe and div.bearcaption CSS
    html_str = '<div class="bearcontainer">'
    html_str += f'<img class="bearframe" src="{frame_tuple[2]}" />'
    html_str += f'<br /><div class="bearcaption">{frame_tuple[1]}</div>'
    html_str += '</div>'
    return html_str

def main(argv):
    previewmode = False
    if '-preview' in argv:
        print("WARNING: Preview Mode")
        previewmode = True
    numbearsperpage = 3
    
    fp = open(bearstoryfile, 'r', encoding='iso-8859-1')
    frame_tuples = []
    for line in fp.readlines():
        num_str = line.split(',')[0]
        caption = ','.join(line.split(',')[1:])
        img_path = imgpath+'/'+num_str+'.jpg'
        if os.path.exists(os.path.join(outdir,img_path)):
            frame_tuples.append( (num_str, caption, img_path) )
    fp.close()

    num_frames = len(frame_tuples)
    print(f"Found {num_frames} frames")
    templatetext = "\n".join(readlines(templatefile))
    numpages = int(num_frames/numbearsperpage)
    if num_frames % numbearsperpage != 0:
        numpages += 1
    print(f"Generating {numpages} pages")
    
    for pagenum in range(numpages):
        # set up replacedict
        replacedict = {}
        replacedict['$bear0'] = frame_html(frame_tuples[pagenum*3 + 0])
        if pagenum*3 + 1 < num_frames:
            replacedict['$bear1'] = frame_html(frame_tuples[pagenum*3 + 1])
        else:
            replacedict['$bear1'] = ''
        if pagenum*3 + 2 < num_frames:
            replacedict['$bear2'] = frame_html(frame_tuples[pagenum*3 + 2])
        else:
            replacedict['$bear2'] = ''
        if pagenum > 0:
            replacedict['$prevpageurl'] = urlfrompagenum(pagenum-1)
        else:
            replacedict['$prevpageurl'] = '#'
        if pagenum < numpages-1:
            replacedict['$nextpageurl'] = urlfrompagenum(pagenum+1)
        else:
            replacedict['$nextpageurl'] = '#'
        replacedict['$lastpageurl'] = urlfrompagenum(numpages-1)
        # replace in template
        pagetext = replacetext(templatetext, replacedict)
        # write to file
        outfile = outdir + os.path.sep + urlfrompagenum(pagenum)
        print(f"generating {outfile}")
        ofp = open(outfile, "w", encoding='iso-8859-1')
        ofp.write(pagetext)
        ofp.close()
    # Open the page
    subprocess.Popen(f'{os.path.join(outdir, "index.html")}', shell=True)

if __name__ == '__main__':
    main(sys.argv)
