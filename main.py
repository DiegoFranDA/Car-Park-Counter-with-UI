import cv2
import pickle
import cvzone
import numpy as np
def open_car_park_counter():
    # Video feed
    cap = cv2.VideoCapture('carPark.mp4')

    with open('CarParkPos', "rb") as f:
        posList = pickle.load(f)
    width, height = 107, 48

    """
    we need to know wether this region of interest, has a car in it or not
    we can do that by looking at its pixel count, first we convert this img into a binary img
    based on its edges and corners and from there we can say that if it doesn't have a lot of corners
    if its like a plain image then there is no car otherwise there is a car
    """
    def checkParkingSpace(imgPro):

        spacesCounter=0

        for pos in posList:
            x, y = pos
            imgCrop = imgPro[y:y+height, x:x+width]
            # cv2.imshow(str(x*y), imgCrop)
            # it gives us the count number of white pixels
            count = cv2.countNonZero(imgCrop)

            if count < 900:
                color = (0, 255, 0)
                tickness = 5
                spacesCounter+=1
            else:
                color = (0, 0, 255)
                tickness = 2
            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, tickness)
            cvzone.putTextRect(img, str(count), (x, y + height - 4), scale=1.1,
                               thickness=2, offset=0, colorR=color)
        cvzone.putTextRect(img, f'Free: {spacesCounter}/{len(posList)}', (100, 50), scale=3,
                           thickness=5, offset=20, colorR=(0,200,0))

    while True:
        # WE ARE RESETING THE FRAMES IF THEY REACH THE TOTAL AMOUNT OF FRAMES THAT THE VIDEO HAS
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, img = cap.read()
        # we need to do some thresholding
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # (3,3) dimension of the corner, sigma = 1
        imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
        imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY_INV, 25, 16)
        # to remove extra noise, dots
        imgMedian = cv2.medianBlur(imgThreshold, 5)
        # sometimes the white dots of the cars are a little bit teen so we can thick them for easier recognition
        kernel = np.ones((3,3), np.uint8)
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)


        checkParkingSpace(imgDilate)

        cv2.imshow("Image", img)
        #cv2.imshow("ImageBlur", imgBlur)
        #cv2.imshow("ImageTresh", imgThreshold)
        #cv2.imshow("ImageMedian", imgMedian)
        #cv2.imshow("ImageDilate", imgDilate)
        cv2.waitKey(10)


"""
Primero, la imagen en color img se convierte a escala de grises imgGray utilizando la función cvtColor de OpenCV. Luego, se aplica un desenfoque gaussiano con un kernel de 3x3 y sigma=1 a la imagen en escala de grises imgGray, lo que produce la imagen imgBlur.
A continuación, se utiliza la función adaptiveThreshold de OpenCV para realizar la umbralización adaptativa sobre imgBlur, lo que produce la imagen binaria imgThreshold.
El umbral adaptativo se realiza utilizando el método Gaussiano y el valor del umbral 
se calcula en función del tamaño de los bloques de píxeles adyacentes y del valor de C.
Para reducir el ruido y los puntos aislados en la imagen binaria imgThreshold, se aplica un filtro de mediana con un tamaño de kernel de 5x5, lo que produce la imagen filtrada imgMedian.
Por último, para mejorar la detección de los vehículos, se utiliza la función dilate de OpenCV para dilatar las regiones blancas en la imagen filtrada imgMedian. Se utiliza un kernel de 3x3
y se realiza una iteración de dilatación para engrosar las regiones blancas de la imagen y hacer que los vehículos sean más reconocibles. El resultado de esta operación se guarda en la variable imgDilate.
"""