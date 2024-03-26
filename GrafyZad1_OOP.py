import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle as pltCircle
from time import time

# Klasa koła, przechouje współrzędne x, y, promień oraz metodę sprawdzającą czy dwa koła się przecinają
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

# Klasa grafu kołowego, przechowuje listę kół, listę sąsiedztwa oraz metody tworzące listę sąsiedztwa, zapisujące graf do pliku oraz odczytujące graf z pliku
class CircleGraph:
    def __init__(self, circles):
        self.circles = circles
        self.adjacency_list = self.create_adjacency_list()

    # Tworzenie listy sąsiedztw
    def create_adjacency_list(self):
        adjacency_list = {i: [] for i in range(len(self.circles))}

        for i in range(len(self.circles)):
            for j in range(i + 1, len(self.circles)):
                if self.circles[i].intersects(self.circles[j]):
                    adjacency_list[i].append(j)
                    adjacency_list[j].append(i)
        return adjacency_list

    # Zapisywanie grafu do pliku z możliwością dodania komentarza
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

    # Odczytanie grafu z pliku
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

    # Dodanie nowego koła do grafu
    def add_circle(self, circle):
        self.circles.append(circle)
        self.adjacency_list = self.create_adjacency_list()

    # Rysowanie grafu
    def plot_circles(self):
        fig, ax = plt.subplots()
        for circle in self.circles:
            circle_plot = plt.Circle((circle.x, circle.y), circle.radius, edgecolor='b', facecolor='none')
            ax.add_artist(circle_plot)
            ax.plot(circle.x, circle.y, 'ro')
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

# Klasa Grafu
class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.degrees = {}

    # Przetworzenie macierzy na listę sąsiedztwa
    def matrix_to_list(self, matrix):
        self.adjacency_list = {}
        self.degrees = {}
        for i in range(len(matrix)):
            neighbors = []
            degree = 0
            for j in range(len(matrix[i])):
                if matrix[i][j] == 1:
                    neighbors.append(j)
                    degree += 1
            self.adjacency_list[i] = neighbors
            self.degrees[i] = degree
        # print(f"Lista sąsiedztwa z macierzy:\n{self.adjacency_list}")
        # print(f"Lista stopni wierzchołków z macierzy:\n{self.degrees}\n")

    # Przetworzenie listy sąsiedztwa na macierz
    def list_to_matrix(self):
        num_vertex = len(self.adjacency_list)
        matrix = [[0] * num_vertex for _ in range(num_vertex)]
        for vertex, neighbors in self.adjacency_list.items():
            for neighbor in neighbors:
                matrix[vertex][neighbor] = 1
        return matrix

    # Dodanie krawędzi do listy sąsiedztwa
    def add_edge(self, vertex1, vertex2):
        if vertex1 in self.adjacency_list and vertex2 in self.adjacency_list[vertex1]:
            print("Krawędź już istnieje.")
        else:
            if vertex1 not in self.adjacency_list:
                self.add_vertex(vertex1)
                self.degrees[vertex1] = 0
            self.adjacency_list[vertex1].append(vertex2)
            if vertex2 not in self.adjacency_list:
                self.add_vertex(vertex2)
                self.degrees[vertex2] = 0
            self.adjacency_list[vertex2].append(vertex1)
            self.degrees[vertex1] += 1
            self.degrees[vertex2] += 1

    # Usunięcie krawędzi z listy sąsiedztwa
    def remove_edge(self, vertex1, vertex2):
        if vertex1 in self.adjacency_list and vertex2 in self.adjacency_list[vertex1]:
            self.adjacency_list[vertex1].remove(vertex2)
        if vertex2 in self.adjacency_list and vertex1 in self.adjacency_list[vertex2]:
            self.adjacency_list[vertex2].remove(vertex1)

    # Dodanie wierzchołka do listy sąsiedztwa
    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
            self.degrees[vertex] = 0
        else:
            print("Wierzchołek już istnieje.")

    # Usunięcie wierzchołka z listy sąsiedztwa
    def remove_vertex(self, vertex):
        if vertex in self.adjacency_list:
            del self.adjacency_list[vertex]
            for neighbors in self.adjacency_list.values():
                if vertex in neighbors:
                    neighbors.remove(vertex)

    # Odczyt z pliku SNAP
    def read_snap_file(self, filename):
        try:
            with open(filename, "r") as file:
                for line in file:
                    if line.startswith("#"):
                        continue
                    vertexs = line.strip().split()
                    vertex1 = int(vertexs[0])
                    vertex2 = int(vertexs[1])
                    if vertex1 not in self.adjacency_list:
                        self.add_vertex(vertex1)
                    if vertex2 not in self.adjacency_list:
                        self.add_vertex(vertex2)
                    if vertex2 not in self.adjacency_list[vertex1]:
                        self.adjacency_list[vertex1].append(vertex2)
                    if vertex1 not in self.adjacency_list[vertex2]:
                        self.adjacency_list[vertex2].append(vertex1)
            print("Czy wyświetlić listę sąsiedztw? T/N")
            input_show = input()
            if (input_show == "T") or (input_show == "t"):
                print(f"Lista sąsiedztwa z pliku:\n{self.adjacency_list}\n")
        except FileNotFoundError:
            print(f"Plik {filename} nie został znaleziony.")

    # Zapis do pliku w formacie SNAP
    def write_snap_file(self, filename):
        with open(filename, "w") as file:
            for vertex, neighbors in self.adjacency_list.items():
                for neighbor in neighbors:
                    file.write(f"{vertex}\t{neighbor}\n")
        file.close()
        print(f"Lista sąsiedztw zapisana do pliku o nazwie {filename}\n")
    
    # Obliczanie stopni wierzchołków
    def calculate_degrees(self, adjacency_list=None):
        if adjacency_list is None:
            adjacency_list = self.adjacency_list
        self.degrees = {}
        for vertex, neighbors in adjacency_list.items():
            self.degrees[vertex] = len(neighbors)
        print("Czy wyświetlić stopnie wierzchołków? T/N")
        input_show = input()
        if (input_show == "T") or (input_show == "t"):
            print(f"Stopnie wierzchołków: {self.degrees}")
    
    # Wyliczanie wszystkich ścieżek o zadanej długości
    def dfs_paths(self, start_vertex, path=[], path_length=0, target_length=3):
        path.append(start_vertex)
        paths = []
        if path_length == target_length:
            paths.append(path.copy())
        for neighbor in self.adjacency_list[start_vertex]:
            if neighbor not in path:
                paths.extend(
                    self.dfs_paths(neighbor, path, path_length + 1, target_length)
                )
        path.pop()
        return paths

    def all_dfs_paths(self, target_length=3):
        all_paths = []
        total_count = 0
        for start_vertex in self.adjacency_list:
            paths = self.dfs_paths(start_vertex, target_length=target_length)
            total_count += len(paths)
            all_paths.extend(paths)
        print(f"Całkowita liczba ścieżek {target_length}: {total_count/2}")
        return all_paths

    def annihilation_number(self):
        # Wyznaczanie stopnia wierzchołków
        degrees = [len(neighbors) for neighbors in self.adjacency_list.values()]

        # Sortowanie stopni wierzchołków w kolejności rosnącej
        degrees.sort()

        # Wylicz ilość krawędzi w grafie
        num_edges = (
            sum(len(neighbors) for neighbors in self.adjacency_list.values()) // 2
        )

        annihilation_num = 0
        # Zsumuj stopnie wierzchołków, aż suma przekroczy ilość krawędzi
        for degree in degrees:
            annihilation_num += degree
            if annihilation_num >= num_edges:
                return min(annihilation_num, num_edges)
        return annihilation_num

    def find_potential(self):
        potentials = {}
        for v,degree in self.degrees.items():  # Loop through vertices and their degrees
            potential = 0
            for i in range(
                1, degree + 1
            ):  # Check degrees from 1 to the degree of the vertex
                if i <= degree:  # If the degree is greater than or equal to the index
                    potential = i  # Update the potential
                else:
                    break  # Break the loop if the condition is not met
            potentials[v] = potential  # Store the potential for the vertex
        return potentials

    def graph_potential(self):
        potentials = self.find_potential()
        return max(potentials.values())            

# Przykładowa macierz:
matrix = [
    [0, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 0, 0],
    [1, 1, 0, 1, 1, 0],
    [1, 1, 1, 0, 1, 1],
    [1, 0, 1, 1, 0, 1],
    [1, 0, 0, 1, 1, 0],
]

# Utworzenie obiektu grafu
graph = Graph()

# Przekształcenie macierzy na listę sąsiedztwa
graph.matrix_to_list(matrix)
graph.calculate_degrees()

# Zapisanie grafu do pliku w formacie SNAP
# graph.write_snap_file("graph.snap")

# Odczytanie grafu z pliku w formacie SNAP
timer_start_readFile = time()
adj_list_file = graph.read_snap_file("facebook_combined.txt")
timer_end_readFile = time()

timer_start_degFile = time()
graph.calculate_degrees(adj_list_file)
timer_end_degFile = time()
# Dodania krawędzi i wierzchołków do listy sąsiedztwa
# graph.add_vertex(6)
# graph.add_vertex(7)
# graph.add_edge(6, 7)
# print(f"Lista sąsiedztwa:\n{graph.adjacency_list}\n")

# Wylicz długość wszystkich ścieżek o wskazanej długości
target_length = 3 
time_start_findPaths = time()
# graph.all_dfs_paths(target_length)
time_end_findPaths = time()

# Wyliczanie liczby anihilacji grafu
time_start_annihilation = time()
annihilation_number = graph.annihilation_number()
time_end_annihilation = time()


# Wyznaczanie potencjałów wierzchołków
timer_start_potential = time()
vertex_potentials = graph.find_potential()
timer_end_potential = time()
print(f"Potencjały wierzchołków: {vertex_potentials}")

# Wyznaczanie potencjału grafu
graph_potential = graph.graph_potential()
print(f"Potencjał grafu: {graph_potential}")

# Odczytaj z pliku circles.txt i wypisz listę sąsiedztwa
circle_graph = CircleGraph.read_from_file("circles.txt")
print(f"Lista sąsiedztw grafu kołowego:\n{circle_graph.adjacency_list}\n")

def UI():
    print("""
Czy chcesz wykonać jakąś czynność?
Podaj odpowiednią cyfrę:
[1] Wyświetlić liczbę anihilacji
[2] Wyświetlić potencjał grafu
[3] Wyliczyć ilość ścieżek
[4] Dodanie nowego koła do grafu kołowego
[5] Zapis do pliku grafu kołowego
[6] Wyliczanie stopni wierzchołków grafu kołowego
[7] Pokazanie grafu kołowego
[8] Pokazanie czasów wykonania
[9] Wyjście
      """)
    int_input = int(input())

    match(int_input):
        case 1:
            print(f"Liczba anihilacji: {annihilation_number}")
            UI()
        case 2:
            print(f"Potencjał grafu: {graph_potential}")
            UI()
        case 3:
            print("TO DO")
            # target_length = int(input("Podaj długość ścieżki: "))
            # print(f"Całkowita liczba ścieżek {target_length}: {len(graph.all_dfs_paths(target_length))/2}")
            UI()
        case 4:
            x = float(input("Podaj współrzędną x: "))
            y = float(input("Podaj współrzędną y: "))
            radius = float(input("Podaj promień: "))
            circle_graph.add_circle(Circle(x, y, radius))
            UI()
        case 5:
            circle_graph.write_to_file("circles.txt")
            UI()
        case 6:
            graph.calculate_degrees(circle_graph.adjacency_list)
            UI()
        case 7:
            circle_graph.plot_circles()
            UI()
        case 8:
            print(f"Czas odczytu pliku: {timer_end_readFile - timer_start_readFile} s")
            print(f"Czas wyliczania ścieżek: {time_end_findPaths - time_start_findPaths} s")
            print(f"Czas wyliczania liczby anihilacji: {time_end_annihilation - time_start_annihilation} s")
            print(f"Czas wyliczania potencjałów wierzchołków: {timer_end_potential - timer_start_potential} s")
            print(f"Czas wyliczania stopni wierzchołków z pliku: {timer_end_degFile - timer_start_degFile} s")
            UI()
        case 9:
            print("Exiting")

UI()