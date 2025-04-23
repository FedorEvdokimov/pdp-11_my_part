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
#print("v:", np.round(v * 10**3, 2))
#v = np.round(v, 4)


v1 = v[:5]
ro1 = SIro(1.2390)
R1 = np.array([
    1.14,
    1.10,
    1.20,
    1.24,
    1.19
]) * 0.001 / 2 #мм в метры
print("v1:", np.round(v1 * 10**3, 2))
nu1 = nu(v1, R1, ro1)
print("nu1:", np.round(nu1 * 10**3, 2))
Tau1 =  Tau(R1, nu1)
print("Tau1:", np.round(Tau1 * 10**4, 2))
Re1 = Re(v1, R1, nu1)
print("Re1:", np.round(Re1, 3))
#print("his_Re:", his_Re[:5])
S1 = v1 * Tau1
#print("v1, Tau1:", v1, Tau1)
print("S1:", np.round(S1, 9))
print()

v2 = v[5:10]
ro2 = SIro(1.2377)
R2 = np.array([
    1.13,
    1.20,
    1.14,
    1.09,
    1.10
]) * 0.001 / 2
print("v2:", np.round(v2 * 10**3, 2))
nu2 = nu(v2, R2, ro2)
print("nu2:", np.round(nu2 * 10**3, 2))
Tau2 =  Tau(R2, nu2)
print("Tau2:", np.round(Tau2 * 10**4, 2))
Re2 = Re(v2, R2, nu2)
print("Re2:", np.round(Re2, 3))
#print("his_Re:", his_Re[5:10])
print()

v3 = v[10:15]
ro3 = SIro(1.2344)
R3 = np.array([
    1.18,
    1.05,
    1.13,
    1.17,
    1.11
]) * 0.001 / 2
print("v3:", np.round(v3 * 10**3, 2))
nu3 = nu(v3, R3, ro3)
print("nu3:", np.round(nu3 * 10**3, 2))
Tau3 =  Tau(R3, nu3)
print("Tau3:", np.round(Tau3 * 10**4, 2))
Re3 = Re(v3, R3, nu3)
print("Re3:", np.round(Re3, 3))
#print("his_Re:", his_Re[10:15])
print()

v4 = v[15:]
ro4 = SIro(1.2312)
R4 = np.array([
    1.15,
    1.14,
    1.24,
    1.36,
    1.23
]) * 0.001 / 2
print("v4:", np.round(v4 * 10**3, 2))
nu4 = nu(v4, R4, ro4)
print("nu4:", np.round(nu4 * 10**3, 2))
Tau4 =  Tau(R4, nu4)
print("Tau4:", np.round(Tau4 * 10**4, 2))
Re4 = Re(v4, R4, nu4)
print("Re4:", np.round(Re4, 3))
#print("his_Re:", his_Re[15:])
print()

