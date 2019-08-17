# genbearpages.py
#
# Generate pages for A Bear's Journey from template

import sys
import pdb
import os

instagramfile = r"C:\git\github\sumitsumit.github.io\abearsjourney\assets\instagramlist.txt"
templatefile = r"C:\git\github\sumitsumit.github.io\abearsjourney\assets\index_template.html"
outdir = r"C:\git\github\sumitsumit.github.io\abearsjourney"


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

def main(argv):
    previewmode = False
    if '-preview' in argv:
        print("WARNING: Preview Mode; IG script suppressed")
        previewmode = True
    numbearsperpage = 3
    
    fp = open(instagramfile, 'r', encoding='iso-8859-1')
    igblocks = [line.strip() for line in fp.readlines()]
    fp.close()

    numigblocks = len(igblocks)
    print(f"Found {numigblocks} instagram blocks")
    templatetext = "\n".join(readlines(templatefile))
    numpages = int(len(igblocks)/numbearsperpage)
    print(f"Generating {numpages} pages")
    
    if len(igblocks) % numbearsperpage != 0:
        numpages += 1
    for pagenum in range(numpages):
        # set up replacedict
        replacedict = {}
        if previewmode:
            replacedict['$igscript'] = ''
        else:
            replacedict['$igscript'] = '<script async defer src="//www.instagram.com/embed.js"></script>'
        replacedict['$bear0'] = igblocks[pagenum*3 + 0]
        if pagenum*3 + 1 < numigblocks:
            replacedict['$bear1'] = igblocks[pagenum*3 + 1]
        else:
            replacedict['$bear1'] = ''
        if pagenum*3 + 2 < numigblocks:
            replacedict['$bear2'] = igblocks[pagenum*3 + 2]
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

if __name__ == '__main__':
    main(sys.argv)
