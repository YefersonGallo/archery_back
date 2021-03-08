import numpy as np
from scipy.stats.distributions import chi2
from scipy.stats import kstwo
import time
import requests


def test_media(randoms):
    med = media(randoms)

    n = len(randoms)
    z = 1.96

    li = (1 / 2) - (z * (1 / np.sqrt(12 * n)));
    ls = (1 / 2) + (z * (1 / np.sqrt(12 * n)));

    return (med <= ls) & (med >= li);


def test_varianza(randoms):
    n = len(randoms)
    grade_liberty = n - 1
    acceptation = 0.95
    a = 1 - acceptation

    variance = np.var(randoms, ddof=1)

    a_2 = a / 2
    a_3 = 1 - a_2

    xa_1 = chi2.ppf(a_3, df=grade_liberty)
    xa_2 = chi2.ppf(a_2, df=grade_liberty)

    li = xa_1 / (12 * grade_liberty)
    ls = xa_2 / (12 * grade_liberty)

    if ls > li:
        return (variance <= ls) & (variance >= li)
    else:
        return (variance >= ls) & (variance <= li)


def test_chi2(randoms):
    n = len(randoms)

    hist = np.histogram(randoms)[0]

    chi_sum = 0

    for i in range(len(hist)):
        frec_obt = hist[i]
        frec_esp = round(n / len(hist), 2)
        chi_sum += round(((frec_obt - frec_esp) ** 2) / frec_esp, 2)

    return chi2.ppf(0.95, df=len(hist) - 1) > chi_sum


def test_ks(randoms):
    acceptation = 0.95
    n = len(randoms)

    hist = np.histogram(randoms)[0]
    difs = []
    p_esp = n / len(hist)
    p_esp_aux = p_esp
    f_acum = hist[0]
    for i in range(len(hist)):
        if i != 0:
            p_esp += p_esp_aux
            f_acum += hist[i]
        difs.append(abs((f_acum / n) - (p_esp / n)))
    d_max = max(difs)
    if n <= 50:
        d_maxp = kstwo.ppf(acceptation, n)
    else:
        d_maxp = 1.3581 / np.sqrt(n)
    return d_max < d_maxp


def test_poker(randoms):
    return requests.post('https://dcb-node-deploy-poker.herokuapp.com/pokertest', json={"listRi": randoms}).json()[
        "isOk"]


def test_all(randoms):
    return test_media(randoms) & test_varianza(randoms) & test_chi2(randoms) & test_ks(randoms) & test_poker(randoms)


def linear_congruence(n):
    xn = int(time.time() * np.random.random())
    k = 4
    a = 1 + (2 * k)
    c = 3
    g = 1
    m = 1024
    while m < n:
        g = g + 1
        m = 2 ** g
    randoms = []
    for i in range(n):
        xn1 = ((a * xn) + c) % m
        randoms.append(xn1 / m)
        xn = xn1
    return randoms;


def media(ri):
    return sum(ri) / len(ri)