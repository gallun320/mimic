from math import sqrt

critics ={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
          'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
          'The Night Listener': 3.0},
          'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
          'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
          'You, Me and Dupree': 3.5},
          'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
'The Night Listener': 4.5, 'Superman Returns': 4.0,
'You, Me and Dupree': 2.5},
'Mick LaSalle': {
    'Lady in the Water': 3.0,
    'Snakes on a Plane': 4.0,
    'Just My Luck': 2.0,
    'Superman Returns': 3.0,
    'The Night Listener': 3.0,
    'You, Me and Dupree': 2.0
},
'Jack Matthews': {
    'Lady in the Water': 3.0,
    'Snakes on a Plane': 4.0,
    'The Night Listener': 3.0,
    'Superman Returns': 5.0,
    'You, Me and Dupree': 3.5
    },
'Toby': {
    'Snakes on a Plane':4.5,
    'You, Me and Dupree':1.0,
    'Superman Returns':4.0
    }
}




def sim_distance(prefs,person1,person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    if len(si) == 0: return 0

    sum_of_squares = sum([pow(prefs[person1][it] - prefs[person2][it],2) for it in prefs[person1] if it in prefs[person2]])
    return 1/(1 + sqrt(sum_of_squares))

def sim_distance_pirs(prefs,p1,p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item] = 1

    n = len(si)

    if n == 0: return 0

    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    sumSq1 = sum([pow(prefs[p1][it],2) for it in si])
    sumSq2 = sum([pow(prefs[p2][it],2) for it in si])

    sumP = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    num = sumP - (sum1 * sum2 / n)

    den = sqrt((sumSq1 - pow(sum1,2) / n) * (sumSq2 - pow(sum2,2) / n))

    if den == 0: return 0

    r = num/den

    return r


def normalize_tanimoto(prefs):
    arr = prefs.copy()

    for critic in arr:
        for film in arr[critic]:
            if arr[critic][film] < 3:
                arr[critic][film] = 0
            else:
                arr[critic][film] = 1
    return arr

def sim_tanimoto(prefs, p1,p2):

    arr = normalize_tanimoto(prefs)

    a = float(len(arr[p1]))
    b = float(len(arr[p2]))
    c = 0.0

    for film in arr[p1]:
        if arr[p1][film] == arr[p2][film]:
            c = c + 1


    result = c / ( a + b - c)
    return float(result)


def topMatches(prefs, pers, n = 5, sim = sim_distance):
    scores = [(sim(prefs,pers, other), other) for other in prefs if other != pers]

    scores.sort(reverse=True)

    return scores[:n]

def getRecommendations(prefs, pers,  similarity = sim_distance):
    totals = {}
    simSum = {}

    for other in prefs:
        if other == pers: continue
        sim = similarity(prefs, pers, other)

        if sim <= 0: continue

        for item in prefs[other]:
            if item not in prefs[pers] or prefs[pers][item] == 0:
                totals[item] = totals.get(item, 0) +  prefs[other][item] * sim
                simSum[item] = simSum.get(item,0) + sim
    ranking = [(total / simSum[item], item) for item, total in totals.items()]

    ranking.sort(reverse=True)

    return ranking


def transformPrefs(prefs):
     result={}
     for person in prefs:
       for item in prefs[person]:
         result[item] = {}
         result[item][person]=prefs[person][item]
     return result

def calculateSimilarItems(prefs, n=10):
    result = {}

    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        c += 1
        if c % 100 == 0: print "%d / %d" % (c, len(itemPrefs))
        scores = topMatches(itemPrefs, item, n = n, sim = sim_distance)
        result[item] = scores
    return result


def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}
    for item, rating in userRatings.items():
        for simalarity, item2 in itemMatch[item]:
            if item2 in userRatings: continue
            scores[item2] = scores.get(item2,0) + (simalarity * rating)
            totalSim[item2] = totalSim.get(item2, 0) + simalarity
    ranking = [(score/totalSim[item], item) for item, score in scores.items()]
    ranking.sort(reverse=True)
    return ranking


def loadMoviewLens(path=''):
    movies = {}

    for line in open('u.item'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title

    prefs = {}

    for  line in open('u.data'):

        (user, movieId, rating, ts) = line.split('\t')
        prefs.setdefault(user,{})
        prefs[user][movies[movieId]] = float(rating)
    return prefs

##print getRecommendations(critics, 'Toby', sim_distance_pirs)


##print getRecommendedItems(critics, itemsim, 'Toby')
##data = loadMoviewLens()
#itemsim = calculateSimilarItems(data)
print sim_tanimoto(critics, 'Toby', 'Lisa Rose')
