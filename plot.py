import matplotlib.pyplot as plt

def draw(arr):
	for i in arr:
		plt.plot(i[0], i[1], linewidth=2.0)
	#plt.axis([0, 6, 0, 20])
	plt.show()
