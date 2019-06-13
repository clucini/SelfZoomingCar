import math
import time
import cv2
import numpy as np
import pyrealsense2 as rs

state={
    "decimate": 1,
    "pitch":-0.9,
    "yaw":0,
    "translation":np.array([0, 0, -0.3], dtype=np.float32),
    "distance":2,
    "scale":True,
    "color":True

}

func_to_send_to = None

def sendImageTo(func):
    global func_to_send_to
    func_to_send_to = func

def rotation():
    Rx, _ = cv2.Rodrigues((state["pitch"], 0, 0))
    Ry, _ = cv2.Rodrigues((0, state["yaw"], 0))
    return np.dot(Ry, Rx).astype(np.float32)

def pivot():
    return state["translation"] + np.array((0, 0, state["distance"]), dtype=np.float32)

def start():

    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Start streaming
    pipeline.start(config)

    # Get stream profile and camera intrinsics
    profile = pipeline.get_active_profile()
    depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
    depth_intrinsics = depth_profile.get_intrinsics()
    w, h = depth_intrinsics.width, depth_intrinsics.height

    # Processing blocks
    pc = rs.pointcloud()
    decimate = rs.decimation_filter()
    decimate.set_option(rs.option.filter_magnitude, 2 ** state["decimate"])
    colorizer = rs.colorizer()

    def project(v):
        """project 3d vector array to 2d"""
        h, w = out.shape[:2]
        view_aspect = float(h)/w

        # ignore divide by zero for invalid depth
        with np.errstate(divide='ignore', invalid='ignore'):
            proj = v[:, :-1] / v[:, -1, np.newaxis] * \
                (w*view_aspect, h) + (w/2.0, h/2.0)

        # near clipping
        znear = 0.03
        proj[v[:, 2] < znear] = np.nan
        return proj


    def view(v):
        """apply view transformation on vector array"""
        return np.dot(v - pivot(), rotation()) + pivot() - state["translation"]


    def pointcloud(out, verts, texcoords, color, painter=True):
        """draw point cloud with optional painter's algorithm"""
        if painter:
            # Painter's algo, sort points from back to front

            # get reverse sorted indices by z (in view-space)
            # https://gist.github.com/stevenvo/e3dad127598842459b68
            v = view(verts)
            s = v[:, 2].argsort()[::-1]
            proj = project(v[s])
        else:
            proj = project(view(verts))

        if state["scale"]:
            proj *= 0.5**state["decimate"]

        h, w = out.shape[:2]

        # proj now contains 2d image coordinates
        j, i = proj.astype(np.uint32).T

        # create a mask to ignore out-of-bound indices
        im = (i >= 0) & (i < h)
        jm = (j >= 0) & (j < w)
        m = im & jm

        cw, ch = color.shape[:2][::-1]
        if painter:
            # sort texcoord with same indices as above
            # texcoords are [0..1] and relative to top-left pixel corner,
            # multiply by size and add 0.5 to center
            v, u = (texcoords[s] * (cw, ch) + 0.5).astype(np.uint32).T
        else:
            v, u = (texcoords * (cw, ch) + 0.5).astype(np.uint32).T
        # clip texcoords to image
        np.clip(u, 0, ch-1, out=u)
        np.clip(v, 0, cw-1, out=v)

        # perform uv-mapping
        out[i[m], j[m]] = color[u[m], v[m]]


    out = np.empty((h, w, 3), dtype=np.uint8)

    while True:
        # Grab camera data
        
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()

        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        depth_frame = decimate.process(depth_frame)

        # Grab new intrinsics (may be changed by decimation)
        depth_intrinsics = rs.video_stream_profile(
            depth_frame.profile).get_intrinsics()
        w, h = depth_intrinsics.width, depth_intrinsics.height

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        cv2.imshow("col",color_image)
        depth_colormap = np.asanyarray(
            colorizer.colorize(depth_frame).get_data())

        if state["color"]:
            mapped_frame, color_source = color_frame, color_image
        else:
            mapped_frame, color_source = depth_frame, depth_colormap

        points = pc.calculate(depth_frame)
        pc.map_to(mapped_frame)

        # Pointcloud data to arrays
        v, t = points.get_vertices(), points.get_texture_coordinates()
        verts = np.asanyarray(v).view(np.float32).reshape(-1, 3)  # xyz
        texcoords = np.asanyarray(t).view(np.float32).reshape(-1, 2)  # uv

        # Render
        now = time.time()

        out.fill(0)

        if not state["scale"] or out.shape[:2] == (h, w):
            pointcloud(out, verts, texcoords, color_source)
        else:
            tmp = np.zeros((h, w, 3), dtype=np.uint8)
            pointcloud(tmp, verts, texcoords, color_source)
            tmp = cv2.resize(
                tmp, out.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)
            np.putmask(out, tmp > 0, tmp)


        dt = time.time() - now
        # convert out to grayscale
        """
        flatout=np.copy(out)
        mask=np.zeros((flatout.shape[0]+2,flatout.shape[1]+2), np.uint8)
        # contour detect absolute black and remove large contours
        cv2.floodFill(flatout, mask, (0,flatout.shape[0]-1),(255,255,255)); 
        flatmask=(flatout==(0,0,0))[:,:,0].astype('uint8')
        """
        kernel = np.ones((3,3),np.uint8)
        out = cv2.dilate(out,kernel,iterations=2)
        #
        # out = cv2.boxFilter(out,mask,3,cv2.INPAINT_TELEA)
        # finish inpaint
        func_to_send_to(out)

        cv2.imshow("rs", out)
        key = cv2.waitKey(1)


        if key in (27, ord("q")):
            break
    # Stop streaming
    pipeline.stop()