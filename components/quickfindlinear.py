def find_overlaps(y_contours, b_contours):
    y_contours.sort(key = lambda x:x[1])
    b_contours.sort(key = lambda x:x[1])

    y_counter = 0
    b_counter = 0

    pairs = []

    for i in range(0, len(y_contours)):
        lastdiff = 100000
        f = 0
        while abs(y_contours[i][1] - b_contours[f][1]) <= lastdiff:
            # print(b_contours[f])
            lastdiff = abs(y_contours[i][1] - b_contours[f][1])
            # print(lastdiff)
            f += 1
            if f >= len(b_contours):
                break
        pairs.append((y_contours[i],b_contours[f-1]))

    return pairs        


y_test = [[300, 20],[300,10],[300,50],[300,40],[300,30]]
b_test = [[400, 15],[400,30]]

find_overlaps(y_test, b_test)