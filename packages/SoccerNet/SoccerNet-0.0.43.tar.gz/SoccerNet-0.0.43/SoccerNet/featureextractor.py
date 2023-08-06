import math
from tensorflow.keras.models import Model  # pip install tensorflow (==2.3.0)
from tensorflow import keras
import os
# import argparse
import numpy as np
import cv2  # pip install opencv-python (==3.4.11.41)
import imutils  # pip install imutils
import skvideo.io
from tqdm import tqdm

# from SoccerNet import getListTestGames, getListGames


from .utils import getListGames

class FeatureExtractor():
    def __init__(self, rootFolder, feature="ResNet", video="LQ", back_end="TF2"):
        self.rootFolder = rootFolder
        self.feature = feature
        self.video = video
        self.back_end = back_end
        self.verbose = True
        self.preprocess = "crop"
        self.overwrite = False

        if self.back_end == "TF2":
            # import TF and keras only AFTER the GPU has been selected

            # create pretrained encoder (here ResNet152, pre-trained on ImageNet)
            base_model = keras.applications.resnet.ResNet152(include_top=True,
                                                            weights='imagenet', input_tensor=None, input_shape=None,
                                                            pooling=None, classes=1000)

            # define model with output after polling layer (dim=2048)
            self.model = Model(base_model.input, outputs=[
                        base_model.get_layer("avg_pool").output])
            self.model.trainable = False
            # model.summary()

            # sanity test for the model with random input
            IMG_SIZE = image_size = 224
            IMG_SHAPE = (IMG_SIZE, IMG_SIZE, 3)
            input_data = np.random.rand(1, *IMG_SHAPE)
            result = self.model.predict(input_data)
            if (self.verbose):
                print(result[0].shape)

        

    def extractAllGames(self):
        for game in getListGames():
            self.extract(video_path=os.path.join(self.rootFolder, game, "1.mkv"))
            self.extract(video_path=os.path.join(self.rootFolder, game, "2.mkv"))

    def extractGameIndex(self, index):
        self.extract(video_path=os.path.join(self.rootFolder, getListGames()[index], "1.mkv"))
        self.extract(video_path=os.path.join(self.rootFolder, getListGames()[index], "2.mkv"))

    def extract(self, video_path):
        if self.back_end == "TF2":

            feature_path = video_path.replace(
                ".mkv", f"_{self.feature}_{self.back_end}.npy")

            if os.path.exists(feature_path) and not self.overwrite:
                return
            #     # print("len", np.load(feature_path).shape[0])
            #     # if np.load(feature_path).shape[0] >= 5400 and not self.overwrite:

            #     # print(old_feature_path)

            #     old_feature = np.load(old_feature_path)
            #     # print("old", old_feature.shape)
            #     new_feature = np.load(feature_path)
            #     # print("new", new_feature.shape)
            #     if (np.abs(old_feature.shape[0] - new_feature.shape[0]) < 1):
            #         print("same shape")
            #         # return
            #     else:
            #         print("DIFFERENT SHAPE!!!!!", "v1", old_feature.shape,
            #             "--> v2", new_feature.shape)
                    # return

            # Read RELIABLE lenght for the video, in second
            if self.verbose:
                print("video path", video_path)
            v = cv2.VideoCapture(video_path)
            v.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
            time_second = v.get(cv2.CAP_PROP_POS_MSEC)/1000
            if self.verbose:
                print("duration video", time_second)
            import json
            metadata = skvideo.io.ffprobe(video_path)
            # print(metadata.keys())
            # print(json.dumps(metadata["video"], indent=4))
            # getduration
            # print(metadata["video"]["@avg_frame_rate"])
            # # print(metadata["video"]["@duration"])

            # Knowing number of frames from FFMPEG metadata w/o without iterating over all frames
            videodata = skvideo.io.FFmpegReader(video_path)
            (numframe, _, _, _) = videodata.getShape()  # numFrame x H x W x channels
            if self.verbose:
                print("shape video", videodata.getShape())

            # # extract REAL FPS
            fps_video = metadata["video"]["@avg_frame_rate"]
            fps_video = float(fps_video.split("/")[0])/float(fps_video.split("/")[1])
            # fps_video = numframe/time_second
            if self.verbose:
                print("fps=", fps_video)
            time_second = numframe / fps_video

            # vidcap = cv2.VideoCapture(video_path)
        # fps = vidcap.get(cv2.CAP_PROP_FPS)
        
            try:
                
                metadata = skvideo.io.ffprobe(video_path)
                # print("metadata", metadata["video"])
                for entry in metadata["video"]["tag"]:
                    # print(entry)
                    # entry = entry[0]
                    # print(entry)
                    # entry = entry[0]
                    # print(entry)
                    if list(entry.items())[0][1] == "DURATION":
                        # print("entry", entry)
                        duration = list(entry.items())[1][1].split(":")
                        # print(duration)
                        time_second = int(duration[0])*3600 + \
                            int(duration[1])*60 + float(duration[2])
                        # print(time_second)
                        fps_video = numframe / time_second

            except:
                pass

            # fps_meta = json.dumps(metadata["video"]['@avg_frame_rate'], indent=4).replace('"','')
            # fps = int(fps_meta.split('/')[0])/int(fps_meta.split('/')[1])

            # time_second = numframe / fps_video
            if self.verbose:
                print("duration video", time_second)
            frames = []
            videodata = skvideo.io.vreader(video_path)
            fps_desired = 2
            drop_extra_frames = fps_video/fps_desired

            will_have_size = 0
            for i_frame in range(numframe):
                # print(i_frame % drop_extra_frames)
                if (i_frame % drop_extra_frames < 1):
                    will_have_size += 1

            print("will have size", will_have_size)
            if os.path.exists(feature_path):
                if new_feature.shape[0] == will_have_size:
                    print("will not change... go to next video")
                    return

            for i_frame, frame in tqdm(enumerate(videodata), total=numframe):
                # print(i_frame % drop_extra_frames)
                if (i_frame % drop_extra_frames < 1):

                    if self.preprocess == "resize256crop224":  # crop keep the central square of the frame
                        frame = imutils.resize(frame, height=256)  # keep aspect ratio
                        # number of pixel to remove per side
                        off_side_h = int((frame.shape[0] - 224)/2)
                        off_side_w = int((frame.shape[1] - 224)/2)
                        frame = frame[off_side_h:-off_side_h,
                                    off_side_w:-off_side_w, :]  # remove them

                    elif self.preprocess == "crop":  # crop keep the central square of the frame
                        frame = imutils.resize(frame, height=224)  # keep aspect ratio
                        # number of pixel to remove per side
                        off_side = int((frame.shape[1] - 224)/2)
                        frame = frame[:, off_side:-off_side, :]  # remove them

                    elif self.preprocess == "resize":  # resize change the aspect ratio
                        # lose aspect ratio
                        frame = cv2.resize(frame, (224, 224),
                                        interpolation=cv2.INTER_CUBIC)

                    else:
                        raise NotImplmentedError()
                    frames.append(frame)

            # create numpy aray (nb_frames x 224 x 224 x 3)
            frames = np.array(frames)
            if self.verbose:
                print("frames", frames.shape, "fps=", frames.shape[0]/time_second)

            # predict the featrues from the frames (adjust batch size for smalled GPU)
            result = self.model.predict(frames, batch_size=64, verbose=1)
            if self.verbose:
                print("features", result.shape, "fps=", result.shape[0]/time_second)

            # save the featrue in .npy format
            os.makedirs(os.path.dirname(feature_path), exist_ok=True)
            np.save(feature_path, result)


