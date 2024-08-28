import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.lines import Line2D

class DraggablePoints:
    def __init__(self, ax, initial_points):
        self.ax = ax
        self.points = []
        self.selected_point = None
        self.press = None
        self.lines = []

        # Add initial points and lines
        for (x, y) in initial_points:
            point, = ax.plot(x, y, 'ro', markersize=10)
            self.points.append(point)

        self.update_lines()

        # Connect event handlers
        self.cid_press = ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def update_lines(self):
        # Remove existing lines
        for line in self.lines:
            line.remove()
        self.lines = []

        # Add new lines connecting the points
        for i in range(len(self.points)):
            start_point = self.points[i]
            end_point = self.points[(i + 1) % len(self.points)]
            x_values = [start_point.get_data()[0][0], end_point.get_data()[0][0]]
            y_values = [start_point.get_data()[1][0], end_point.get_data()[1][0]]
            line = Line2D(x_values, y_values, color='blue')
            self.ax.add_line(line)
            self.lines.append(line)

        plt.draw()

    def on_press(self, event):
        if event.inaxes != self.ax:
            return

        for point in self.points:
            contains, _ = point.contains(event)
            if contains:
                self.selected_point = point
                self.press = (event.xdata, event.ydata)
                break

    def on_release(self, event):
        self.selected_point = None
        self.press = None
        plt.draw()

    def on_motion(self, event):
        if self.selected_point is None or self.press is None:
            return

        dx = event.xdata - self.press[0]
        dy = event.ydata - self.press[1]

        x, y = self.selected_point.get_data()
        self.selected_point.set_data([x[0] + dx], [y[0] + dy])

        self.press = (event.xdata, event.ydata)
        self.update_lines()

    def get_points(self):
        return [(point.get_data()[0][0], point.get_data()[1][0]) for point in self.points]

def draw(path_img, initial_points):
    # Assume the 4 corner points are already known
    # Example: top-left, top-right, bottom-right, bottom-left
    # initial_points =

    # Load the image
    img = mpimg.imread(path_img)

    # Create plot
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.set_xlim(0, img.shape[1])
    ax.set_ylim(img.shape[0], 0)

    # Initialize DraggablePoints with initial points
    draggable_points = DraggablePoints(ax, initial_points)

    plt.show()

    # Get coordinates of the points after the plot is closed
    coordinates = draggable_points.get_points()


# Centroid: (642.5226478830568, 357.9047337726275)
# Top-left corner: (236.0, 84.0), Bottom-right corner: (1050.0, 640.0)

# draw("your_image.jpg")