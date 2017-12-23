import face_recognition
import uuid
import logging
import os
import datetime
import cv2
import json

from fdr_backend.models import FaceEntry
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


TOLERANCE = 0.6


class FaceEntryInMemory():
    def __init__(self, face_uuid, face_encoding, timestamp):
        self.face_uuid = face_uuid
        self.face_encoding = face_encoding
        self.timestamp = timestamp



class Engine():
    def __init__(self):
        self.faces={}


    def handle(self,face_encodings, timestamp):
        face_names = self._process_face_recognition_results_(face_encodings, timestamp)
        return face_names

    def is_new_face(self, face_uuid):
        return face_uuid not in self.faces

    def add_face(self,face_encodings, timestamp):
        self._process_face_recognition_results_(face_encodings)

    def attach_face_image(self, face_uuid, image):
        face_entry = self.faces[face_uuid]
        face_entry.image = image

    def persist(self, face_uuid, file_path):
        face_entry_persistent = FaceEntry(uuid=face_uuid, face_encoding_json=json.dumps(self.faces[face_uuid]),
                                          image=file_path)
        face_entry_persistent.save()
        logger.debug('Saved new FaceEntry')

    def save_to_file(self, face_uuid, image):
        todayDate = datetime.datetime.now().strftime("%Y-%d-%m")
        directory = './detected_faces/' + todayDate
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, str(face_uuid)+'.png')
        cv2.imwrite(file_path, image)
        return file_path

    def _process_face_recognition_results_(self,face_encodings, timestamp):
        face_names = {}
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            # print(face_encoding)
            match = face_recognition.compare_faces(
                                [face_entry.face_encoding for face_entry in self.__get_known_faces_list__()],
                                face_encoding, tolerance=TOLERANCE)
            name = "Unknown"

            is_matched, matched_uuids = self.__get_match_uuid__(match)

            if (len(matched_uuids)>1):
                logger.warning('Match more than one face, set tolerance at lower level ')

            if is_matched:
                name = "Known"
                face_names[matched_uuids[0]] = name
                logger.debug('Matched uuid: ' + str(matched_uuids))
            else:
                uuid_for_face = self.__add_to_known_faces_dict__(face_encoding, timestamp)

                face_names[uuid_for_face] = name
                logger.debug('Created new uuid: ' + str(uuid_for_face))

        return face_names

    def __get_match_uuid__(self, match):
        matched_uuid_list = []
        is_matched = False
        for match_result, face_entry in zip(match, self.__get_known_faces_list__()):
            if match_result:
                matched_uuid_list.append(face_entry.face_uuid)
                is_matched = True
        return is_matched, matched_uuid_list

    def __add_to_known_faces_dict__(self, face_encoding, timestamp):
        face_uuid = uuid.uuid4()
        self.faces[face_uuid] = FaceEntryInMemory(face_uuid, face_encoding, timestamp)
        return face_uuid

    def __get_known_faces_list__(self):
        return [face_entry for _, face_entry in self.faces.items()]

    def matched_uuid(self,match):
        for match_result in match:
            if match_result:
                return True
        return False
