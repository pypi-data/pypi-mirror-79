


class FeatureExtractor():
    def __init__(self, rootFolder, feature="ResNet", video="LQ", back_end="TF"):
        self.rootFolder = rootFolder
        self.feature = feature
        self.video = video
        self.back_end = back_end
        

    def extractAllGames(self):
        for game in getListGames():
            extract(os.path.join(self.rootFolder, game, "1.mkv"))
            extract(os.path.join(self.rootFolder, game, "2.mkv"))

    def extractGameIndex(self, index):

    def extract(self, video_path):
        if back
        for file in files:

            GameDirectory = os.path.join(self.LocalDirectory, game)
            FileURL = os.path.join(
                self.OwnCloudServer, game, file).replace(' ', '%20')
            os.makedirs(GameDirectory, exist_ok=True)

            # LQ Videos
            if file in ["1.mkv", "2.mkv"]:
                res = self.downloadFile(path_local=os.path.join(GameDirectory, file),
                                        path_owncloud=FileURL,
                                        user="6XYClm33IyBkTgl",  # user for video LQ
                                        password=self.password)

            # HQ Videos
            elif file in ["1_HQ.mkv", "2_HQ.mkv", "video.ini"]:
                res = self.downloadFile(path_local=os.path.join(GameDirectory, file),
                                        path_owncloud=FileURL,
                                        user="B72R7dTu1tZtIst",  # user for video HQ
                                        password=self.password)

            # Labels
            elif file in ["Labels.json"]:
                res = self.downloadFile(path_local=os.path.join(GameDirectory, file),
                                        path_owncloud=FileURL,
                                        user="ZDeEfBzCzseRCLA",  # user for Labels
                                        password="SoccerNet")

            # features
            elif any(feat in file for feat in ["ResNET", "C3D", "I3D"]):
                res = self.downloadFile(path_local=os.path.join(GameDirectory, file),
                                        path_owncloud=FileURL,
                                        user="9eRjic29XTk0gS9",  # user for Features
                                        password="SoccerNet")
