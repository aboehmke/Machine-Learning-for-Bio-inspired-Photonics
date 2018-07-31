
def FixFilenames(path):
    '''Takes path (as string), renames all files from top down according to file format:
     date-material_num-misc.spe
    extra thing: returns list of the background files contained in directoryself.
    Background files should contain the label 'bckgrnd'.
    '''
    import os
    for root,dirs,filenames in os.walk(path):
        # print('path: ',root)
        # print('directories: ',dirs)
        # print('filenames: ',filenames)
        if len(dirs) != 0:
            print("given directory mustn't contain subdirectories")
        filenames.sort(key=str.lower)
        newfilenames = []
        for filename in filenames:
            if filename.endswith('.spe'):
                lst = filename.split()
                x = 0
                if len(lst) == 1: # if filename contains no spaces
                    x = x+1
                    newfilename = filename # then hopefully it's right
                else:
                    if lst[0] > '99':
                        # if alphabet instead of numerals at begin of name
                        if 'ws2' in lst[0].lower():
                            lst.insert(0,'1')
                        else:
                            # lst = lst[1:] # then get rid of begin of name.
                            del lst[0]
                            if len(lst) == 1: # then no misc part and date attached to 'WS2'
                                lst0 = lst[0].split('_')
                                lst[0] = lst0[0]
                                lst.append( '_'.join(lst0[1:]) )
                    lst_new = []
                    lst_new.append(lst[0])
                    lst_new.append(lst[1])
                    if len(lst) >= 3: # if filename has misc part
                        misc = '_'.join(lst[2:])
                        lst_new.append(misc)
                    newfilename = '-'.join(lst_new)
                os.rename(path+filename, path+newfilename)
                newfilenames.append(newfilename)
        # ~ extra ~
        filenames,bckgrnds = GetBckgrnds(newfilenames)
        return filenames,bckgrnds

def GetBckgrnds(filenames):
    '''returns list of the bckgrnd file corresponding to each spefile.
    (len(bckgrnds) = num spe files.)
    '''
    # print('length file names before = ',len(filenames)) # = 76
    fnames = []
    bgnames = []
    bg_dct = dict()
    for i in range(len(filenames)):
        fname = filenames[i]
        if 'bckgrnd' in fname:
            # separate spectra and bg files
            bg = fname
            bgnames.append(bg)
            bglst = bg.split('-')
            bgnm = bglst[1].split('_') # [WS2,n1,n2,...]
            bglst[1] = '_'.join(bgnm[:2])
            bgbase = '-'.join(bglst[:2]) # date-WS2_n1
            if bgbase in bg_dct:
                pass
            else:
                bg_dct[bgbase] = bg
        else:
            fnames.append(fname)
    # print('length file names after = ',len(fnames)) # = 54
    bckgrnds = []
    for j in range(len(fnames)):
        fname = fnames[j]
        lst = fname.split('-')
        nm = lst[1].split('_')
        if len(nm) <= 3: # get rid of '.spe'
            y = nm[-1].split('.')
            nm[-1] = y[0]
        lst[1] = '_'.join(nm[:2])
        base = '-'.join(lst[:2])
        bg = bg_dct.get(base)
        if bg == None:
            print('No bg file for ',fname,'?')
        else:
            # print(fname,' goes with ',bg)
            bckgrnds.append(bg)
    print('num fnames (',len(fnames),') should equal num bg (',len(bckgrnds),')')
    return fnames,bckgrnds
