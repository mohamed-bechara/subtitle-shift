
### USAGE: srt_time_shift filename.srt <timeshift>
### WHERE timeshift is a +/- float number, representing the number of seconds and milliseconds to shift the timestamps ( -4.9 means shift back by 4 seconds and 900 milliseconds)
### By default timeshift is forward (so, for a backward timeshift, a negative value should be supplied)


import sys

from collections import OrderedDict
import re

src_file = sys.argv[1]
subtitle_extenstion = re.match('(.*)\.(\D+)', src_file)[2]      ### get the file extension

timeshift = float(sys.argv[2])
print('To be shifted by: ' + str(timeshift) + '\n')


### Function to convert the timestamp format of srt file to seconds (float)
### EXAMPLE: srt_time_to_seconds('01:00:42,149') RETURNS 3642.149
def srt_time_to_seconds(timestamp):
    seconds, milliseconds = timestamp.split(',')
    hours, minutes, seconds = seconds.split(':')
    total_seconds = int(hours) * 60 * 60 + int(minutes) * 60 + int(seconds)
    seconds_out = str(total_seconds) + '.' + milliseconds
    return float(seconds_out)


### Function to convert an srt file to an OrderedList with time limits as keys and text as value
def srt_to_dict(file):
    with open(file, 'r', encoding="utf8") as f:
        text = f.read()
    text = re.sub(r'^\d+[\n\r]','',text,flags=re.MULTILINE)
    lines = text.splitlines()

    ### Initialize an OrderedDict object and empty-value key, to be populated by subtitle lines
    output = OrderedDict()
    key = ''

    for line in lines:
        line = line.strip()
        
        ### If line contains '-->', set key to time limits value
        if line.find('-->') > -1:
            key = line
            output[key] = ''
        
        ### If line does not contain '-->', it means it is text under the previous time limits. Append all text under the time limits
        else:
            if key != '':
                output[key] += line + ' '

    f.close()
    return output


### Converts a timestamp in seconds to srt timeformat after shifting it by timeshift value
def shift_seconds_timestamp(timestamp_in_seconds,timeshift):
	
	time = timestamp_in_seconds + timeshift
	hours = (int(time/(60*60)))        
	minutes = (int((time - hours * 3600)/(60)))
	seconds = (int(time - hours * 3600 - minutes * 60))
    
    ### to get the first three digits after the floating point 
	milliseconds = (time - hours * 3600 - minutes * 60 - seconds) * 1000     
	
    ### "{:02.0f}".format(float_num)        # add leading zero if number < 10
	timestamp = "{:02.0f}".format(hours) + ":" + "{:02.0f}".format(minutes) + ":" + "{:02.0f}".format(seconds) + "," + "{:03.0f}".format(milliseconds)
	return timestamp




src_file_to_open = src_file
output = srt_to_dict(src_file_to_open)
srt_timestamp_list = [timestamp for timestamp in output.keys()]
srt_text_list = [text for text in output.values()]


srt_timestamps_shifted = [( shift_seconds_timestamp(srt_time_to_seconds(stamp.split('-->')[0]),timeshift),shift_seconds_timestamp(srt_time_to_seconds(stamp.split('-->')[1]),timeshift)) for stamp in srt_timestamp_list]

output_srt_file = src_file + '-shiftedby' + str(timeshift) + '.srt'

of = open(output_srt_file, 'w', encoding="utf8")

for i in range(len(srt_text_list)):
#    print(i)
#    print(str(srt_timestamps_shifted[i][0]) + ' --> ' + str(srt_timestamps_shifted[i][1]))
#    print(srt_text_list[i])
    of.write(str(i) + "\n")
    of.write(str(srt_timestamps_shifted[i][0]) + ' --> ' + str(srt_timestamps_shifted[i][1]) + "\n")
    of.write(srt_text_list[i] + "\n\n")

of.close()







