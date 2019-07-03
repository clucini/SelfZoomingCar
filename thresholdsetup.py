import components.seeforward as camera
import cv2

b_lower = (150, 60, 60)
b_upper = (190,255,255)


y_lower = (15, 150, 50)
y_upper = (30,255,255)

def reciever(helper):
    image = helper['image']
    global y_lower, y_upper, b_lower, b_upper
    cv2.imshow("Color", image)

    y_mask = cv2.inRange(hsv, y_lower, y_upper)
    b_mask = cv2.inRange(hsv, b_lower, b_upper)

    cv2.imshow("y_mask", y_mask)
    cv2.imshow("b_mask", b_mask)
    cv2.waitKey(1)
    c = input("Yellow (y) or Blue (b): ")
    if not c.lower() in ['y', 'b']:
        print("Invalid Colour, no changes made.")
        return

    b = input("Upper (u) or Lower (l): ")
    if not b.lower() in ['u', 'l']:
        print("Invalid Boundary, no changes made.")
        return
    
    s = input("Hue, Saturation, Value: ")
    ss = s.split(',')
    if len(ss) != 3:
        print("Invalid values, enter as displayed.")
        return

    ss[0] = int(ss[0])
    ss[1] = int(ss[1])
    ss[2] = int(ss[2])

    if c == 'y':
        if b == 'u':
            y_upper = (ss[0], ss[1], ss[2])
            print("y_upper changed to: ", ss)
        else:
            y_lower = (ss[0], ss[1], ss[2])
            print("y_lower changed to: ", ss)
    else:
        if b == 'u':
            b_upper = (ss[0], ss[1], ss[2])
            print("b_upper changed to: ", ss)
        else:
            b_lower = (ss[0], ss[1], ss[2])
            print("b_lower changed to: ", ss)


    



camera.sendImageTo(reciever)

# Start the program
camera.start()