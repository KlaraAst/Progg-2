import matplotlib.pyplot as plt
from PIL import Image

'''
Customer at each point:

0. Distribution substation with the 11/0.4 kV transformer = red

1. Tegel bruket: garage with car painting workshop = blue

2. 2 single-family houses = green

3. 7 single-family houses 

4. 15 single-family houses and a Car service shop (Mattias Rekond) --> Car Service = pink

5. Farmstead = yellow

6. Farmstead and 5 single-family houses.

7. 9 single-family houses.

8. Small carpinter workshop (Staffans Snickeri AB) and 8 Single-family houses --> Small carpinter workshop = black

9. Small church and 7 single-family houses --> Small church = white

10. 10 single-family houses.

11. Business Park (offices for 6 companies) and a gym (Knivsta PADEL & fys) --> Buiness Park = purple, gym = light blue

12. 1000m of LED streetlights. Divide the load into two sections connected to one phase each = orange

'''




im = plt.imread('Marma.png')
implot = plt.imshow(im)


im_height, im_width, im_channel = im.shape


# display width and height
print("The height of the image is: ", im_height)
print("The width of the image is: ", im_width)


# 0


# 1


# 2


# 3


# 4




#%%

# put a red dot, size 40, at 2 locations:

#plt.scatter(x=[300, 400], y=[450, 500], c='r', s=20)   # s = size of dots

plt.show()


