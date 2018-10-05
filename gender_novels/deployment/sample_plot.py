import matplotlib.pyplot as plt


X = [1795, 1803, 1812, 1815, 1816, 1830, 1844, 1846, 1860]
Y = [0.21, 0.18, 0.34, 0.35, 0.33, 0.34, 0.45, 0.65, 0.56]

fig, ax = plt.subplots()
ax.scatter(X, Y)
plt.title('Prevalence of female characters over time')
plt.xlabel('Year published')
plt.ylabel('Ratio of female to male characters')
plt.xlim(1790, 1865)
plt.ylim(0, 1)
plt.show()

#this is a really badly coded matplotlib scatter plot
#we're just using it to try putting a plot on a website
#I'll come back and make it better soon
