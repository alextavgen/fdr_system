import face_recognition
import uuid
import logging
import os
import datetime
import cv2
import json

from fdr_backend.models import Face, FaceEntry


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


TOLERANCE = 0.8


class FaceEntryInMemory():
    def __init__(self, face_uuid, face_encoding, timestamp):
        self.face_uuid = face_uuid
        self.face_encoding = face_encoding
        self.timestamp = timestamp



class Engine():
    def __init__(self):
        self.faces={}


    def handle(self,face_encodings, timestamp):
        face_names, is_new = self._process_face_recognition_results_(face_encodings, timestamp)
        return face_names, is_new

    def is_new_face(self, face_uuid):
        return face_uuid not in self.faces

    def add_face(self,face_encodings, timestamp):
        self._process_face_recognition_results_(face_encodings)

    def attach_face_image(self, face_uuid, image):
        face_entry = self.faces[face_uuid]
        face_entry.image = image

    def persist(self, face_uuid, file_path, timestamp):
        face_persistent = Face(uuid=face_uuid,
                                          face_encoding_json=json.dumps(self.faces[face_uuid].face_encoding.tolist()),
                                          timestamp=timestamp,
                                          image=file_path)
        face_persistent.save()
        logger.debug('Saved new Face')

    def persist_entry(self, face_uuid, file_path, timestamp):
        face_entry_persistent = FaceEntry(image=file_path, timestamp=timestamp)
        face_by_uuid = Face.objects.get(uuid=face_uuid)
        face_entry_persistent.face = face_by_uuid
        face_entry_persistent.save()
        logger.debug('Saved new FaceEntry')

    def save_to_file(self, face_uuid, image):
        directory = 'faces/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, str(face_uuid) + '.png')
        cv2.imwrite(file_path, image)
        return file_path

    def save_to_file_entry(self, face_uuid, image):
        todayDate = datetime.datetime.now().strftime("%Y-%d-%m")
        directory = 'detected_faces/' + todayDate
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, str(face_uuid) + datetime.datetime.now().strftime("%H:%M:%S") + '.png')
        cv2.imwrite(file_path, image)
        return file_path

    def __fetch_faces_from_db__(self):
        faces = Face.objects.all()
        #self.faces = {}
        for face in faces:
            self.faces[face.uuid] = FaceEntryInMemory(face.uuid, json.loads(face.face_encoding_json), datetime.datetime.now())


    def _process_face_recognition_results_(self,face_encodings, timestamp):
        new_uuids = {}
        face_names = {}
        self.__fetch_faces_from_db__()
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            # print(face_encoding)
            match = face_recognition.compare_faces(
                                [face_entry.face_encoding for face_entry in self.__get_known_faces_list__()],
                                face_encoding, tolerance=TOLERANCE)
            name = "Unknown"

            is_matched, matched_uuids = self.__get_match_uuid__(match)

            if (len(matched_uuids)>1):
                logger.debug('Match more than one face')

            matched_uuids.sort()
            if is_matched:
                name = "Known"
                face_names[matched_uuids[0]] = name
                logger.debug('Matched uuid: ' + str(matched_uuids))
            else:
                uuid_for_face = self.__add_to_known_faces_dict__(face_encoding, timestamp)

                face_names[uuid_for_face] = name
                logger.debug('Created new uuid: ' + str(uuid_for_face))
                new_uuids[uuid_for_face] = name

        return face_names, new_uuids

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
