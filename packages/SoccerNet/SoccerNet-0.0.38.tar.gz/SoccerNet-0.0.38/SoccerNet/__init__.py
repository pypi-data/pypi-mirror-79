
__version_info__ = ('0', '0', '38')
__version__ = '.'.join(__version_info__)
__authors__ = "Silvio Giancola"
__authors_username__ = "giancos"
__author_email__ = "silvio.giancola@kaust.edu.sa"
__github__ = 'https://github.com/SilvioGiancola/SoccerNetv2'


import logging
from SoccerNet.downloader import SoccerNetDownloader
# from SoccerNet.featureextractor import FeatureExtractor
from SoccerNet.utils import getListGames


from SoccerNet.DataLoader import VideoLoader


try:
    from SoccerNet.DataLoaderTorch import SoccerNetDataLoaderTorch
except:
    logging.info("Install Torch for SoccerNetDataLoaderTorch")
    pass


try:
    from SoccerNet.DataLoaderTensorFlow import SoccerNetDataLoaderTensorFlow
except:
    logging.info("Install TensorFlow for SoccerNetDataLoaderTensorFlow")
    pass


