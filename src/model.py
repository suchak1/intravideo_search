from controller import Worker
import os
import time
import torch
import sys
import cv2
import pickle
import warnings
from PIL import Image
from torchvision import transforms
from seer_model import EncoderCNN, DecoderRNN
from multiprocessing import Pool
sys.path.append('utils')
import my_pytube


class Job:

    "Model - data logic"

    def __init__(self, settings, multi=None):
        if isinstance(settings, type(None)):
            self.video_path = None
            self.settings = None
        else:
            self.settings = settings['settings']
            self.video_path = settings['video']
        # disable multiprocessing on mac os
        if multi is None:
            self.multi = sys.platform != 'darwin'
        else:
            self.multi = multi

    def multi_map(self, fxn, arr):
        # Given a function and a list to iterate over, multi_map will attempt
        # to leverage multiprocessing to speed up the operation.
        # If unsuccessful, will default to nonconcurrent method (slow).

        if self.multi:
            with Pool() as pool:
                results = pool.map(fxn, arr)
                pool.close()
                pool.join()
            return results
        else:
            return [fxn(elem) for elem in arr]

    def handle_vid(self):
        video_path = self.video_path
        if 'youtube.com' in video_path or 'youtu.be/' in video_path: # if given YouTube URL
            yt_vid_path = self.get_from_yt(video_path)
            if yt_vid_path: # if non-empty string
                self.video_path = yt_vid_path

    def do_the_job(self, queue=None):
        try:
            self.handle_vid()
        except:
            queue.put(-1)
            return queue
        video = cv2.VideoCapture(self.video_path)
        video.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
        mRuntime = video.get(cv2.CAP_PROP_POS_MSEC)
        self.settings['runtime'] = int(mRuntime // 1000)
        data = self.classify_frames()
        results = self.interpret_results(data, self.settings['conf'])
        queue.put(len(results))
        self.save_clips(results)
        return queue

    def get_frame(self, timestamp):
        video = cv2.VideoCapture(self.video_path)
        video.set(cv2.CAP_PROP_POS_MSEC, (timestamp * 1000))
        success, frame = video.read()
        if not success:
            warnings.warn(
                f'This time ({timestamp} sec) does not exist in the video.')
            return None
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return (img, timestamp)

    def get_frames(self):
        # Given video and poll setting, returns list of tuples
        # where the first element is an Image of the frame from the video
        # at each timestamp designated by poll setting, and the second
        # element is the timestamp. For example, if poll is 5, get_frames()
        # will return a frame every 5 seconds at timestamps 0, 5, 10, etc.
        # seconds, i.e. it will return [(frame, 0), (frame, 5), (frame, 10)...]
        print('Retrieving video frames...')
        poll = int(self.settings['poll'])
        runtime = int(self.settings['runtime'])
        poll_times = list(range(0, runtime + poll, poll))
        timestamps = [time for time in poll_times if time <= runtime]
        frames = self.multi_map(self.get_frame, timestamps)
        frames = [frame for frame in frames if frame]
        frame_num = len(frames)
        print(f'{frame_num} frames retrieved successfully.')
        return frames

    def classify_frame(self, frame):
        img, time = frame
        classifications = Worker().classify_img(img)
        for term in self.settings['search']:
            if term in classifications:
                prob = round(classifications[term], 2)
                print(f'{term} at {time} sec with probability: {prob}%')
        return (time, self.score(classifications) / 100)

    def classify_frames(self):
        frames = self.get_frames()
        num_frames = len(frames)
        print(f'Classifying {num_frames} frames...')
        results = self.multi_map(self.classify_frame, frames)
        print(f'{num_frames} frames classified successfully.')
        return list(sorted(results, key=lambda x: x[0]))

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
        clip_num = len(timestamps)
        if not timestamps:
            print('No clips found.')
        else:
            print(f'Saving {clip_num} clips...')
        success = timestamps and self.multi_map(
            Worker(self.video_path).make_clip, timestamps)
        if success:
            print(f'{clip_num} clips saved successfully.')
        return success


    def kill(self):
        del self


    def get_from_yt(self, url):
        # input YouTube video URL
        # output string of path to downloaded video
        folder_path = './test'
        vid_path = ''
        for i in range(3):
            try:
                yt = my_pytube.YouTube(url)
                vid = yt.streams.filter(file_extension = 'mp4',progressive=True).first()
                name = vid.default_filename

                files = os.listdir(folder_path)
                already_dl = [file for file in files if name in file and file[-4:] == '.mp4']

                if already_dl:
                    print(already_dl)
                    vid_path = os.path.join(folder_path, already_dl[0])
                    print(f'Found already downloaded video: {already_dl[0]}')
                    break

                print('Downloading video...')
                vid_path = vid.download(output_path=folder_path)
                print('Download complete.')
                break
            except Exception as e:
                if i == 2:
                    raise ValueError("Your video could not be downloaded: %s" % e)
                else:
                    time.sleep(5)

        return vid_path

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
        with open(self.vocab_path, 'rb') as f:
            self.vocab = CustomUnpickler(open(self.vocab_path, 'rb')).load()

        # The Model
        self.encoder, self.decoder = self.prepare_model()


    def prepare_model(self):
        # This is a utility to load and otherwise prepare the pytorch model.
        # It is only used in initialization of the Seer class.
        # Create a new destination file
        if not os.path.isfile(self.encoder_path):
            whole_encoder = open(self.encoder_path, 'wb')
            parts = [os.path.join('torchdata',file) for file in os.listdir('torchdata/') if 'part' in file]
            parts.sort()
            for file in parts:
                input_file = open(file, 'rb')
                while True:
                    bytes = input_file.read()
                    if not bytes:
                        break
                    whole_encoder.write(bytes)
                input_file.close()
            whole_encoder.close()


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
