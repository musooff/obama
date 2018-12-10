import re # module for regular expressions
from collections import Counter
from moviepy.editor import VideoFileClip, concatenate


def convert_time(timestring):
    """ Converts a string into seconds """
    nums = map(float, re.findall(r'\d+', timestring))
    return 3600*nums[0] + 60*nums[1] + nums[2] + nums[3]/1000

def times_texts_maker(sub_file):
    with open(sub_file) as f:
        lines = f.readlines()

    times_texts = []
    current_times , current_text = None, ""
    for line in lines:
        times = re.findall("[0-9]*:[0-9]*:[0-9]*,[0-9]*", line)
        if times != []:
            current_times = map(convert_time, times)
        elif line == '\n':
            times_texts.append((current_times, current_text))
            current_times, current_text = None, ""
        elif current_times is not None:
            current_text = current_text + line.replace("\n"," ")
    return times_texts


def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

def words_list(sub_file):
    with open(sub_file,'r') as f:
        words = f.read().lower().split()
    return words

shape_words =remove_duplicates(words_list("shapeofyou.txt"))
print shape_words

def word_counter(times_and_texts):
    whole_text = " ".join([text for (time, text) in times_and_texts])
    all_words = re.findall("\w+", whole_text)
    counter = Counter([w.lower() for w in all_words if (w.lower() in shape_words)])
    return counter
def word_counter_2(sub_file):
    #whole_text = " ".join([text for (time, text) in times_and_texts])
    common_words = [w for w in words_list(sub_file) if (w in shape_words)]
    #print is_words
    counter = Counter([w for w in common_words])
    return [remove_duplicates(common_words), counter]


def word_timing(word, tt):
    return [times for (times,text) in tt
        if (re.findall(word,text) != [])]


#print word_counter_2("int1.txt")

def find_word(word, padding=.05):
    """ Finds all 'exact' (t_start, t_end) for a word """
    matches = [re.search(word, text)
               for (t,text) in times_texts]
    return [(t1 + m.start()*(t2-t1)/len(text) - padding,
             t1 + m.end()*(t2-t1)/len(text) + padding)
             for m,((t1,t2),text) in zip(matches, times_texts)
             if (m is not None)]

def assemble_cuts(inputfile, cuts, outputfile):
    """ Concatenate cuts and generate a video file. """
    video = VideoFileClip(inputfile)
    final = concatenate([video.subclip(start, end)
                         for (start,end) in cuts])
    final.write_videofile(outputfile, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)
def least_commong_word_clips(lst):
    for word in words_int1:
        if (lst[word] < 10):
            assemble_cuts("int1.mp4", word_timing(word),word+".mp4")

def get_all_word_clips(int_sub,int_int):

    t_and_t = times_texts_maker(int_sub)
    common_words, counter = word_counter_2(int_sub)
    print common_words
    print counter
    #assemble_cuts(int_int, word_timing("best", t_and_t),"best.mp4")
    for word in common_words:
        if counter[word] < 15:
            assemble_cuts(int_int, word_timing(word, t_and_t),word+".mp4")
            break

get_all_word_clips("int1.txt","int1.mp4")
#assemble_cuts(word_timing("i'm"),"i'm.mp4")
#assemble_cuts(word_timing("with"),"with.mp4")
#assemble_cuts(word_timing("nobody"),"nobody.mp4")