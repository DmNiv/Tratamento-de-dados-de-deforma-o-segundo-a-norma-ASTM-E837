## AUTOMATIZAÇÃO E CRIAÇÃO DE INTERFACE PARA CÁLCULOS DA NORMA ASTM E-837 13
## Trabalho de Conclusão de curso - Lucas Franco Brito
## Msc. Sério Custódio


import xlrd
import numpy as np
import tkinter as tk
from tkinter import ttk
from scipy.interpolate import interp1d
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import math
from math import sqrt
from math import pi
from math import atan


def calcular_tensoes_uniformes():
    modulo_elasticidade = float(entrada_modulo.get())
    poisson = float(entrada_poisson.get())
    diametro_furo = (entrada_diametro.get())
    tipo_roseta = entrada_roseta.get()
    arquivo = entrada_arquivo.get()

    calculo_uniforme(modulo_elasticidade, poisson, diametro_furo, tipo_roseta, arquivo)


def calcular_tensoes_nao_uniformes():
    modulo_elasticidade = float(entrada_modulo.get())
    poisson = float(entrada_poisson.get())
    diametro_furo = float(entrada_diametro.get())
    tipo_roseta = entrada_roseta.get()
    arquivo = entrada_arquivo.get()

    calculo_n_uniforme(modulo_elasticidade, poisson, diametro_furo, tipo_roseta, arquivo)


def calculo_n_uniforme(modulo_elasticidade, poisson, diametro_furo, tipo_roseta, arquivo):
    ## Inputs
    E = modulo_elasticidade;  # TPa - 0.205
    v = poisson;  # Poisson - 0.3
    hole_diameter = diametro_furo;  # mm - 0.0625
    Rosete_Type = tipo_roseta;  # 1=A, 2=B, 3=C
    filename = arquivo;  # dados_novo.txt

    ## 10.1 Strain Data
    straindata_load = np.loadtxt(filename)

    straindata = np.zeros((20, 4))
    straindata[:, 0] = np.arange(0.05, 1.05, 0.05)
    straindata[:, 1] = interp1d(straindata_load[:, 0], straindata_load[:, 1], kind='cubic', fill_value="extrapolate")(
        straindata[:, 0])
    straindata[:, 2] = interp1d(straindata_load[:, 0], straindata_load[:, 2], kind='cubic', fill_value="extrapolate")(
        straindata[:, 0])
    straindata[:, 3] = interp1d(straindata_load[:, 0], straindata_load[:, 3], kind='cubic', fill_value="extrapolate")(
        straindata[:, 0])

    p = (straindata[:, 3] + straindata[:, 1]) / 2
    q = (straindata[:, 3] - straindata[:, 1]) / 2
    t = (straindata[:, 3] + straindata[:, 1] - 2 * straindata[:, 2]) / 2

    p_std2 = 0
    q_std2 = 0
    t_std2 = 0

    for j in range(straindata.shape[0] - 3):
        p_std2 += ((p[j] - 3 * p[j + 1] + 3 * p[j + 2] - p[j + 3]) ** 2) / (20 * (straindata.shape[0] - 3))
        q_std2 += ((q[j] - 3 * q[j + 1] + 3 * q[j + 2] - q[j + 3]) ** 2) / (20 * (straindata.shape[0] - 3))
        t_std2 += ((t[j] - 3 * t[j + 1] + 3 * t[j + 2] - t[j + 3]) ** 2) / (20 * (straindata.shape[0] - 3))

    # Type A
    if Rosete_Type == '1':
        matrix_a = np.array([
            [-0.00679, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.00815, -0.00714, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.00937, -0.00844, -0.00734, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01046, -0.00960, -0.00858, -0.00739, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01141, -0.01063, -0.00968, -0.00856, -0.00728, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01223, -0.01152, -0.01064, -0.00960, -0.00839, -0.00701, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01291, -0.01227, -0.01147, -0.01050, -0.00936, -0.00806, -0.00659, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0],
            [-0.01360, -0.01287, -0.01207, -0.01132, -0.01015, -0.00893, -0.00759, -0.00615, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0],
            [-0.01416, -0.01344, -0.01264, -0.01184, -0.01082, -0.00970, -0.00846, -0.00712, -0.00567, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0],
            [-0.01463, -0.01392, -0.01312, -0.01223, -0.01134, -0.01031, -0.00917, -0.00793, -0.00657, -0.00511, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01508, -0.01434, -0.01354, -0.01270, -0.01173, -0.01072, -0.00977, -0.00854, -0.00730, -0.00600,
             -0.00464, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01545, -0.01471, -0.01391, -0.01306, -0.01211, -0.01113, -0.01013, -0.00906, -0.00791, -0.00670,
             -0.00543, -0.00411, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01578, -0.01503, -0.01422, -0.01340, -0.01243, -0.01146, -0.01049, -0.00938, -0.00842, -0.00722,
             -0.00604, -0.00485, -0.00364, 0, 0, 0, 0, 0, 0, 0],
            [-0.01606, -0.01531, -0.01450, -0.01366, -0.01271, -0.01175, -0.01078, -0.00970, -0.00869, -0.00765,
             -0.00655, -0.00544, -0.00431, -0.00316, 0, 0, 0, 0, 0, 0],
            [-0.01629, -0.01554, -0.01473, -0.01390, -0.01294, -0.01199, -0.01102, -0.00996, -0.00892, -0.00795,
             -0.00693, -0.00589, -0.00484, -0.00378, -0.00270, 0, 0, 0, 0, 0],
            [-0.01649, -0.01574, -0.01493, -0.01410, -0.01313, -0.01217, -0.01123, -0.01018, -0.00919, -0.00815,
             -0.00716, -0.00624, -0.00524, -0.00425, -0.00328, -0.00231, 0, 0, 0, 0],
            [-0.01665, -0.01590, -0.01510, -0.01426, -0.01330, -0.01234, -0.01138, -0.01036, -0.00938, -0.00836,
             -0.00738, -0.00644, -0.00555, -0.00464, -0.00373, -0.00283, -0.00195, 0, 0, 0],
            [-0.01679, -0.01604, -0.01523, -0.01441, -0.01344, -0.01248, -0.01151, -0.01049, -0.00955, -0.00852,
             -0.00755, -0.00665, -0.00574, -0.00492, -0.00406, -0.00323, -0.00241, -0.00162, 0, 0],
            [-0.01692, -0.01617, -0.01536, -0.01452, -0.01357, -0.01261, -0.01164, -0.01063, -0.00967, -0.00866,
             -0.00770, -0.00679, -0.00592, -0.00508, -0.00432, -0.00353, -0.00277, -0.00203, -0.00131, 0],
            [-0.01704, -0.01628, -0.01548, -0.01465, -0.01368, -0.01272, -0.01176, -0.01074, -0.00978, -0.00877,
             -0.00781, -0.00690, -0.00605, -0.00521, -0.00448, -0.00374, -0.00303, -0.00234, -0.00167, -0.00103]
        ])

        matrix_b = np.array([
            [-0.01264, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01470, -0.01352, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01656, -0.01554, -0.01414, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01821, -0.01735, -0.01611, -0.01449, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01967, -0.01897, -0.01789, -0.01642, -0.01458, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.02092, -0.02038, -0.01946, -0.01815, -0.01647, -0.01439, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.02197, -0.02159, -0.02083, -0.01968, -0.01815, -0.01624, -0.01395, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0],
            [-0.02308, -0.02256, -0.02182, -0.02112, -0.01952, -0.01778, -0.01576, -0.01348, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0],
            [-0.02400, -0.02351, -0.02280, -0.02202, -0.02072, -0.01917, -0.01735, -0.01525, -0.01289, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0],
            [-0.02481, -0.02434, -0.02366, -0.02273, -0.02167, -0.02031, -0.01868, -0.01678, -0.01460, -0.01216, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0],
            [-0.02554, -0.02507, -0.02440, -0.02362, -0.02235, -0.02103, -0.01981, -0.01793, -0.01599, -0.01386,
             -0.01156, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.02616, -0.02571, -0.02505, -0.02428, -0.02305, -0.02177, -0.02045, -0.01890, -0.01715, -0.01522,
             -0.01310, -0.01081, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.02668, -0.02625, -0.02561, -0.02487, -0.02364, -0.02239, -0.02109, -0.01949, -0.01813, -0.01623,
             -0.01430, -0.01226, -0.01013, 0, 0, 0, 0, 0, 0, 0],
            [-0.02715, -0.02673, -0.02611, -0.02536, -0.02417, -0.02294, -0.02164, -0.02012, -0.01866, -0.01708,
             -0.01531, -0.01345, -0.01149, -0.00944, 0, 0, 0, 0, 0, 0],
            [-0.02753, -0.02713, -0.02653, -0.02582, -0.02463, -0.02341, -0.02213, -0.02064, -0.01911, -0.01767,
             -0.01608, -0.01439, -0.01260, -0.01073, -0.00875, 0, 0, 0, 0, 0],
            [-0.02789, -0.02749, -0.02690, -0.02620, -0.02502, -0.02382, -0.02256, -0.02108, -0.01968, -0.01807,
             -0.01652, -0.01511, -0.01344, -0.01172, -0.00995, -0.00812, 0, 0, 0, 0],
            [-0.02821, -0.02781, -0.02722, -0.02652, -0.02536, -0.02417, -0.02292, -0.02146, -0.02007, -0.01850,
             -0.01698, -0.01549, -0.01408, -0.01251, -0.01089, -0.00921, -0.00747, 0, 0, 0],
            [-0.02848, -0.02809, -0.02750, -0.02682, -0.02565, -0.02447, -0.02324, -0.02176, -0.02041, -0.01885,
             -0.01736, -0.01590, -0.01441, -0.01312, -0.011591, -0.01004, -0.00847, -0.00688, 0, 0],
            [-0.02871, -0.02832, -0.02774, -0.02706, -0.02591, -0.02473, -0.02350, -0.02204, -0.02067, -0.01916,
             -0.01769, -0.01624, -0.01480, -0.01340, -0.01213, -0.01072, -0.00928, -0.00781, -0.00632, 0],
            [-0.02889, -0.02851, -0.02794, -0.02727, -0.02612, -0.02495, -0.02373, -0.02227, -0.02089, -0.01940,
             -0.01796, -0.01655, -0.01511, -0.01367, -0.01249, -0.01121, -0.00989, -0.00856, -0.00719, -0.00581]
        ])

    # Type B
    if Rosete_Type == '2':
        matrix_a = np.array([
            [-0.00726, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.00878, -0.00766, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01013, -0.00909, -0.00788, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01133, -0.01037, -0.00924, -0.00793, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01237, -0.01149, -0.01043, -0.00921, -0.00781, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01325, -0.01245, -0.01147, -0.01033, -0.00901, -0.00751, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01397, -0.01325, -0.01235, -0.01129, -0.01004, -0.00863, -0.00704, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0],
            [-0.01471, -0.01388, -0.01297, -0.01214, -0.01088, -0.00956, -0.00811, -0.00654, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0],
            [-0.01533, -0.01450, -0.01360, -0.01268, -0.01161, -0.01039, -0.00904, -0.00758, -0.00599, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0],
            [-0.01587, -0.01504, -0.01414, -0.01313, -0.01217, -0.01105, -0.00981, -0.00845, -0.00696, -0.00536, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01634, -0.01550, -0.01460, -0.01367, -0.01257, -0.01147, -0.01046, -0.00909, -0.00774, -0.00633,
             -0.00486, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01672, -0.01589, -0.01500, -0.01406, -0.01299, -0.01190, -0.01082, -0.00964, -0.00839, -0.00708,
             -0.00572, -0.00430, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01705, -0.01621, -0.01532, -0.01441, -0.01332, -0.01225, -0.01118, -0.00997, -0.00892, -0.00764,
             -0.00637, -0.00509, -0.00379, 0, 0, 0, 0, 0, 0, 0],
            [-0.01735, -0.01651, -0.01561, -0.01468, -0.01362, -0.01255, -0.01148, -0.01031, -0.00921, -0.00810,
             -0.00691, -0.00571, -0.00450, -0.00327, 0, 0, 0, 0, 0, 0],
            [-0.01759, -0.01675, -0.01586, -0.01493, -0.01387, -0.01280, -0.01174, -0.01059, -0.00945, -0.00840,
             -0.00730, -0.00619, -0.00506, -0.00392, -0.00277, 0, 0, 0, 0, 0],
            [-0.01781, -0.01697, -0.01607, -0.01515, -0.01408, -0.01302, -0.01196, -0.01080, -0.00974, -0.00860,
             -0.00753, -0.00655, -0.00549, -0.00443, -0.00339, -0.00234, 0, 0, 0, 0],
            [-0.01799, -0.01715, -0.01625, -0.01533, -0.01426, -0.01320, -0.01213, -0.01099, -0.00992, -0.00881,
             -0.00775, -0.00674, -0.00581, -0.00484, -0.00387, -0.00291, -0.00195, 0, 0, 0],
            [-0.01814, -0.01730, -0.01640, -0.01550, -0.01441, -0.01334, -0.01229, -0.01114, -0.01008, -0.00897,
             -0.00793, -0.00695, -0.00598, -0.00514, -0.00423, -0.00333, -0.00246, -0.00162, 0, 0],
            [-0.01829, -0.01744, -0.01654, -0.01561, -0.01454, -0.01347, -0.01242, -0.01129, -0.01021, -0.00912,
             -0.00809, -0.00710, -0.00617, -0.00528, -0.00449, -0.00366, -0.00285, -0.00207, -0.00131, 0],
            [-0.01843, -0.01757, -0.01666, -0.01573, -0.01465, -0.01358, -0.01253, -0.01140, -0.01035, -0.00925,
             -0.00822, -0.00724, -0.00632, -0.00541, -0.00466, -0.00389, -0.00314, -0.00242, -0.00172, -0.00104]
        ])

        matrix_b = np.array([
            [-0.01417, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01470, -0.01352, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01656, -0.01554, -0.01414, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01821, -0.01735, -0.01611, -0.01449, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01967, -0.01897, -0.01789, -0.01642, -0.01458, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.02092, -0.02038, -0.01946, -0.01815, -0.01647, -0.01439, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.02197, -0.02159, -0.02083, -0.01968, -0.01815, -0.01624, -0.01395, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0],
            [-0.02308, -0.02256, -0.02182, -0.02112, -0.01952, -0.01778, -0.01576, -0.01348, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0],
            [-0.02400, -0.02351, -0.02280, -0.02202, -0.02072, -0.01917, -0.01735, -0.01525, -0.01289, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0],
            [-0.02481, -0.02434, -0.02366, -0.02273, -0.02167, -0.02031, -0.01868, -0.01678, -0.01460, -0.01216, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0],
            [-0.02554, -0.02507, -0.02440, -0.02362, -0.02235, -0.02103, -0.01981, -0.01793, -0.01599, -0.01386,
             -0.01156, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.02616, -0.02571, -0.02505, -0.02428, -0.02305, -0.02177, -0.02045, -0.01890, -0.01715, -0.01522,
             -0.01310, -0.01081, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.02668, -0.02625, -0.02561, -0.02487, -0.02364, -0.02239, -0.02109, -0.01949, -0.01813, -0.01623,
             -0.01430, -0.01226, -0.01013, 0, 0, 0, 0, 0, 0, 0],
            [-0.02715, -0.02673, -0.02611, -0.02536, -0.02417, -0.02294, -0.02164, -0.02012, -0.01866, -0.01708,
             -0.01531, -0.01345, -0.01149, -0.00944, 0, 0, 0, 0, 0, 0],
            [-0.02753, -0.02713, -0.02653, -0.02582, -0.02463, -0.02341, -0.02213, -0.02064, -0.01911, -0.01767,
             -0.01608, -0.01439, -0.01260, -0.01073, -0.00875, 0, 0, 0, 0, 0],
            [-0.02789, -0.02749, -0.02690, -0.02620, -0.02502, -0.02382, -0.02256, -0.02108, -0.01968, -0.01807,
             -0.01652, -0.01511, -0.01344, -0.01172, -0.00995, -0.00812, 0, 0, 0, 0],
            [-0.02821, -0.02781, -0.02722, -0.02652, -0.02536, -0.02417, -0.02292, -0.02146, -0.02007, -0.01850,
             -0.01698, -0.01549, -0.01408, -0.01251, -0.01089, -0.00921, -0.00747, 0, 0, 0],
            [-0.02848, -0.02809, -0.02750, -0.02682, -0.02565, -0.02447, -0.02324, -0.02176, -0.02041, -0.01885,
             -0.01736, -0.01590, -0.01441, -0.01312, -0.011591, -0.01004, -0.00847, -0.00688, 0, 0],
            [-0.02871, -0.02832, -0.02774, -0.02706, -0.02591, -0.02473, -0.02350, -0.02204, -0.02067, -0.01916,
             -0.01769, -0.01624, -0.01480, -0.01340, -0.01213, -0.01072, -0.00928, -0.00781, -0.00632, 0],
            [-0.02889, -0.02851, -0.02794, -0.02727, -0.02612, -0.02495, -0.02373, -0.02227, -0.02089, -0.01940,
             -0.01796, -0.01655, -0.01511, -0.01367, -0.01249, -0.01121, -0.00989, -0.00856, -0.00719, -0.00581]
        ])

    # Type C
    if Rosete_Type == '3':
        matrix_a = np.array([
            [-0.00679, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.00815, -0.00714, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.00937, -0.00844, -0.00734, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01046, -0.00960, -0.00858, -0.00739, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01141, -0.01063, -0.00968, -0.00856, -0.00728, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01223, -0.01152, -0.01064, -0.00960, -0.00839, -0.00701, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01291, -0.01227, -0.01147, -0.01050, -0.00936, -0.00806, -0.00659, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0],
            [-0.01360, -0.01287, -0.01207, -0.01132, -0.01015, -0.00893, -0.00759, -0.00615, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0],
            [-0.01416, -0.01344, -0.01264, -0.01184, -0.01082, -0.00970, -0.00846, -0.00712, -0.00567, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0],
            [-0.01463, -0.01392, -0.01312, -0.01223, -0.01134, -0.01031, -0.00917, -0.00793, -0.00657, -0.00511, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01508, -0.01434, -0.01354, -0.01270, -0.01173, -0.01072, -0.00977, -0.00854, -0.00730, -0.00600,
             -0.00464, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01545, -0.01471, -0.01391, -0.01306, -0.01211, -0.01113, -0.01013, -0.00906, -0.00791, -0.00670,
             -0.00543, -0.00411, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01578, -0.01503, -0.01422, -0.01340, -0.01243, -0.01146, -0.01049, -0.00938, -0.00842, -0.00722,
             -0.00604, -0.00485, -0.00364, 0, 0, 0, 0, 0, 0, 0],
            [-0.01606, -0.01531, -0.01450, -0.01366, -0.01271, -0.01175, -0.01078, -0.00970, -0.00869, -0.00765,
             -0.00655, -0.00544, -0.00431, -0.00316, 0, 0, 0, 0, 0, 0],
            [-0.01629, -0.01554, -0.01473, -0.01390, -0.01294, -0.01199, -0.01102, -0.00996, -0.00892, -0.00795,
             -0.00693, -0.00589, -0.00484, -0.00378, -0.00270, 0, 0, 0, 0, 0],
            [-0.01649, -0.01574, -0.01493, -0.01410, -0.01313, -0.01217, -0.01123, -0.01018, -0.00919, -0.00815,
             -0.00716, -0.00624, -0.00524, -0.00425, -0.00328, -0.00231, 0, 0, 0, 0],
            [-0.01665, -0.01590, -0.01510, -0.01426, -0.01330, -0.01234, -0.01138, -0.01036, -0.00938, -0.00836,
             -0.00738, -0.00644, -0.00555, -0.00464, -0.00373, -0.00283, -0.00195, 0, 0, 0],
            [-0.01679, -0.01604, -0.01523, -0.01441, -0.01344, -0.01248, -0.01151, -0.01049, -0.00955, -0.00852,
             -0.00755, -0.00665, -0.00574, -0.00492, -0.00406, -0.00323, -0.00241, -0.00162, 0, 0],
            [-0.01692, -0.01617, -0.01536, -0.01452, -0.01357, -0.01261, -0.01164, -0.01063, -0.00967, -0.00866,
             -0.00770, -0.00679, -0.00592, -0.00508, -0.00432, -0.00353, -0.00277, -0.00203, -0.00131, 0],
            [-0.01704, -0.01628, -0.01548, -0.01465, -0.01368, -0.01272, -0.01176, -0.01074, -0.00978, -0.00877,
             -0.00781, -0.00690, -0.00605, -0.00521, -0.00448, -0.00374, -0.00303, -0.00234, -0.00167, -0.00103]
        ])

        matrix_b = np.array([
            [-0.01264, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01470, -0.01352, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01656, -0.01554, -0.01414, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01821, -0.01735, -0.01611, -0.01449, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.01967, -0.01897, -0.01789, -0.01642, -0.01458, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.02092, -0.02038, -0.01946, -0.01815, -0.01647, -0.01439, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.02197, -0.02159, -0.02083, -0.01968, -0.01815, -0.01624, -0.01395, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0],
            [-0.02308, -0.02256, -0.02182, -0.02112, -0.01952, -0.01778, -0.01576, -0.01348, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0],
            [-0.02400, -0.02351, -0.02280, -0.02202, -0.02072, -0.01917, -0.01735, -0.01525, -0.01289, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0],
            [-0.02481, -0.02434, -0.02366, -0.02273, -0.02167, -0.02031, -0.01868, -0.01678, -0.01460, -0.01216, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0],
            [-0.02554, -0.02507, -0.02440, -0.02362, -0.02235, -0.02103, -0.01981, -0.01793, -0.01599, -0.01386,
             -0.01156, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.02616, -0.02571, -0.02505, -0.02428, -0.02305, -0.02177, -0.02045, -0.01890, -0.01715, -0.01522,
             -0.01310, -0.01081, 0, 0, 0, 0, 0, 0, 0, 0],
            [-0.02668, -0.02625, -0.02561, -0.02487, -0.02364, -0.02239, -0.02109, -0.01949, -0.01813, -0.01623,
             -0.01430, -0.01226, -0.01013, 0, 0, 0, 0, 0, 0, 0],
            [-0.02715, -0.02673, -0.02611, -0.02536, -0.02417, -0.02294, -0.02164, -0.02012, -0.01866, -0.01708,
             -0.01531, -0.01345, -0.01149, -0.00944, 0, 0, 0, 0, 0, 0],
            [-0.02753, -0.02713, -0.02653, -0.02582, -0.02463, -0.02341, -0.02213, -0.02064, -0.01911, -0.01767,
             -0.01608, -0.01439, -0.01260, -0.01073, -0.00875, 0, 0, 0, 0, 0],
            [-0.02789, -0.02749, -0.02690, -0.02620, -0.02502, -0.02382, -0.02256, -0.02108, -0.01968, -0.01807,
             -0.01652, -0.01511, -0.01344, -0.01172, -0.00995, -0.00812, 0, 0, 0, 0],
            [-0.02821, -0.02781, -0.02722, -0.02652, -0.02536, -0.02417, -0.02292, -0.02146, -0.02007, -0.01850,
             -0.01698, -0.01549, -0.01408, -0.01251, -0.01089, -0.00921, -0.00747, 0, 0, 0],
            [-0.02848, -0.02809, -0.02750, -0.02682, -0.02565, -0.02447, -0.02324, -0.02176, -0.02041, -0.01885,
             -0.01736, -0.01590, -0.01441, -0.01312, -0.011591, -0.01004, -0.00847, -0.00688, 0, 0],
            [-0.02871, -0.02832, -0.02774, -0.02706, -0.02591, -0.02473, -0.02350, -0.02204, -0.02067, -0.01916,
             -0.01769, -0.01624, -0.01480, -0.01340, -0.01213, -0.01072, -0.00928, -0.00781, -0.00632, 0],
            [-0.02889, -0.02851, -0.02794, -0.02727, -0.02612, -0.02495, -0.02373, -0.02227, -0.02089, -0.01940,
             -0.01796, -0.01655, -0.01511, -0.01367, -0.01249, -0.01121, -0.00989, -0.00856, -0.00719, -0.00581]
        ])

    a_ = matrix_a * (hole_diameter / 0.08)
    b_ = matrix_b * (hole_diameter / 0.08)

    alfa_P = 1e-4
    alfa_Q = 1e-4
    alfa_T = 1e-4

    c = np.zeros((straindata.shape[0], straindata.shape[0]))

    for i in range(1, c.shape[0] - 1):
        c[i, i - 1] = -1
        c[i, i] = 2
        c[i, i + 1] = -1

    teste = 0
    while True:
        teste += 1
        P = np.linalg.inv(a_.T @ a_ + alfa_P * c.T @ c) @ ((E / (1 + v)) * a_.T @ p)
        p_misfit = p - ((1 + v) / E) * a_ @ P
        p_rms2 = (1 / straindata.shape[0]) * sum(p_misfit ** 2)

        if np.any(abs(p_rms2 - p_std2) / p_std2 <= 0.05):
            break
        else:
            alfa_P = (p_std2 / p_rms2) * alfa_P

    teste2 = 0
    while True:
        teste2 += 1
        Q = np.linalg.inv(b_.T @ b_ + alfa_Q * c.T @ c) @ (E * b_.T @ q)
        q_misfit = q - (1 / E) * b_ @ Q
        q_rms2 = (1 / straindata.shape[0]) * sum(q_misfit ** 2)

        if np.any(abs(q_rms2 - q_std2) / q_std2 <= 0.05):
            break
        else:
            alfa_Q = (q_std2 / q_rms2) * alfa_Q

    teste3 = 0
    while True:
        teste3 += 1
        T = np.linalg.inv(b_.T @ b_ + alfa_T * c.T @ c) @ (E * b_.T @ t)
        t_misfit = t - (1 / E) * b_ @ T
        t_rms2 = (1 / straindata.shape[0]) * sum(t_misfit ** 2)

        if np.any(abs(t_rms2 - t_std2) / t_std2 <= 0.05):
            break
        else:
            alfa_T = (t_std2 / t_rms2) * alfa_T

    sigma_x = P - Q
    sigma_y = P + Q
    tau_xy = T

    sigma_max = P + np.sqrt(Q ** 2 + T ** 2)
    sigma_min = P - np.sqrt(Q ** 2 + T ** 2)
    beta = (1 / 2) * np.arctan2(-T, -Q) * (180 / np.pi)

    # Plot 1
    graf1 = tk.Tk()
    graf1.title("Deformações lidas pelos extensômetros")
    fig, ax = plt.subplots()

    frame = tk.Frame(graf1)
    frame.pack()

    canvas1 = FigureCanvasTkAgg(fig, master=graf1)
    canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    # leg = canvas1.add_subplot(1,1,1)

    e1 = straindata[:, 1]
    e2 = straindata[:, 2]
    e3 = straindata[:, 3]

    # ax.xlabel('Hole Depth')
    line1 = ax.plot(e1, 'r--', label='e1')
    line2 = ax.plot(e2, 'b--', label='e2')
    line3 = ax.plot(e3, 'g--', label='e3')
    ax.legend(['e1', 'e2', 'e3'])
    ax.set_xlabel('Profundidade do Furo Cego(mm)')
    ax.set_ylabel('Deformação')
    canvas1.draw()

    # Plot 2
    graf2 = tk.Tk()
    graf2.title("Tensões Normais e de Cisalhamento")
    fig, ax = plt.subplots()

    frame = tk.Frame(graf2)
    frame.pack()

    canvas2 = FigureCanvasTkAgg(fig, master=graf2)
    canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    ax.plot(sigma_x, 'r--', label='Tensão Longitudinal')
    ax.plot(sigma_y, 'b--', label='Tensão Transversal')
    ax.plot(tau_xy, 'g--', label='Tensão de Cisalhamento')
    ax.legend(['Tensão Longitudinal', 'Tensão Transversal', 'Tensão de Cisalhamento'])
    ax.set_xlabel('Profundidade do Furo Cego(mm)')
    ax.set_ylabel('Tensão(MPa)')
    canvas2.draw()

    # Plot 3
    graf3 = tk.Tk()
    graf3.title("Tensões Principais Máxima e Mínima")
    fig, ax = plt.subplots()

    frame = tk.Frame(graf3)
    frame.pack()

    canvas3 = FigureCanvasTkAgg(fig, master=graf3)
    canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    ax.plot(sigma_max, 'r--', label='Tensão Principal Máxima')
    ax.plot(sigma_min, 'b--', label='Tensão Principal Mínima')
    ax.legend(['Tensão Principal Máxima', 'Tensão Principal Mínima'])
    ax.set_xlabel('Profundidade do Furo Cego(mm)')
    ax.set_ylabel('Tensão(MPa)')
    canvas3.draw()

    # Plot 4
    graf4 = tk.Tk()
    graf4.title("Ângulo Beta")
    fig, ax = plt.subplots()

    frame = tk.Frame(graf4)
    frame.pack()

    canvas4 = FigureCanvasTkAgg(fig, master=graf4)
    canvas4.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    ax.plot(beta, 'g--', label='Ângulo Beta')
    ax.legend(['Ângulo Beta'])
    ax.set_xlabel('Profundidade do Furo Cego(mm)')
    ax.set_ylabel('Ângulo')
    canvas4.draw()

    print('sigma_x', sigma_x)
    print('sigma_y', sigma_y)
    print('tau_xy', tau_xy)
    print('sigma_max', sigma_max)
    print('sigma_min', sigma_min)
    print('Beta', beta)

    mensagem = f"Tensões uniformes calculadas:\n\nTensão Longitudinal: {sigma_x}\nTensão Transversal: {sigma_y}\nTensão de Cisalhamento: {tau_xy}\nTensão Principal Máxima: {sigma_max}\nTensão Principal Mínima: {sigma_min}\nÂngulo Beta: {beta}"

    resultado.config(text=mensagem)

    graf1.mainloop()
    graf2.mainloop()
    graf3.mainloop()
    graf4.mainloop()


def calculo_uniforme(modulo_elasticidade, poisson, diametro_furo, tipo_roseta, arquivo):
    ## Inputs
    E = modulo_elasticidade;  # TPa - 0.205
    v = poisson;  # Poisson - 0.3
    hole_diameter = diametro_furo;  # mm - 0.0625
    Rosete_Type = tipo_roseta;  # 1=A, 2=B, 3=C
    filename = arquivo;  # dados_novo.txt

    ## 9.2.1 Strain Data
    straindata_load = np.loadtxt(filename)

    straindata = np.zeros((10, 4))
    straindata[:, 0] = np.arange(0.10, 1.10, 0.10)
    straindata[:, 1] = interp1d(straindata_load[:, 0], straindata_load[:, 1], kind='cubic', fill_value="extrapolate")(
        straindata[:, 0])
    straindata[:, 2] = interp1d(straindata_load[:, 0], straindata_load[:, 2], kind='cubic', fill_value="extrapolate")(
        straindata[:, 0])
    straindata[:, 3] = interp1d(straindata_load[:, 0], straindata_load[:, 3], kind='cubic', fill_value="extrapolate")(
        straindata[:, 0])

    p = (straindata[:, 3] + straindata[:, 1]) / 2
    q = (straindata[:, 3] - straindata[:, 1]) / 2
    t = (straindata[:, 3] + straindata[:, 1] - 2 * straindata[:, 2]) / 2

    # Plot 1
    graf1 = tk.Tk()
    graf1.title("Deformações lidas pelos extensômetros")
    fig, ax = plt.subplots()

    frame = tk.Frame(graf1)
    frame.pack()

    canvas1 = FigureCanvasTkAgg(fig, master=graf1)
    canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    ax.plot(straindata[:, 1], 'r--', label='e1')
    ax.plot(straindata[:, 2], 'b--', label='e2')
    ax.plot(straindata[:, 3], 'g--', label='e3')
    ax.legend(['e1', 'e2', 'e3'])
    ax.set_xlabel('Profundidade do Furo Cego(mm)')
    ax.set_ylabel('Deformação')
    canvas1.draw()

    ##9.2.2 Calibration Constants
    wb2 = xlrd.open_workbook('Constantes.xls')
    pp = wb2.sheet_by_name('A')
    lin = pp.nrows

    if Rosete_Type == '1':
        p1 = wb2.sheet_by_name('A')

        if hole_diameter == '0.06':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = p1.cell(i, 1).value
                b_[i] = p1.cell(i, 7).value

        if hole_diameter > '0.06' and hole_diameter < '0.07':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = np.interp(hole_diameter, p1.cell(i, 1).value, p1.cell(i, 2).value)
                b_[i] = np.interp(hole_diameter, p1.cell(i, 7).value, p1.cell(i, 8).value)

        if hole_diameter == '0.07':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = p1.cell(i, 2).value
                b_[i] = p1.cell(i, 8).value

        if hole_diameter > '0.07' and hole_diameter < '0.08':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = np.interp(hole_diameter, p1.cell(i, 2).value, p1.cell(i, 3).value)
                b_[i] = np.interp(hole_diameter, p1.cell(i, 8).value, p1.cell(i, 9).value)

        if hole_diameter == '0.08':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = p1.cell(i, 3).value
                b_[i] = p1.cell(i, 9).value

        if hole_diameter > '0.08' and hole_diameter < '0.09':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = np.interp(hole_diameter, p1.cell(i, 3).value, p1.cell(i, 4).value)
                b_[i] = np.interp(hole_diameter, p1.cell(i, 9).value, p1.cell(i, 10).value)

        if hole_diameter == '0.09':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = p1.cell(i, 4).value
                b_[i] = p1.cell(i, 10).value

        if hole_diameter > '0.09' and hole_diameter < '0.10':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = np.interp(hole_diameter, p1.cell(i, 4).value, p1.cell(i, 5).value)
                b_[i] = np.interp(hole_diameter, p1.cell(i, 10).value, p1.cell(i, 11).value)

        if hole_diameter == '0.10':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = p1.cell(i, 5).value
                b_[i] = p1.cell(i, 11).value

    if Rosete_Type == '2':
        p1 = wb2.sheet_by_name('B')

        if hole_diameter == '0.06':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = p1.cell(i, 1).value
                b_[i] = p1.cell(i, 7).value

        if hole_diameter > '0.06' and hole_diameter < '0.07':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = np.interp(hole_diameter, p1.cell(i, 1).value, p1.cell(i, 2).value)
                b_[i] = np.interp(hole_diameter, p1.cell(i, 7).value, p1.cell(i, 8).value)

        if hole_diameter == '0.07':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = p1.cell(i, 2).value
                b_[i] = p1.cell(i, 8).value

        if hole_diameter > '0.07' and hole_diameter < '0.08':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = np.interp(hole_diameter, p1.cell(i, 2).value, p1.cell(i, 3).value)
                b_[i] = np.interp(hole_diameter, p1.cell(i, 8).value, p1.cell(i, 9).value)

        if hole_diameter == '0.08':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = p1.cell(i, 3).value
                b_[i] = p1.cell(i, 9).value

        if hole_diameter > '0.08' and hole_diameter < '0.09':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = np.interp(hole_diameter, p1.cell(i, 3).value, p1.cell(i, 4).value)
                b_[i] = np.interp(hole_diameter, p1.cell(i, 9).value, p1.cell(i, 10).value)

        if hole_diameter == '0.09':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = p1.cell(i, 4).value
                b_[i] = p1.cell(i, 10).value

        if hole_diameter > '0.09' and hole_diameter < '0.10':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = np.interp(hole_diameter, p1.cell(i, 4).value, p1.cell(i, 5).value)
                b_[i] = np.interp(hole_diameter, p1.cell(i, 10).value, p1.cell(i, 11).value)

        if hole_diameter == '0.10':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = p1.cell(i, 5).value
                b_[i] = p1.cell(i, 11).value

    if Rosete_Type == '3':
        p1 = wb2.sheet_by_name('C')

        if hole_diameter == '0.06':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = p1.cell(i, 1).value
                b_[i] = p1.cell(i, 7).value

        if hole_diameter > '0.06' and hole_diameter < '0.07':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = np.interp(hole_diameter, p1.cell(i, 1).value, p1.cell(i, 2).value)
                b_[i] = np.interp(hole_diameter, p1.cell(i, 7).value, p1.cell(i, 8).value)

        if hole_diameter == '0.07':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = p1.cell(i, 2).value
                b_[i] = p1.cell(i, 8).value

        if hole_diameter > '0.07' and hole_diameter < '0.08':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = np.interp(hole_diameter, p1.cell(i, 2).value, p1.cell(i, 3).value)
                b_[i] = np.interp(hole_diameter, p1.cell(i, 8).value, p1.cell(i, 9).value)

        if hole_diameter == '0.08':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = p1.cell(i, 3).value
                b_[i] = p1.cell(i, 9).value

        if hole_diameter > '0.08' and hole_diameter < '0.09':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = np.interp(hole_diameter, p1.cell(i, 3).value, p1.cell(i, 4).value)
                b_[i] = np.interp(hole_diameter, p1.cell(i, 9).value, p1.cell(i, 10).value)

        if hole_diameter == '0.09':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = p1.cell(i, 4).value
                b_[i] = p1.cell(i, 10).value

        if hole_diameter > '0.09' and hole_diameter < '0.10':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = np.interp(hole_diameter, p1.cell(i, 4).value, p1.cell(i, 5).value)
                b_[i] = np.interp(hole_diameter, p1.cell(i, 10).value, p1.cell(i, 11).value)

        if hole_diameter == '0.10':
            a_ = np.zeros(lin)
            b_ = np.zeros(lin)

            for i in range(lin):
                a_[i] = p1.cell(i, 5).value
                b_[i] = p1.cell(i, 11).value

    # print (a_, b_)
    ## STRESS CALCULATION METHOD

    a_a = a_ ** 2
    a_p = a_ * p
    b_b = b_ ** 2
    b_q = b_ * q
    b_t = b_ * t

    aa = sum(a_a)
    ap = sum(a_p)
    bb = sum(b_b)
    bq = sum(b_q)
    bt = sum(b_t)

    P = -(E / (1 + v)) * (ap / aa)
    Q = -E * (bq / bb)
    T = -E * (bt / bb)

    # Compute the Cartesian stresses

    sigma_x = P - Q
    sigma_y = P + Q
    tau_xy = T

    # Compute the principal stresses and direction

    sigma_max = P + math.sqrt(((Q * Q) + (T * T)))
    sigma_min = P - math.sqrt((Q * Q) + (T * T))
    be = (0.5) * math.atan((-T) / (-Q))
    beta = np.degrees(be)

    print('sigma_x', sigma_x)
    print('sigma_y', sigma_y)
    print('tau_xy', tau_xy)
    print('sigma_max', sigma_max)
    print('sigma_min', sigma_min)
    print('Beta', beta)
    # resultados = sigma_x , sigma_y , tau_xy , sigma_max , sigma_min , beta

    mensagem = f"Tensões uniformes calculadas:\n\nTensão Longitudinal: {sigma_x}\nTensão Transversal: {sigma_y}\nTensão de Cisalhamento: {tau_xy}\nTensão Principal Máxima: {sigma_max}\nTensão Principal Mínima: {sigma_min}\nÂngulo Beta: {beta}"

    resultado.config(text=mensagem)
    graf1.mainloop()


# Criação da janela principal
janela = tk.Tk()
janela.title("Automatização de cálculos da ASTM E-837 13a")

# Estilo
estilo = ttk.Style()
estilo.configure("TLabel", font=("Arial", 12))
estilo.configure("TButton", font=("Arial", 12))

# Campos de entrada e rótulos
rotulo_modulo = ttk.Label(janela, text="Insira o módulo de elasticidade do material (TPa):")
rotulo_modulo.pack(pady=10)
entrada_modulo = ttk.Entry(janela)
entrada_modulo.pack(pady=5)

rotulo_poisson = ttk.Label(janela, text="Insira o poisson do material:")
rotulo_poisson.pack(pady=10)
entrada_poisson = ttk.Entry(janela)
entrada_poisson.pack(pady=5)

rotulo_diametro = ttk.Label(janela, text="Insira o diâmetro do furo realizado (in):")
rotulo_diametro.pack(pady=10)
entrada_diametro = ttk.Entry(janela)
entrada_diametro.pack(pady=5)

rotulo_roseta = ttk.Label(janela, text="Insira o tipo de roseta (1=A, 2=B, 3=C):")
rotulo_roseta.pack(pady=10)
entrada_roseta = ttk.Entry(janela)
entrada_roseta.pack(pady=5)

nome_arquivo = ttk.Label(janela, text="Insira o nome do arquivo (.txt):")
nome_arquivo.pack(pady=10)
entrada_arquivo = ttk.Entry(janela)
entrada_arquivo.pack(pady=5)

# Botões
botao_uniformes = ttk.Button(janela, text="Calcular tensões uniformes", command=calcular_tensoes_uniformes)
botao_uniformes.pack(pady=10)

botao_nao_uniformes = ttk.Button(janela, text="Calcular tensões não uniformes", command=calcular_tensoes_nao_uniformes)
botao_nao_uniformes.pack(pady=5)

# Rótulo para exibir o resultado
resultado = ttk.Label(janela, font=("Arial", 12))
resultado.pack(pady=10)

# Execução da janela principal
janela.mainloop()