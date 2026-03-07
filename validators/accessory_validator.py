import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh


def validate_accessories(image_path):

    image = cv2.imread(image_path)
    if image is None:
        return True, []

    h, w, _ = image.shape
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    reasons = []

    # ─────────────────────────────────────────
    # WATERMARK / TEXT DETECTION
    # ─────────────────────────────────────────

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # only bottom corners
    br = gray[int(h*0.70):h, int(w*0.70):w]
    bl = gray[int(h*0.70):h, 0:int(w*0.30)]

    def watermark_score(region):

        if region.size == 0:
            return 0

        region = cv2.GaussianBlur(region,(5,5),0)

        edges = cv2.Canny(region,60,150)

        return np.sum(edges>0)/edges.size

    score = max(watermark_score(br), watermark_score(bl))

    if score > 0.22:
        reasons.append("Watermark or text overlay detected on image")

    # ─────────────────────────────────────────
    # FACE LANDMARK ANALYSIS
    # ─────────────────────────────────────────

    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True
    ) as face_mesh:

        results = face_mesh.process(image_rgb)

        if not results.multi_face_landmarks:
            return False, ["Face not detected"]

        landmarks = results.multi_face_landmarks[0].landmark

        def lm(i):
            p = landmarks[i]
            return int(p.x*w), int(p.y*h)

        forehead = lm(10)
        left_temple = lm(234)
        right_temple = lm(454)

        temple_width = abs(right_temple[0]-left_temple[0])

        # ─────────────────────────────────────────
        # HAT DETECTION
        # ─────────────────────────────────────────

        hat_y1 = max(0,forehead[1]-int(temple_width*1.2))
        hat_y2 = forehead[1]

        hat_x1 = max(0,left_temple[0]-10)
        hat_x2 = min(w,right_temple[0]+10)

        region = image[hat_y1:hat_y2,hat_x1:hat_x2]

        if region.size>0:

            std = np.mean(np.std(region.reshape(-1,3),axis=0))

            if std < 35:
                reasons.append("Hat or head covering detected")

        # ─────────────────────────────────────────
        # SUNGLASSES DETECTION
        # ─────────────────────────────────────────

        left_eye = lm(468)
        right_eye = lm(473)

        def eye_region(pt):

            x,y = pt
            r=20

            area = image[max(0,y-r):min(h,y+r),
                         max(0,x-r):min(w,x+r)]

            if area.size==0:
                return 255,50

            g=cv2.cvtColor(area,cv2.COLOR_BGR2GRAY)

            return np.mean(g), np.std(g)

        l_mean,l_std = eye_region(left_eye)
        r_mean,r_std = eye_region(right_eye)

        if (l_mean+r_mean)/2 < 60 and (l_std+r_std)/2 < 20:
            reasons.append("Sunglasses detected")

        # ─────────────────────────────────────────
        # MASK DETECTION
        # ─────────────────────────────────────────

        nose = lm(1)
        chin = lm(152)

        mask_region = image[nose[1]:chin[1], left_temple[0]:right_temple[0]]

        if mask_region.size>0:

            std = np.mean(np.std(mask_region.reshape(-1,3),axis=0))

            if std < 20:
                reasons.append("Face mask detected")

    if reasons:
        return False, reasons

    return True, []