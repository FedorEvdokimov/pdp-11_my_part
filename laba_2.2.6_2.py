import numpy as np


his_Re =  np.array([
    322.95,
    209.96,
    270.70,
    344.82,
    338.05,
    467.07,
    432.99,
    377.00,
    462.76,
    373.35,
    647.98,
    821.32,
    565.58,
    706.63,
    788.80,
    885.27,
    1060.73,
    1042.13,
    983.39,
    959.66
])
his_Re = np.round(his_Re / 10**5, 5)
print("his_Re:", his_Re)






h = 0.1
t =  np.array([
    48.13,
    65.72,
    53.52,
    47.01,
    48.04,
    39.20,
    42.00,
    45.71,
    39.11,
    45.30,
    34.65,
    28.90,
    37.08,
    32.71,
    30.13,
    29.37,
    26.40,
    26.37,
    27.77,
    28.22
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
    1.12,
    0.92,
    1.08,
    1.10,
    1.07
]) * 0.001 / 2 #мм в метры
print("v1:", np.round(v1 * 10**3, 2))
nu1 = nu(v1, R1, ro1)
print("nu1:", np.round(nu1 * 10**3, 2))
Tau1 =  Tau(R1, nu1)
print("Tau1:", np.round(Tau1 * 10**4, 2))
Re1 = Re(v1, R1, nu1)
print("Re1:", np.round(Re1, 5))
print("his_Re:", his_Re[:5])
print()

v2 = v[5:10]
ro2 = SIro(1.2368)
R2 = np.array([
    1.16,
    1.09,
    1.06,
    1.18,
    1.09
]) * 0.001 / 2
print("v2:", np.round(v2 * 10**3, 2))
nu2 = nu(v2, R2, ro2)
print("nu2:", np.round(nu2 * 10**3, 2))
Tau2 =  Tau(R2, nu2)
print("Tau2:", np.round(Tau2 * 10**4, 2))
Re2 = Re(v2, R2, nu2)
print("Re2:", np.round(Re2, 5))
print("his_Re:", his_Re[5:10])
print()

v3 = v[10:15]
ro3 = SIro(1.2344)
R3 = np.array([
    1.07,
    1.21,
    1.07,
    1.10,
    1.16
]) * 0.001 / 2
print("v3:", np.round(v3 * 10**3, 2))
nu3 = nu(v3, R3, ro3)
print("nu3:", np.round(nu3 * 10**3, 2))
Tau3 =  Tau(R3, nu3)
print("Tau3:", np.round(Tau3 * 10**4, 2))
Re3 = Re(v3, R3, nu3)
print("Re3:", np.round(Re3, 5))
print("his_Re:", his_Re[10:15])
print()

v4 = v[15:]
ro4 = SIro(1.2320)
R4 = np.array([
    1.08,
    1.12,
    1.14,
    1.09,
    1.08
]) * 0.001 / 2
print("v4:", np.round(v4 * 10**3, 2))
nu4 = nu(v4, R4, ro4)
print("nu4:", np.round(nu4 * 10**3, 2))
Tau4 =  Tau(R4, nu4)
print("Tau4:", np.round(Tau4 * 10**4, 2))
Re4 = Re(v4, R4, nu4)
print("Re4:", np.round(Re4, 5))
print("his_Re:", his_Re[15:])
print()


