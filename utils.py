import sox
import config

##########################################################################################

def create_filename_dictionary(channel_assignment):

    '''
    This function uses the channel assignment table to create a dictionary which is
    easier to use for file naming.

    :param channel_assignment: numpy array with the channel assignment table
    :return: dictionary of dictionaries with the information
    '''

    headers = ['Logic', 'All', 'Basses', 'QuartetB', 'QuartetA', 'Shortcuts']

    nrows, ncols = channel_assignment.shape

    filename_dict = {}

    for i in range(nrows):
        chann = {}
        for j in range(1, ncols):
            chann[headers[j]] = channel_assignment[i, j]
            filename_dict[channel_assignment[i, 0]] = chann

    return filename_dict

##########################################################################################

def generate_filename(input_filename,segment_info,filename_dictionary):

    track = input_filename[:-4]

    ##
    # Segment info
    # [2] songID
    # [3] group
    # [4] take
    ##

    songid,group,take = segment_info[2],segment_info[3],segment_info[4]
    if not take == 'Solo':
        singer = filename_dictionary[track][group]
    else:
        singer = segment_info[5]
    shortcut = filename_dictionary[track]['Shortcuts']

    output_filename = "{}_{}_{}_{}_{}.wav".format(songid,group,take,singer,shortcut)
    return output_filename

##########################################################################################

def cut_audiofile_iteratively(input_filename,bounds,filename_dict):

    '''

    :param input_filename: filename of the audio to cut
    :param bounds: numpy array with the time boundaries of each segment and associated labels
    :param output_path: path of the folder where cut files should be exported
    :return: void function

    '''

    cnt=0
    # cut one segment of the input audio at each iteration of the for loop
    for line in bounds:

        cnt+=1
        # define time boundaries of each segment
        tin,tout = line[0],line[1]

        tfm = sox.Transformer()
        tfm.trim(tin,tout)

        output_filename = generate_filename(input_filename,line,filename_dict)

        if 'nan' in output_filename: continue

        tfm.build(config.input_path+input_filename,config.output_path+output_filename)

        print(cnt)

##########################################################################################




