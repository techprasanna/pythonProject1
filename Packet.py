from json import JSONEncoder


class Packet_Structure:

    def __init__(self, Cam_IP, Number_Faces, Images, AreaID, Timestamp, Frag_bit):
        self.Cam_IP = Cam_IP
        self.Number_Faces = Number_Faces
        self.Images = Images
        self.AreaID = AreaID
        self.Timestamp = Timestamp
        self.Frag_bit = Frag_bit

    def get_Cam_IP(self):
        return self.Cam_IP

    def get_Number_Faces(self):
        return self.Number_Faces

    def get_AreaID(self):
        return self.AreaID

    class EmployeeEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

