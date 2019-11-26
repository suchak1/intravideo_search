from controller import Worker
import os
import torch
import sys
import cv2
import pickle
from torchvision import transforms
import numpy as np
sys.path.append('utils')
from build_vocab import Vocabulary
from seer_model import EncoderCNN, DecoderRNN
from PIL import Image
#from multiprocessing import Pool

class Job:

    "Model - data logic"

    def __init__(self, settings):
        if not isinstance(settings, type(None)):
            if 'youtube.com' in settings['video']: # if given YouTube URL
                yt_vid_path = self.get_from_yt(settings['video'])
                if not yt_vid_path: # if empty string
                    self.video_path = settings['video']
                else: # if YouTube video successfully downloaded
                    self.video_path = yt_vid_path
            else: # if given string was not a YouTube URL
                self.video_path = settings['video']

            #self.video_path = settings['video']
            self.settings = settings['settings']
            # self.do_the_job()
        else:
            self.video_path = None
            self.settings = None

    def do_the_job(self):
        data = self.classify_frames()
        results = self.interpret_results(data)
        self.save_clips(results)

    def get_frames(self):
        # Given video and poll setting, returns list of tuples
        # where the first element is an Image of the frame from the video
        # at each timestamp designated by poll setting, and the second
        # element is the timestamp. For example, if poll is 5, get_frames()
        # will return a frame every 5 seconds at timestamps 0, 5, 10, etc.
        # seconds, i.e. it will return [(frame, 0), (frame, 5), (frame, 10)...]
        vidPath = self.video_path
        poll = self.settings['poll']
        count = 0
        frms = []
        video = cv2.VideoCapture(vidPath)
        success = True
        while success:
            timestamp = (count*poll)
            video.set(cv2.CAP_PROP_POS_MSEC, (timestamp*1000))
            success,frame = video.read()
            if success:
                cv2.imwrite('frame%d.jpg' % count, frame) # save frame as .jpg
                try:
                    f = Image.open('frame%d.jpg' % count) # make frame Image
                    os.remove('frame%d.jpg' % count) # delete frame.jpg
                    frms.append((f,timestamp))
                except:
                    raise NameError('getFrameError')
            count += 1
        return frms

    def classify_frames(self):
        frames = self.get_frames()
        results = [(self.score(Worker().classify_img(f)), t) for (f, t) in frames]
        norm = 100
        results = [(val / norm, t) for (val, t) in results]
        return list(sorted(results, key=lambda x: x[1]))

    def score(self, confidence_dict):
        search_terms = self.settings['search']
        max_score = 0
        for term in search_terms:
            max_score = max(max_score, confidence_dict.get(term, 0))
        return max_score

    def has_valid_args_interpret_results(self, results, cutoff):
        # This is a very simple helper function which throws an exception
        # in the case of invalid arguments. The functionality of this is
        # sufficiently tested in the tests of the interpret_results() function.

        if not isinstance(results, type([])):
            raise TypeError("Expected List. Got {}".format(type(results)))
        timeSet = set()
        for elt in results:
            if elt[0] < 0:
                raise ValueError("Negative time stamp in results. Please don't do that. Got {}".format(elt[0]))
            if elt[1] < 0:
                raise ValueError("Negative score in results. Don't do this to me. Got {}".format(elt[1]))
            if elt[1] > 1:
                raise ValueError("Un-normalized score in results. Got {}, expected value in [0,1]".format(elt[1]))
            if elt[0] in timeSet:
                raise ValueError("Duplicate times in results. Found more than one of: {}".format(elt[0]))
            else:
                timeSet.add(elt[0])
            if elt[0] < sorted(list(timeSet))[-1]:
                raise ValueError("Results given out of order. I could fix this, but \
                this probably means something is funky with whatever process produced this.")
            if cutoff < 0:
                raise ValueError("Cutoff parameter less than zero. Got: {}".format(cutoff))

    def interpret_results(self, results, cutoff=0.5):
        # Assuming arg: results is something like a list of tuples
        # of the form ((float)timestamp_t, (float)APIScore_t)
        # where APIScore_t is the score given by classify_frames()
        # to each frame_t fed through the API, normalized to be between [0,1].
        # Also assuming "runtime" is included in settings.

        # Checking that the arguments are valid.
        self.has_valid_args_interpret_results(results, cutoff)

        # If there are no results, return an empty list.
        if len(results) == 0:
            return []

        # For each positive result, find the proper start/end times of the
        # relevant sub-clip.
        positiveResults = []
        i = 0
        while(True):
            if i >= len(results):
                break
            if results[i][1] >= cutoff:
                foundEnd = False
                for j in range(i+1, len(results)):
                    if results[j][1] < cutoff:
                        positiveResults.append((i, j))
                        foundEnd = True
                        break
                if foundEnd:
                    i = j+1
                    continue
                else:
                    positiveResults.append((i, -1))
                    break
            else:
                i += 1
                continue

        # Adjust those times to fit in the midpoint of the polled frames,
        # for a smoother results.
        adjustedEndpoints = []
        for endpts in positiveResults:
            startIdx = endpts[0]
            endIdx = endpts[1]

            result1 = results[startIdx]
            result2 = results[endIdx]

            if startIdx == 0:
                startTime = 0.0
            else:
                thisTime = result1[0]
                lastTime = results[startIdx-1][0]
                startTime = (thisTime + lastTime) / 2

            if endIdx == -1:
                endTime = self.settings["runtime"]
            else:
                finalTime = results[endIdx-1][0]
                nextTime = results[endIdx][0]
                endTime = (finalTime + nextTime) / 2

            adjustedEndpoints.append((startTime, endTime))

        return adjustedEndpoints


    def save_clips(self, timestamps):
        #with Pool() as pool:
        #    v = self.video_path
        #    args_list = [(t, v) for t in timestamps]
        #    map_results = pool.starmap(Worker().make_clip, args_list)

        #return map_results
        # multiprocessing is running into issues with shared resources
        v = self.video_path
        return [Worker().make_clip(t, v) for t in timestamps]


    def kill(self):
        del self


    def get_from_yt(self, url):
        # input YouTube video URL
        # output string of path to downloaded video
        return ['todo']

class Seer():
    def __init__(self):
        # Device Config. Use GPU if available.
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Default Paths
        self.vocab_path = 'torchdata/vocab.pkl'
        self.encoder_path = 'torchdata/encoder-5-3000.pkl'
        self.decoder_path = 'torchdata/decoder-5-3000.pkl'

        # Default Model Parameters
        self.embed_size = 256
        self.hidden_size = 512
        self.num_layers = 1
        self.vocab = CustomUnpickler(open(self.vocab_path, 'rb')).load()

        # The Model
        self.encoder, self.decoder = self.prepare_model()


    def prepare_model(self):
        # This is a utility to load and otherwise prepare the pytorch model.
        # It is only used in initialization of the Seer class.
        encoder = EncoderCNN(self.embed_size).eval()  # eval mode (batchnorm uses moving mean/variance)
        decoder = DecoderRNN(self.embed_size, self.hidden_size, len(self.vocab), self.num_layers)
        encoder = encoder.to(self.device)
        decoder = decoder.to(self.device)
        # Load the trained model parameters
        encoder.load_state_dict(torch.load(self.encoder_path))
        decoder.load_state_dict(torch.load(self.decoder_path))

        return encoder, decoder

    def tell_us_oh_wise_one(self, pilImage):
        # This is the method which produces a caption given an image (PIL Image)
        # The argument type is str and the return type is str.
        img = self.prepare_data(pilImage)
        features = self.encoder(img)
        sampled_ids = self.decoder.sample(features)
        sampled_ids = sampled_ids[0].cpu().numpy()

        # Convert word_ids to words
        sampled_caption = []
        for word_id in sampled_ids:
            word = self.vocab.idx2word[word_id]
            if word == '<end>':
                break
            sampled_caption.append(word)
        if sampled_caption[-1] == ".":
            sampled_caption = sampled_caption[:-1]
        caption = ' '.join(sampled_caption[1:])
        return caption

    def prepare_data(self, pilImage):
        # This is a private utility for the tell_us_oh_wise_one method.
        # This loads and preproceses the image, normalizing, resizing etc.
        # Image preprocessing
        transform = transforms.Compose([transforms.ToTensor(),
                                        transforms.Normalize((0.485, 0.456, 0.406),
                                                             (0.229, 0.224, 0.225))])
        image = pilImage.resize([224, 224], Image.LANCZOS)
        image = transform(image).unsqueeze(0)
        image_tensor = image.to(self.device)

        return image_tensor


class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == 'Vocabulary':
            from build_vocab import Vocabulary
            return Vocabulary
        return super().find_class(module, name)
