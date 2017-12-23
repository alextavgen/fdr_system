import os
import time

import cv2
import face_recognition

print (os.getcwd())



def main():
    import engine.engine as engine
    engine = engine.Engine()
    video_capture = cv2.VideoCapture(0)

    # Attach engine


    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    try:
        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(small_frame)
                face_encodings = face_recognition.face_encodings(small_frame, face_locations)

                timestamp = time.time()
                face_names, is_new = engine.handle(face_encodings,timestamp)

            process_this_frame = not process_this_frame


            # Display the results
            for (top, right, bottom, left), (face_uuid, name) in zip(face_locations, face_names.items()):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, str(face_uuid), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                crop_img = frame[top:bottom, left:right]
                cv2.imshow(name + str(face_uuid), crop_img)

                #print((top, right, bottom, left))
                if is_new:
                    #SAVE FACE
                    file_path = engine.save_to_file(face_uuid, crop_img)
                    engine.persist(face_uuid, file_path)
            # Display the resulting image
            cv2.imshow('Video', frame)


        # Release handle to the webcam
    except KeyboardInterrupt:
        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fr_settings')
    import django

    django.setup()
    main()
