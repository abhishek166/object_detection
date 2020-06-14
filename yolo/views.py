import time
import cv2
import os
import logging
import numpy as np
import tensorflow as tf
from .yolov3_tf2.models import YoloV3
from .yolov3_tf2.dataset import transform_images
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
import json
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from io import BytesIO
from PIL import Image
import urllib
import requests
from django.conf import settings

yolo = YoloV3(classes=2)
yolo.load_weights('/home/abhishek/Documents/Civilcops/Civilcops_object_detection/object_detection/yolo/checkpoints/yolov3.tf')
logging.basicConfig(filename='/home/abhishek/Documents/Civilcops/Civilcops_object_detection/object_detection/logs/debug.log',
                        filemode='a',
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)
logging.info('weights loaded')
# Create your views here.

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def download(request, image):
    path1 = '/home/abhishek/Documents/Civilcops/Civilcops_object_detection/object_detection/images/'+image.split('/')[-1]
    print(path1)
    with open(path1, 'rb') as f:
        return HttpResponse(f.read(), content_type="image/jpeg")


@api_view(["POST"])
@permission_classes((IsAuthenticated, ))
def test(request):
    physical_devices = tf.config.experimental.list_physical_devices('GPU')
    if len(physical_devices) > 0:
        tf.config.experimental.set_memory_growth(physical_devices[0], True)
    t1 = time.time()
    global yolo
    class_names = [c.strip() for c in open('/home/abhishek/Documents/Civilcops/Civilcops_object_detection/object_detection/yolo/complaints.names').readlines()]
    logging.info('classes loaded')
    image = json.loads(request.body.decode('utf-8'))
    logging.info('image url : {}'.format(image['image_url']))
    response = requests.get(image['image_url'])
    content_type = response.headers['content-type']
    print(content_type)
    logging.info('image type:{}'.format(content_type))
    dict = {}
    Invalid = 9
    if content_type in ['image/jpeg','image/png','image/jpg','image/webp']:
        im = response.content
        img = tf.image.decode_image(im, channels=3)
        img = tf.expand_dims(img, 0)
        img = transform_images(img, 416)
        boxes, scores, classes, nums = yolo(img)
        for i in range(nums[0]):
            print(i)
        t2 = time.time()
        logging.info('prediction time : {} sec.'.format(t2-t1))

        ### Image compression and storing ###
        image_time = time.time()
        img1 = Image.open(BytesIO(im))
        im_name = 'harpath' + str(image_time) + '.jpeg'
        image_path = '/home/abhishek/Documents/Civilcops/Civilcops_object_detection/object_detection/images/' + im_name
        img1.save(image_path, format='JPEG')
        size = os.path.getsize(image_path) / 1000
        if (size < 256):
            image_path_send = 'http://127.0.0.1:8000/object/download/' + im_name
            # img_base64 = base64.encodebytes(im)
        else:
            img2 = Image.open(BytesIO(im))
            im_name = 'harpath_compressed' + str(image_time) + '.jpeg'
            compressed_image_path = '/home/abhishek/Documents/Civilcops/Civilcops_object_detection/object_detection/images/' + im_name
            img2.save(compressed_image_path, format='JPEG', quality=10, optimize=True)
            image_path_send = 'http://127.0.0.1:8000/object/download/' + im_name
            # with open(compressed_image_path,'rb') as image_file:
            # img_base64 = base64.encodebytes(image_file.read())
        logging.info('compression, storing time : {} sec.'.format(time.time() - image_time))
        dict['image_url'] = image_path_send
        Pothole = 0
        Damaged = 6
        pothole_count =0
        damaged_road_count = 0
        pothole_confidence = []
        damaged_confidence = []
        for i in range(nums[0]):
            logging.info('object_class : {}, confidence_score : {}, boundary_box : {}'
                         .format(class_names[int(classes[0][i])],
                                 np.array(scores[0][i]),
                                 np.array(boxes[0][i])))
            name = class_names[int(classes[0][i])]
            # print(name)
            if(name=='pothole'):
                pothole_count = pothole_count + 1
                pothole_confidence.append(scores[0][i])
            elif(name=='damaged road'):
                damaged_road_count = damaged_road_count + 1
                damaged_confidence.append(scores[0][i])
        if (damaged_road_count > 1):
            logging.info('Damaged Road')
            dict['category'] = Damaged
            return Response(dict)
        elif (damaged_road_count==1):
            if (pothole_count>2):
                logging.info('{} count : {}'.format(class_names[0], pothole_count))
                dict['category'] = Damaged
                return Response(dict)
            elif (pothole_count==1):
                if(pothole_confidence[0]>damaged_confidence[0]):
                    logging.info('{} count : {}'.format(class_names[0], pothole_count))
                    dict['category'] = Pothole
                    return Response(dict)
                else:
                    logging.info('Damaged Road')
                    dict['category'] = Damaged
                    return Response(dict)
            elif (pothole_count==2):
                logging.info('{} count : {}'.format(class_names[0], pothole_count))
                dict['category'] = Pothole
                return Response(dict)
            else:
                logging.info('Damaged Road')
                dict['category'] = Damaged
                return Response(dict)
        elif (damaged_road_count==0):
            if (pothole_count>2):
                logging.info('{} count : {}'.format(class_names[0], pothole_count))
                dict['category'] = Damaged
                return Response(dict)
            elif pothole_count in range(1, 3):
                logging.info('{} count : {}'.format(class_names[0], pothole_count))
                dict['category'] = Pothole
                return Response(dict)
            else:
                logging.info('No {} or {} found'.format(class_names[0],class_names[1]))
                dict['category'] = Invalid
                return Response(dict)
    else:
        dict['category'] = Invalid
        logging.info('Invalid Format')
        return Response(dict)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)
