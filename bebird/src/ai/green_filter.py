import cv2
import numpy as np

class GreenFilterEngine:
    def __init__(self):
        # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        # Digunakan untuk naikkan kontras salur darah (micro-vasculature) tanpa over-exposure
        self.clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))

    def apply_filter(self, frame, mode='clahe_gray'):
        """
        Gunakan Digital Green Filter (DGF) pada bingkai imej.
        Hemoglobin dalam darah menyerap cahaya hijau, jadi salur darah akan nampak lebih gelap dan jelas.
        """
        # Ekstrak channel (B, G, R)
        b, g, r = cv2.split(frame)

        if mode == 'pure_green':
            # Hanya biarkan channel hijau, R dan B jadi kosong (hitam)
            return cv2.merge([np.zeros_like(b), g, np.zeros_like(r)])
            
        elif mode == 'clahe_gray':
            # Tingkatkan kontras pada channel hijau, dan jadikannya format grayscale 3-channel (paling ideal untuk klinikal)
            enhanced_g = self.clahe.apply(g)
            return cv2.merge([enhanced_g, enhanced_g, enhanced_g])
            
        elif mode == 'pseudo_color':
            # Campuran: Channel hijau ditingkatkan kontras, dikekalkan bersama B dan R yang digelapkan
            enhanced_g = self.clahe.apply(g)
            return cv2.merge([b // 2, enhanced_g, r // 2])
            
        else:
            return frame
