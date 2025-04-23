import numpy as np

h = 0.1
t =  np.array([
    52.84,
    56.05,
    48.46,
    48.43,
    52.78,
    41.92,
    45.44,
    42.42,
    44.53,
    44.73,
    32.82,
    32.70,
    35.51,
    30.88,
    29.85,
    24.08,
    25.10,
    24.86,
    23.15,
    26.88
])


def SIro(rox): #СИ
    return rox * 10**(-3) / (0.01)**3


ro = SIro(2.6) #ля шариков, СИ
def nu(v, R, roi):
    g = 9.8
    nu = 2/9 * g * R**2 * (ro - roi) / v
    return nu


def Tau(R, nu):
    Tau = 2/9 * R**2 * ro / nu
    return Tau


def Re(v, R, nu):
    Re = ro * v * 2*R / nu
    return Re

v = h / t



v1 = v[:5]
ro1 = SIro(1.2390)
R1 = np.array([
    1.14,
    1.10,
    1.20,
    1.24,
    1.19
]) * 0.001 / 2 #мм в метры

nu1 = nu(v1, R1, ro1)

Tau1 =  Tau(R1, nu1)

Re1 = Re(v1, R1, nu1)

S1 = v1 * Tau1


v2 = v[5:10]
ro2 = SIro(1.2377)
R2 = np.array([
    1.13,
    1.20,
    1.14,
    1.09,
    1.10
]) * 0.001 / 2

nu2 = nu(v2, R2, ro2)

Tau2 =  Tau(R2, nu2)

Re2 = Re(v2, R2, nu2)

S2 = v2 * Tau2


v3 = v[10:15]
ro3 = SIro(1.2344)
R3 = np.array([
    1.18,
    1.05,
    1.13,
    1.17,
    1.11
]) * 0.001 / 2

nu3 = nu(v3, R3, ro3)

Tau3 =  Tau(R3, nu3)

Re3 = Re(v3, R3, nu3)

S3 = v3 * Tau3


v4 = v[15:]
ro4 = SIro(1.2312)
R4 = np.array([
    1.15,
    1.14,
    1.24,
    1.36,
    1.23
]) * 0.001 / 2

nu4 = nu(v4, R4, ro4)

Tau4 =  Tau(R4, nu4)

Re4 = Re(v4, R4, nu4)

#print("his_Re:", his_Re[15:])
S4 = v4 * Tau4


def MNK(x, y):
    N = 20
    Sx = np.sum(x)
    Sy = np.sum(y)
    Sx2 = np.sum(x**2)
    Sxy = 0
    for i in range(N):
        Sxy += x[i] * y[i]
    a = (N * Sxy - Sx * Sy) / (N * Sx2 - Sx**2)
    b = (Sy - a*Sx) / N
    return a, b


lnu1 = np.log(nu1)
lnu2 = np.log(nu2)
lnu3 = np.log(nu3)
lnu4 = np.log(nu4)
lnu = np.hstack((lnu1, lnu2, lnu3, lnu4))

T1 = 28.57 + 273.15
T2 = 32.00 + 273.15
T3 = 36.00 + 273.15
T4 = 40.00 + 273.15

ar1 = [1 / T1] * 5
ar2 = [1 / T2] * 5
ar3 = [1 / T3] * 5
ar4 = [1 / T4] * 5
ar1 = np.array(ar1)
ar2 = np.array(ar2)
ar3 = np.array(ar3)
ar4 = np.array(ar4)
arx = np.hstack((ar1, ar2, ar3, ar4))

a, b = MNK(arx, lnu)
print("a b:", a, b)

k = 1.38 / 10**23 #Дж/К
W = k * a
print("W:", W, "Джоулей") #в Джоулях


