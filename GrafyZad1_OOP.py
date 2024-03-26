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
        self.annih_number = 0
        self.poten = 0

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

    # Przetworzenie listy sąsiedztwa na macierz
    def list_to_matrix(self, adjacency_list=None):
        adjacency_list = adjacency_list or self.adjacency_list
        max_vertex = max(adjacency_list.keys()) if adjacency_list else 0
        num_vertex = max_vertex + 1
        matrix = [[0] * num_vertex for _ in range(num_vertex)]
        for vertex, neighbors in adjacency_list.items():
            for neighbor in neighbors:
                adjusted_neighbor = min(neighbor, max_vertex)  # Adjust neighbor index
                matrix[vertex][adjusted_neighbor] = 1
        return matrix
    
    # Wypisanie macierzy sąsiedztwa
    def print_matrix(self, adjacency_list=None):
        adjacency_list = adjacency_list or self.adjacency_list
        matrix = self.list_to_matrix(adjacency_list)
        print("Matrix representation of the graph:")
        for row in matrix:
            print(row)

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
    
    # Wyszukiwanie wszystkich ścieżek o zadanej długości
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
    
    # Wyliczanie liczby anihilacji
    def annihilation_number(self, adjacency_list=None):
        adjacency_list = adjacency_list or self.adjacency_list
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
        self.annih_number = annihilation_num
        return annihilation_num
    
    # Wyliczanie potencjału grafu
    def find_potential(self, degrees=None):
        degrees = degrees or self.degrees
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
        self.poten = self.find_potential()
        max_potential = max(self.poten.values())
        self.poten = max_potential
        return max_potential            

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
timer_start_adjList_default = time()
graph.matrix_to_list(matrix)
timer_end_adjList_default = time()

timer_start_deg_default = time()
graph.calculate_degrees(graph.adjacency_list)
timer_end_deg_default = time()

timer_start_anihilation_default = time()
graph.annihilation_number()
timer_end_anihilation_default = time()

timer_start_potential_default = time()
graph.find_potential()
timer_end_potential_default = time()


graphFile = Graph()
timer_start_adjList_File = time()
graphFile.read_snap_file("graph.snap")
timer_end_adjList_File = time()

timer_start_deg_File = time()
graphFile.calculate_degrees(graphFile.adjacency_list)
timer_end_deg_File = time()

timer_start_anihilation_File = time()
graphFile.annihilation_number(graphFile.adjacency_list)
timer_end_anihilation_File = time()

timer_start_potential_File = time()
graphFile.find_potential(graphFile.degrees)
timer_end_potential_File = time()

graphCircle = CircleGraph.read_from_file("circles.txt")

# Funkcje interfejsu użytkownika
def UI_HighLvL():
    print("""
Dla jakiego grafu chcesz wykonywać czynności?
[1] Graf przykładowy
[2] Graf z pliku SNAP
[3] Graf kołowy
[4] Wyjdź
      """)
    int_input_graphType = int(input())
    UI_LowLvL(int_input_graphType)
    return int_input_graphType

def UI_LowLvL(int_input_graphType):
    match(int_input_graphType):
        case 1:
            print("""
Wybierz akcję którą chcesz wykonać dla grafu przykładowego:
Podaj odpowiednią cyfrę:
[1] Wyświetl listę sąsiedztw
[2] Wyświetl listę stopni wierzchołków
[3] Wyświetl macierz sąsiedztwa
[4] Dodaj wierzchołek
[5] Usuń wierzchołek
[6] Dodaj krawędź
[7] Usuń krawędź
[8] Wylicz liczbę anihilacji
[9] Wylicz potencjał grafu
[10] Wylicz wszystkie ścieżki o zadanej długości
[11] Wypisz czasy operacji na grafie                  
[12] Zapisz graf do pliku
[13] Zmień graf
""")
            int_input_actionType = int(input())
            match(int_input_actionType):
                case 1:
                    print(f"Lista sąsiedztwa:\n{graph.adjacency_list}\n")
                    UI_LowLvL(int_input_graphType)
                case 2:
                    print(f"Lista stopni wierzchołków:\n{graph.degrees}\n")
                    UI_LowLvL(int_input_graphType)
                case 3:
                    graph.print_matrix(graph.adjacency_list)
                    UI_LowLvL(int_input_graphType)
                case 4:
                    vertex = int(input("Podaj wierzchołek do dodania: "))
                    timer_start_addVertex = time()
                    graph.add_vertex(vertex)
                    timer_end_addVertex = time()
                    UI_LowLvL(int_input_graphType)
                case 5:
                    vertex = int(input("Podaj wierzchołek do usunięcia: "))
                    graph.remove_vertex(vertex)
                    UI_LowLvL(int_input_graphType)
                case 6:
                    vertex1 = int(input("Podaj wierzchołek 1 dla którego chcesz stworzyć krawędź: "))
                    vertex2 = int(input("Podaj wierzchołek 2 dla którego chcesz stworzyć krawędź: "))
                    graph.add_edge(vertex1, vertex2)
                    UI_LowLvL(int_input_graphType)
                case 7:
                    vertex1 = int(input("Podaj wierzchołek 1 dla którego chcesz usunąć krawędź: "))
                    vertex2 = int(input("Podaj wierzchołek 2 dla którego chcesz usunąć krawędź: "))
                    graph.remove_edge(vertex1, vertex2)
                    UI_LowLvL(int_input_graphType)
                case 8:
                    print(f"Liczba anihilacji: {graph.annihilation_number}")
                    UI_LowLvL(int_input_graphType)
                case 9:
                    print(f"Potencjał grafu: {graph.graph_potential}")
                    UI_LowLvL(int_input_graphType)
                case 10:
                    target_length = int(input("Podaj długość ścieżki: "))
                    timer_start_paths_default = time()
                    graph.all_dfs_paths(target_length)
                    timer_end_paths_default = time()
                    print(f"Czas wyliczania stopni wierzchołków z pliku: {timer_end_paths_default - timer_start_paths_default} s")
                    UI_LowLvL(int_input_graphType)
                case 11:
                    print(f"Czas wyliczenia listy sąsiedztwa dla grafu przykłądowego: {timer_end_adjList_default - timer_start_adjList_default} s")
                    print(f"Czas wyliczania stopni wierzchołków: {timer_end_deg_default - timer_start_deg_default} s")
                    print(f"Czas dodania wierzchołka: {timer_end_addVertex - timer_start_addVertex} s")
                    print(f"Czas wyliczania liczby anihilacji: {timer_end_anihilation_default - timer_start_anihilation_default} s")
                    print(f"Czas wyliczania potencjałów wierzchołków: {timer_end_potential_default - timer_start_potential_default} s")
                    UI_LowLvL(int_input_graphType)
                case 12:
                    input_file = str(input("Podaj nazwę pliku: "))
                    graph.write_snap_file(input_file)
                    print("Zapisano")
                case 13:
                    print("Zmień graf.")
                    UI_HighLvL()
        case 2:
            print("""
Wybierz akcję którą chcesz wykonać dla grafu przykładowego:
Podaj odpowiednią cyfrę:
[1] Wyświetl listę sąsiedztw
[2] Wyświetl listę stopni wierzchołków
[3] Wyświetl macierz sąsiedztwa
[4] Dodaj wierzchołek
[5] Usuń wierzchołek
[6] Dodaj krawędź
[7] Usuń krawędź
[8] Wylicz liczbę anihilacji
[9] Wylicz potencjał grafu
[10] Wylicz wszystkie ścieżki o zadanej długości
[11] Wypisz czasy operacji na grafie  
[12] Wczytaj nowy graf z pliku           
[13] Zmień rodzaj grafu
                  """)
            int_input_actionType = int(input())
            match(int_input_actionType):
                case 1:
                    print(f"Lista sąsiedztwa:\n{graphFile.adjacency_list}\n")
                    UI_LowLvL(int_input_graphType)
                case 2:
                    print(f"Lista stopni wierzchołków:\n{graphFile.degrees}\n")
                    timer_end_deg_default = time()
                    UI_LowLvL(int_input_graphType)
                case 3:
                    graphFile.print_matrix(graphFile.adjacency_list)
                    UI_LowLvL(int_input_graphType)
                case 4:
                    vertex = int(input("Podaj wierzchołek do dodania: "))
                    timer_start_addVertex = time()
                    graphFile.add_vertex(vertex)
                    timer_end_addVertex = time()
                    UI_LowLvL(int_input_graphType)
                case 5:
                    vertex = int(input("Podaj wierzchołek do usunięcia: "))
                    graphFile.remove_vertex(vertex)
                    UI_LowLvL(int_input_graphType)
                case 6:
                    vertex1 = int(input("Podaj wierzchołek 1 dla którego chcesz stworzyć krawędź: "))
                    vertex2 = int(input("Podaj wierzchołek 2 dla którego chcesz stworzyć krawędź: "))
                    graphFile.add_edge(vertex1, vertex2)
                    UI_LowLvL(int_input_graphType)
                case 7:
                    vertex1 = int(input("Podaj wierzchołek 1 dla którego chcesz usunąć krawędź: "))
                    vertex2 = int(input("Podaj wierzchołek 2 dla którego chcesz usunąć krawędź: "))
                    graphFile.remove_edge(vertex1, vertex2)
                    UI_LowLvL(int_input_graphType)
                case 8:
                    print(f"Liczba anihilacji: {graphFile.adjacency_list}")
                    UI_LowLvL(int_input_graphType)
                case 9:
                    timer_start_potential = time()
                    print(f"Potencjał grafu: {graphFile.graph_potential}")
                    timer_end_potential = time()
                    UI_LowLvL(int_input_graphType)
                case 10:
                    target_length = int(input("Podaj długość ścieżki: "))
                    timer_start_paths = time()
                    graphFile.all_dfs_paths(target_length)
                    timer_end_paths = time()
                    UI_LowLvL(int_input_graphType)
                case 11:
                    print(f"Czas wyliczenia listy sąsiedztwa dla grafu przykłądowego: {timer_end_adjList_File - timer_start_adjList_File} s")
                    print(f"Czas wyliczania stopni wierzchołków: {timer_end_deg_File - timer_start_deg_File} s")
                    print(f"Czas wyliczania liczby anihilacji: {timer_end_anihilation_File - timer_start_anihilation_File} s")
                    print(f"Czas wyliczania potencjałów wierzchołków: {timer_end_potential_File - timer_start_potential_File} s")
                    UI_LowLvL(int_input_graphType)
                case 12:
                    input_file = str(input("Podaj nazwę pliku: "))
                    graphFile.read_snap_file(input_file)
                    graphFile.calculate_degrees()
                    UI_LowLvL(int_input_graphType)
                case 13:
                    UI_HighLvL()
        case 3:
            print("""
Wybierz akcję którą chcesz wykonać dla grafu kołowego:
Podaj odpowiednią cyfrę:
[1] Wyświetl listę sąsiedztw
[2] Wyświetl listę stopni wierzchołków
[3] Wyświetl macierz sąsiedztwa
[4] Dodaj koło
[5] Usuń koło
[6] Wylicz liczbę anihilacji
[7] Wylicz potencjał grafu
[8] Wypisz czasy operacji na grafie                  
[9] Wyjdź
""")
            int_input_actionType = int(input())
            match(int_input_actionType):
                case 1:
                    timer_start_adjList_default = time()
                    print(f"Lista sąsiedztwa:\n{graph.adjacency_list}\n")
                    timer_end_adjList_default = time()
                    UI_LowLvL(int_input_graphType)
                case 2:
                    timer_start_deg_default = time()
                    print(f"Lista stopni wierzchołków:\n{graph.degrees}\n")
                    timer_end_deg_default = time()
                    UI_LowLvL(int_input_graphType)
                case 3:
                    graph.print_matrix(graph.adjacency_list)
                    UI_LowLvL(int_input_graphType)
                case 4:
                    vertex = int(input("Podaj wierzchołek do dodania: "))
                    timer_start_addVertex = time()
                    graph.add_vertex(vertex)
                    timer_end_addVertex = time()
                    UI_LowLvL(int_input_graphType)
                case 5:
                    vertex = int(input("Podaj wierzchołek do usunięcia: "))
                    graph.remove_vertex(vertex)
                    UI_LowLvL(int_input_graphType)
                case 6:
                    vertex1 = int(input("Podaj wierzchołek 1 dla którego chcesz stworzyć krawędź: "))
                    vertex2 = int(input("Podaj wierzchołek 2 dla którego chcesz stworzyć krawędź: "))
                    graph.add_edge(vertex1, vertex2)
                    UI_LowLvL(int_input_graphType)
                case 7:
                    vertex1 = int(input("Podaj wierzchołek 1 dla którego chcesz usunąć krawędź: "))
                    vertex2 = int(input("Podaj wierzchołek 2 dla którego chcesz usunąć krawędź: "))
                    graph.remove_edge(vertex1, vertex2)
                    UI_LowLvL(int_input_graphType)
                case 8:
                    timer_start_anihilation = time()
                    print(f"Liczba anihilacji: {graph.annihilation_number}")
                    timer_end_anihilation = time()
                    UI_LowLvL(int_input_graphType)
                case 9:
                    timer_start_potential = time()
                    print(f"Potencjał grafu: {graph.graph_potential}")
                    timer_end_potential = time()
                    UI_LowLvL(int_input_graphType)
                case 10:
                    target_length = int(input("Podaj długość ścieżki: "))
                    timer_start_paths = time()
                    graph.all_dfs_paths(target_length)
                    timer_end_paths = time()
                    print(f"Czas wyliczania stopni wierzchołków z pliku: {timer_end_paths - timer_start_paths} s")
                    UI_LowLvL(int_input_graphType)
                case 11:
                    print(f"Czas wyliczenia listy sąsiedztwa dla grafu przykłądowego: {timer_end_adjList_default - timer_start_adjList_default} s")
                    print(f"Czas wyliczania stopni wierzchołków: {timer_end_deg_default - timer_start_deg_default} s")
                    print(f"Czas dodania wierzchołka: {timer_end_addVertex - timer_start_addVertex} s")
                    print(f"Czas wyliczania liczby anihilacji: {timer_end_anihilation - timer_start_anihilation} s")
                    print(f"Czas wyliczania potencjałów wierzchołków: {timer_end_potential - timer_start_potential} s")
                    UI_LowLvL(int_input_graphType)
                case 12:
                    print("Zmień graf.")
                    UI_HighLvL()   
        case 4:
            print("Koniec programu.")
            exit(0)
graphType = UI_HighLvL()