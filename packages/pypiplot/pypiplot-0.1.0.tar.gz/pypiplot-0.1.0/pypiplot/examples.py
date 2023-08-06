# %%
# import pypiplot
# print(pypiplot.__version__)

from pypiplot import pypiplot
print(dir(pypiplot))

# %%
pp = pypiplot(username='erdogant')

# %% Update all
pp.update()

# %% Update single repo
pp.update(repo=['bnlearn'])
pp.update(repo='bnlearn')

results = pp.stats(repo=['df2onehot','pca'])
results = pp.stats(repo='df2onehot')

# %% Get some stats
results = pp.stats(repo=['df2onehot','pca','bnlearn','ismember','thompson'])

# %%
pp = pypiplot(username='erdogant')

pp.stats(repo='distfit')
pp.plot_year()
pp.plot(vmin=25)

pp.stats(repo='worldmap')
pp.plot_year()

pp.stats(repo='hnet')
pp.plot_year()

pp.stats(repo='ismember')
pp.plot_year()

pp.stats(repo='flameplot')
pp.plot_year()

pp.stats(repo='pca')
pp.plot_year()

pp.stats(repo=['df2onehot','pca','bnlearn','ismember','thompson'])
pp.plot_year(vmin=100)
pp.plot(vmin=25)

# %% Plot bnlearn
results = pp.stats(repo='bnlearn')
pp.plot_year()

# %%
results = pp.stats()
pp.plot_year(vmin=700)
pp.plot(vmin=25)

# %% Plot
pp.stats()
path = 'D://PY/REPOSITORIES/erdogant.github.io/docs/imagesc/pypi/pypi_heatmap.html'
pp.plot_year(path=path, vmin=700)

path = 'D://PY/REPOSITORIES/erdogant.github.io/docs/imagesc/pypi/pypi_heatmap_repos.html'
pp.plot(path=path, vmin=10)

# %%

# import seaborn as sns
# idx= ['aaa','bbb','ccc','ddd','eee']
# cols = list('ABCD')
# df = pd.DataFrame(abs(np.random.randn(5,4)), index=idx, columns=cols)

# # _r reverses the normal order of the color map 'RdYlGn'
# sns.heatmap(dfnew, cmap='RdYlGn_r', linewidths=0.5, annot=False)
