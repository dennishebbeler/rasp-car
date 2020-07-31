import matplotlib.pyplot as plt

class SlamPlot:

    # otherwise sleep that many milliseconds between plots (eg 500)

    def __init__(self, real_lms=[]):
        super().__init__()

        fig = plt.figure(figsize=(7, 7))  # scale of window
        self.ax = fig.add_subplot(1, 1, 1)

        if len(real_lms) > 0:
            self.plot_real_landmarks(real_lms)

        r = 10
        plt.axis([-r, r, -r, r])  # range of x and y (minX,maxX,minY,maxY)
        #plt.grid(True)

        plt.draw()
        plt.pause(0.0001)

    def plot_real_landmarks(self, real_lms):
        real_lm_x = []
        real_lm_y = []

        for rlm in real_lms:
            real_lm_x.append(rlm.x)
            real_lm_y.append(rlm.y)

        self.ax.plot(real_lm_x, real_lm_y, "gx", label="echte Karte")

    def update_plot(self, obstacles: list,):
        obstacles_x = []
        obstacles_y = []

        for o in obstacles:  # get position of all particles
            obstacles_x.append(o[0])
            obstacles_y.append(o[1])


        self.ax.plot(obstacles_x, obstacles_y, "k.", label="Messungen")  # plot obstacles
        # weightDist.plot(weightD, np.ones(len(weightD)), "--y.", label="weight distrubution")
        # _,_,c = weightDist.hist( weightD, bins=np.arange(0,1.4,0.05), color="b", density=True, histtype="step", stacked=True, label="weight distrubution")

        # plt.subplots_adjust(left=0.25)
        plt.draw()  # update plot window
        plt.pause(0.001)  # whyever nessecary to update the plot

        # remove lines and patches, so they dont show up next step
        #for p in self.ax.patches:
        #    p.remove()
        #for index in range(len(self.ax.lines)):
        #    del(self.ax.lines[-1])

