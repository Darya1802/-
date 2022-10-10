from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors

import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)


# поиск мастера с максимальным рейтингом
def find_max_ratings(max_rating, perfect_masters, best_master):
    for master in perfect_masters:
        if max_rating < master[6]:
            max_rating = master[6]
            best_master = master

    return max_rating, best_master


# обучение сети с алгоритмом к-ближайших соседей
def knn(X, geo_needed, n_neighbors=5):
    neighbors = NearestNeighbors(n_neighbors=n_neighbors, algorithm='ball_tree').fit(X)
    k_distances, k_indices = neighbors.kneighbors([[geo_needed["lat"], geo_needed["lon"]]])

    return k_distances, k_indices


# получение координат
def get_coords(found_masters, geo_needed):
    coords = [[found_masters[i][3], found_masters[i][4]] for i in range(len(found_masters))]

    coords.append([geo_needed["lat"], geo_needed["lon"]])

    return np.array(coords)


# получение мастеров только с нужными услугами
def get_master_service_true(X, services_need):
    master_service_true = []

    for i in range(len(X)):
        for j in range(len(services_need)):
            if X[i][1] == services_need[j]:
                master_service_true.append(X[i])

    return master_service_true


# подсчет суммы стоимости необходимых услуг у найденных мастеров
def get_masters_prices(masters, master_service_true):
    found_masters = []
    prices = {}

    for i in range(len(masters)):
        tmp = 0
        price = 0
        for j in range(len(master_service_true)):
            if masters[i][0] == master_service_true[j][0]:
                tmp += 1
                price += master_service_true[j][3]
                if tmp == len(services_need):
                    found_masters.append(masters[i])
                    prices[masters[i][0]] = price

    return found_masters, prices


X = []
masters = []

ms = pd.read_csv('master_service_big.csv')
m = pd.read_csv('masters_big.csv')
m2 = m.query("geo_lat != 0")
m2 = m.query("geo_lon != 0")

X = np.array(ms)
masters = np.array(m2)

# входные данные
services_need = [1, 2, 3]
level_need = 2
price_need = 5000 * 1.2

geo_needed = {
    "lat": -1,
    "lon": -1
}

studio_need = 'f'

found_masters, prices = get_masters_prices(
    masters,
    get_master_service_true(X, services_need)
)

# получение подходящих по услугам мастеров
perfect_masters = list(filter(
    lambda master: (prices[master[0]] < price_need) and (master[1] == level_need) and (master[5] == studio_need),
    found_masters
))

# если во входных данных указаны координаты, то найти ближайщих мастеров
if (geo_needed["lat"] != -1) or (geo_needed["lon"] != -1):
    coords = get_coords(perfect_masters, geo_needed)

    distances, indices = knn(coords[0:-1], geo_needed)

    masters_near = [perfect_masters[index] for index in indices[0]]

    #

    max_rating = 0
    best_master = masters_near[0]
    max_rating, best_master = find_max_ratings(max_rating, masters_near, best_master)

    for master in masters_near:
        print("Ближайший мастер:\n",
              master, '\n',
              "Цена за желаемые услуги: ", prices[master[0]], '\n', )

    i = 5

    while (i < 20) or (max_rating < 4):
        distances, indices = knn(coords[0:-1], geo_needed, i)
        masters_near = [perfect_masters[index] for index in indices[0]]
        max_rating, best_master = find_max_ratings(max_rating, masters_near, best_master)
        i += 10

    print("Мастер с лучшим рейтингом, но на большем расстоянии:\n",
          best_master, '\n',
          "Цена за желаемые услуги: ", prices[best_master[0]], '\n')

# если координаты не указаны, то возвращаются мастера с наибольшим рейтингом
else:
    best_masters_without_address = []
    for master in perfect_masters:
        if (master[6] > 4):
            best_masters_without_address.append(master)
    for master in best_masters_without_address:
        print("Подходящие мастера:\n",
              master, '\n',
              "Цена за желаемые услуги: ", prices[master[0]], '\n', )
