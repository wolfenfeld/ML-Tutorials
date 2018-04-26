import sys, math
import numpy as np
from scipy.stats import ortho_group
from scipy.stats import pearsonr
from tpot import TPOTRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics.scorer import make_scorer
from sklearn.linear_model import SGDRegressor
from sklearn import datasets
import matplotlib.pyplot as plt


def npperm(M):
    n = M.shape[0]
    d = np.ones(n)
    j = 0
    s = 1
    f = np.arange(n)
    v = M.sum(axis=0)
    p = np.prod(v)
    while (j < n-1):
        v -= 2*d[j]*M[j]
        d[j] = -d[j]
        s = -s
        prod = np.prod(v)
        p += s*prod
        f[0] = 0
        f[j] = f[j+1]
        f[j+1] = j+1
        j = f[0]
    return p/2**(n-1)


# Define loss function to be between 0 and 1 where 0 is the best and 1 is the
# worst for optimisation.
def correlation_coefficient(y_true, y_pred):
    pearson_r, _ = pearsonr(y_pred, y_true)
    return 1-pearson_r**2


dimension = 8

print("Making the input data using seed 7", file=sys.stderr)
np.random.seed(7)
U = ortho_group.rvs(dimension**2)
U = U[:, :dimension]
# U is a random orthogonal matrix
X = []
Y = []
print(U)
for i in range(4000):
    I = np.random.choice(dimension**2, size=dimension)
    A = U[I][np.lexsort(np.rot90(U[I]))]
    X.append(A.ravel())
    Y.append(math.log(npperm(A)**2, 2))

data, target = datasets.load_boston()

X = np.array(data)
Y = np.array(target)

# Split into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, Y,
                                                    train_size=0.75, test_size=0.25)


my_scorer = make_scorer(correlation_coefficient, greater_is_better=True)

svr = GridSearchCV(SGDRegressor(kernel='rbf', gamma=0.1),
                   scoring=my_scorer,
                   cv=5,
                   param_grid={"C": [1e0, 1e1, 1e2, 1e3],
                               "gamma": np.logspace(-2, 2, 5)})
train_size = 1
svr.fit(X[:train_size], y[:train_size])

print(svr.best_params_)
print svr.score(X[train_size:], y[train_size:])

# Create model
tpot = TPOTRegressor(scoring=correlation_coefficient, generations=10,
                     population_size=40, verbosity=2, n_jobs=4)
tpot.fit(X_train, y_train)


class PatientDistribution(object):

    def __init__(self, mean=0, std=1, plot_type=go.Bar):
        self.pdf = gaussian
        self.mean = mean
        self.std = std
        self.plot_type = plot_type
        self.range = np.arange(0, 10, 0.01)

    def get_single_plot(self, step, color='00CED1'):
        return go.Bar(visible=False,
                      marker=dict(color=color),
                      name='𝜈 = ' + str(step),
                      x=self.range,
                      y=gaussian(self.range, step, self.std))

    def get_slider_figure(self, slider_range=self.range):
        data = [self.get_single_plot(i) for i in slider_range]

        steps = []

        for i in range(len(slider_range)):
            step = dict(
                method='restyle',
                args=['visible', [False] * len(slider_range)],
            )
            step['args'][1][i] = True  # Toggle i'th trace to "visible"
            steps.append(step)

        sliders = [dict(
            active=10,
            currentvalue={"prefix": "Frequency: "},
            pad={"t": 50},
            steps=steps
        )]

        layout = go.Layout(sliders=sliders)

        fig = go.Figure(data=data, layout=layout)