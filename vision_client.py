import os
import requests
import json
# headers = {"Authorization": "Token 2b053891116b497b306bb9bcd580647bfa35f7ff"}
headers = {"Authorization": "Token 09873efa52b0b530961527ced5050b9afe493255"}
url = 'http://127.0.0.1:8000/object/'
# url = 'http://api.civilcops.com:8000/object/'
# with open('/home/abhishek/Documents/Civilcops/Object_detection/potholes2.jpg','rb') as img_file:
#     body = {'image':img_file}
#     response = requests.post(url,files=body)
#     print(response.status_code)
#     print(response.text)

# urls = ['https://ichef.bbci.co.uk/news/660/cpsprodpb/129DB/production/_104615267_9faf0b8c-02ef-4634-81b8-0d2d847439d0.jpg',
#         'https://scx1.b-cdn.net/csz/news/800/2018/potholeshowe.jpg',
#         'https://tatainnoverse.com/public/challangeImages/potholes.jpg',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRPjFBxR6lh1B4lvJiDnxq9NzxlKTyye4un3V4tmjyVKrgS5_OJdA&s',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6r4gn2ReBF3hIvVqmVW566k0bh-QE4mSvjxlPT-9LU0fOLd9V&s',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ3HGtEHmR1puQHF4hJveHR7O_e2P0brkc2dUPxPpPR9JSVS8_p&s',
#         'https://akm-img-a-in.tosshub.com/indiatoday/images/story/201909/pothole-770x433.png?tM4GjUaGXLtMVxnQg6wjpqViLLEczXHL',
#         'https://media.graytvinc.com/images/810*455/potholesPic.jpg',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSzN2Smzd-G4vwlAYElvq3eg6-35MukVZzodQHloXcsZ5uqP_1s&s',
#         'https://img.etimg.com/thumb/msid-65006748,width-640,resizemode-4,imgsize-271047/potholes-the-serial-killer-on-road.jpg',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRBF1SJbsUYZLPYjDEPWLJvezbIZk1fdT2ksR4u4IxBUhdCnYS2kA&s',
#         'https://static-news.moneycontrol.com/static-mcnews/2018/07/Potholes-770x433.jpg',
#         'https://mediaindia.eu/wp-content/uploads/2018/07/pothole.jpg',
#         'https://static.toiimg.com/thumb/69065524.cms?resizemode=4&width=400',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRyapYd7fK0-x87Pm-WV1leawYGAQHKcwRPYGz2rddA5AczDF77yQ&s',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS9AkWPVM5JCkhd-glyw8baT-R2PK5fEDw5d9L-ohMMdT7whYKN_A&s',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRClYMl_Ri0oYGSyF9R_8sFjPrVawpDOaqpAX5tpD68Ep0bVjvNlw&s',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTV1y7k986CtTnWrt41uaaGDaaSgq7xPeNLvbrKX5EnOi4DxOfJVQ&s',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQHFcwRlvm0bCOzBH0jXEwCCCqdFbRVTV6nR5oYW7WGF-0YwgyEcA&s',
#         'https://bloximages.chicago2.vip.townnews.com/kansan.com/content/tncms/assets/v3/editorial/1/03/10394616-3de6-11e9-8079-b3cfc30d2329/5c7c236186b56.image.jpg',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfH8z1CCx5IITsYl06OKYua1nQ0z-mu0BvI6mdjpRDrMm2ePDn&s',
#         'https://ichef.bbci.co.uk/news/660/cpsprodpb/129DB/production/_104615267_9faf0b8c-02ef-4634-81b8-0d2d847439d0.jpg',
#         'https://scx1.b-cdn.net/csz/news/800/2018/potholeshowe.jpg',
#         'https://tatainnoverse.com/public/challangeImages/potholes.jpg',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRPjFBxR6lh1B4lvJiDnxq9NzxlKTyye4un3V4tmjyVKrgS5_OJdA&s',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6r4gn2ReBF3hIvVqmVW566k0bh-QE4mSvjxlPT-9LU0fOLd9V&s',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ3HGtEHmR1puQHF4hJveHR7O_e2P0brkc2dUPxPpPR9JSVS8_p&s',
#         'https://akm-img-a-in.tosshub.com/indiatoday/images/story/201909/pothole-770x433.png?tM4GjUaGXLtMVxnQg6wjpqViLLEczXHL',
#         'https://media.graytvinc.com/images/810*455/potholesPic.jpg',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSzN2Smzd-G4vwlAYElvq3eg6-35MukVZzodQHloXcsZ5uqP_1s&s',
#         'https://img.etimg.com/thumb/msid-65006748,width-640,resizemode-4,imgsize-271047/potholes-the-serial-killer-on-road.jpg',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRBF1SJbsUYZLPYjDEPWLJvezbIZk1fdT2ksR4u4IxBUhdCnYS2kA&s',
#         'https://static-news.moneycontrol.com/static-mcnews/2018/07/Potholes-770x433.jpg',
#         'https://mediaindia.eu/wp-content/uploads/2018/07/pothole.jpg',
#         'https://static.toiimg.com/thumb/69065524.cms?resizemode=4&width=400',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRyapYd7fK0-x87Pm-WV1leawYGAQHKcwRPYGz2rddA5AczDF77yQ&s',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS9AkWPVM5JCkhd-glyw8baT-R2PK5fEDw5d9L-ohMMdT7whYKN_A&s',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRClYMl_Ri0oYGSyF9R_8sFjPrVawpDOaqpAX5tpD68Ep0bVjvNlw&s',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTV1y7k986CtTnWrt41uaaGDaaSgq7xPeNLvbrKX5EnOi4DxOfJVQ&s',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQHFcwRlvm0bCOzBH0jXEwCCCqdFbRVTV6nR5oYW7WGF-0YwgyEcA&s',
#         'https://bloximages.chicago2.vip.townnews.com/kansan.com/content/tncms/assets/v3/editorial/1/03/10394616-3de6-11e9-8079-b3cfc30d2329/5c7c236186b56.image.jpg',
#         'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfH8z1CCx5IITsYl06OKYua1nQ0z-mu0BvI6mdjpRDrMm2ePDn&s',
#         ]

raw_data = {}
raw_data['iurl'] = '/home/abhishek/Documents/Civilcops/Object_detection/YOLO-DARKNET/annotation/image class/dataset/468.jpg'
# for i in urls:
#     raw_data.update({'image_url':str(i)})
response = requests.post(url, data=json.dumps(raw_data),headers=headers)
print(response.status_code)
print(response.text)
print(response.headers)

# print(type(raw_data['url']))