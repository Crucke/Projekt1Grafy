import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle as pltCircle

## Klasa koła, przechouje współrzędne x, y, promień oraz metodę sprawdzającą czy dwa koła się przecinają
class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.center = (x, y)

    def intersects(self, other_circle):
        distance = np.sqrt(
            (self.x - other_circle.x) ** 2 + (self.y - other_circle.y) ** 2
        )
        return distance < self.radius + other_circle.radius

## Klasa grafu kołowego, przechowuje listę kół, listę sąsiedztwa oraz metody tworzące listę sąsiedztwa, zapisujące graf do pliku oraz odczytujące graf z pliku
class CircleGraph:
    def __init__(self, circles):
        self.circles = circles
        self.adjacency_list = self.create_adjacency_list()

    ##Tworzenie listy sąsiedztw
    def create_adjacency_list(self):
        adjacency_list = {i: [] for i in range(len(self.circles))}

        for i in range(len(self.circles)):
            for j in range(i + 1, len(self.circles)):
                if self.circles[i].intersects(self.circles[j]):
                    adjacency_list[i].append(j)
                    adjacency_list[j].append(i)
        return adjacency_list

    ##Zapisywanie grafu do pliku z możliwością dodania komentarza
    def write_to_file(self, filename):
        print("Chcesz dodać komentarz? T/N")
        input_comment = input()
        if (input_comment == "T") or (input_comment == "t"):
            comment = input("Podaj komentarz: ")
            with open(filename, "w") as f:
                f.write(f"#{comment}\n")
                f.write(f"#X Y Rad\n")
                for circle in self.circles:
                    f.write(f"{circle.x} {circle.y} {circle.radius}\n")
        else:
            comment = ""

    ##Odczytanie grafu z pliku
    @classmethod
    def read_from_file(cls, filename):
        circles = []
        with open(filename, "r") as f:
            for line in f:
                if line.startswith("#"):
                    continue
                x, y, radius = map(float, line.strip().split())
                circles.append(Circle(x, y, radius))
        return cls(circles)

    ##Dodanie nowego koła do grafu
    def add_circle(self, circle):
        self.circles.append(circle)
        self.adjacency_list = self.create_adjacency_list()

    ##Rysowanie grafu
    def plot_circles(self):
        fig, ax = plt.subplots()
        for circle in self.circles:
            circle_plot = plt.Circle((circle.x, circle.y), circle.radius, edgecolor='b', facecolor='none')
            ax.add_artist(circle_plot)
            ax.plot(circle.x, circle.y, 'ro')  # plot center of circle
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlim(min(circle.x - circle.radius for circle in self.circles) - 1,
                    max(circle.x + circle.radius for circle in self.circles) + 1)
        ax.set_ylim(min(circle.y - circle.radius for circle in self.circles) - 1,
                    max(circle.y + circle.radius for circle in self.circles) + 1)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Circles')
        plt.grid(True)
        plt.show()


# Odczytaj z pliku circles.txt i wypisz listę sąsiedztwa
circle_graph = CircleGraph.read_from_file("circles.txt")
print(circle_graph.adjacency_list)

# Dodaj nowe koło
print("Chcesz dodac nowe kolo? T/N")
input_circle = input()
if (input_circle == "T") or (input_circle == "t"):
    x = float(input("Podaj współrzędną x: "))
    y = float(input("Podaj współrzędną y: "))
    radius = float(input("Podaj promień: "))
    circle_graph.add_circle(Circle(x, y, radius))

# Zapis do pliku
print("Czy zapisać do pliku? T/N")
input_save = input()
if (input_save == "T") or (input_save == "t"):
    circle_graph.write_to_file("circles.txt")

# Pokazanie grafu
print("Pokazać graf? T/N")
input_showPlot = input()
if (input_showPlot == "T") or (input_showPlot == "t"):
    circle_graph.plot_circles()