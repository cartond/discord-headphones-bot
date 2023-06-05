from io import BytesIO
# import io
from PIL import Image, ImageDraw
import face_recognition
import math


def flip_facial_landmarks_horizontally(landmarks):
    # If landmarks are
    # [(474, 76), (473, 89), (473, 101)....]
    # We want to keep the X value, but flip the Y values
    # Meaning we look at the diff and flip based on first? at half way we need to swap to flipping from last value maybe? Idk
    # diffs: 0, 13, 25 then minus them from first val
    # [(474, 76), (473, 63), (473, 51)....]
    # I think that just means yFN = y0 - (yN - y0)

    # This is lazy, but get the lower side and base off that
    y0 = max(landmarks[0][1], landmarks[-1][1])

    new_landmarks = []

    for landmark in landmarks:
        yN = landmark[1]
        yFN = y0 - (yN - y0)
        new_landmarks.append((landmark[0], yFN))
    
    return new_landmarks

def draw_headphones(image_bytes):
    # Load the jpg file into a numpy array
    image = face_recognition.load_image_file(BytesIO(image_bytes))

    # Find all facial features in all the faces in the image
    face_landmarks_list = face_recognition.face_landmarks(image)

    print("I found {} face(s) in this photograph.".format(len(face_landmarks_list)))

    # Create a PIL imagedraw object so we can draw on the picture
    pil_image = Image.fromarray(image)
    d = ImageDraw.Draw(pil_image)

    if len(face_landmarks_list) == 0:
        return None

    # for face_landmarks in face_landmarks_list:
    for i, face_landmarks in enumerate(face_landmarks_list):
        print('looking at face', i)

        keys_wanted = ['chin']
        print('\tFeature keys: ', face_landmarks.keys())
        print('\tFeature keys WATNED: ', keys_wanted)
        # Print the location of each facial feature in this image
        for facial_feature in face_landmarks.keys():
            if facial_feature not in keys_wanted: 
                continue
            print("\tThe {} in this face has the following points: {}".format(facial_feature, face_landmarks[facial_feature]))

        # # Let's trace out each facial feature in the image with a line!
        # for facial_feature in face_landmarks.keys():
        #     if facial_feature not in keys_wanted: 
        #         continue
        #     d.line(face_landmarks[facial_feature], width=5)
        
        # Flip and draw chin line
        for facial_feature in face_landmarks.keys():
            if facial_feature not in keys_wanted: 
                continue
            flipped_landmarks = flip_facial_landmarks_horizontally(face_landmarks[facial_feature])
            print(face_landmarks[facial_feature])
            print(flipped_landmarks)
            # Overhead line
            d.line(flipped_landmarks, width=5, fill="grey")

            # Mic line (just half, but not flipped)
            half_points = math.floor(len(face_landmarks[facial_feature]) / 2)
            d.line(face_landmarks[facial_feature][0:half_points], width=5, fill="grey")

            # Mic foam
            d.ellipse(
                [
                    (face_landmarks[facial_feature][half_points-1][0]-10, face_landmarks[facial_feature][half_points-1][1]-10),
                    (face_landmarks[facial_feature][half_points+1][0]+5, face_landmarks[facial_feature][half_points+1][1]+5)
                ], 
                fill='black', 
                width=1
            )

            # Left headphone 
            d.ellipse(
                [
                    (face_landmarks[facial_feature][0][0]-10, face_landmarks[facial_feature][0][1]-10),
                    (face_landmarks[facial_feature][3][0]+10, face_landmarks[facial_feature][3][1]+10)
                ], 
                fill='black', 
                width=3
            )

            d.line([face_landmarks[facial_feature][0][0]-10, face_landmarks[facial_feature][0][1]-10], width=5, fill="green")



            print(face_landmarks[facial_feature])

            # # Right headphone 
            # d.ellipse(
            #     [
            #         (face_landmarks[facial_feature][-4][0], face_landmarks[facial_feature][-4][1]),
            #         (face_landmarks[facial_feature][-1][0], face_landmarks[facial_feature][-1][1])
            #     ], 
            #     fill='black', 
            #     width=3
            # )


    # Show the picture
    pil_image.show()
    bytes = BytesIO()
    pil_image.save(bytes, format='PNG')
    bytes.seek(0)
    return bytes
    # display(pil_image)