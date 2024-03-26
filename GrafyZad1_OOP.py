import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle as pltCircle
from time import time

# Klasa koła, przechouje id koła, współrzędne x, y, promień oraz metodę sprawdzającą czy dwa koła się przecinają
class Circle:
    def __init__(self, circle_Id, x, y, radius):
        self.id = circle_Id
        self.x = x
        self.y = y
        self.radius = radius
        self.center = (x, y)

    def intersects(self, other_circle):
        distance = np.sqrt(
            (self.x - other_circle.x) ** 2 + (self.y - other_circle.y) ** 2
        )
        return distance < self.radius + other_circle.radius

    def __str__(self):
        return f"\nCircle ID: {self.id}, Center: ({self.x}, {self.y}), Radius: {self.radius}\n"

# Klasa grafu kołowego, przechowuje listę kół, listę sąsiedztwa oraz metody tworzące listę sąsiedztwa, zapisujące graf do pliku oraz odczytujące graf z pliku
class CircleGraph:
    def __init__(self, circles):
        self.circles = circles
        self.adjacency_list = self.create_adjacency_list()

    # Tworzenie listy sąsiedztw
    def create_adjacency_list(self):
        adjacency_list = {}
        for circle in self.circles:
            neighbors = []
            for other_circle in self.circles:
                if circle != other_circle and circle.intersects(other_circle):
                    neighbors.append(other_circle)
            adjacency_list[circle] = neighbors
        return adjacency_list

    def show_adjacency_list(self):
        print("Lista sąsiedztwa:")
        for circle, neighbors in self.adjacency_list.items():
            print(circle, "neighbors:", [str(neighbor) for neighbor in neighbors])

    # Zapisywanie grafu do pliku z możliwością dodania komentarza
    def write_to_file(self, filename):
        print("Chcesz dodać komentarz? T/N")
        input_comment = input()
        if (input_comment == "T") or (input_comment == "t"):
            comment = input("Podaj komentarz: ")
            with open(filename, "w") as f:
                f.write(f"#{comment}\n")
                f.write(f"#Id X Y Rad\n")
                for circle in self.circles:
                    f.write(f"{circle.id} {circle.x} {circle.y} {circle.radius}\n")

    # Odczytanie grafu z pliku
    @classmethod
    def read_from_file(cls, filename):
        circles = []
        with open(filename, "r") as f:
            for line in f:
                if line.startswith("#"):
                    continue
                id, x, y, radius = map(float, line.strip().split())
                circles.append(Circle(id, x, y, radius))
        return cls(circles)

    # Dodanie nowego koła do grafu
    def add_circle(self, circle):
        self.circles.append(circle)
        self.adjacency_list = self.create_adjacency_list()

    def delete_circle_by_id(self, circle_id):
        circle_to_remove = None
        for circle in self.circles:
            if circle.id == circle_id:
                circle_to_remove = circle

        if circle_to_remove:
            if circle_to_remove in self.adjacency_list:
                del self.adjacency_list[circle_to_remove]
            else:
                print("Circle not found in the adjacency list.")
        else:
            print("Circle with ID", circle_id, "not found.")




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

class Statistics:
    TimeAdjListDefault: float
    TimeDegDefault: float
    TimeAddVertexDefault: float
    TimeAnnihilationDefault: float
    TimePotentialDefault: float
    TimeAdjListFile: float
    TimeDegFile: float
    TimeAddVertFile: float
    TimeAnnihilationFile: float
    TimePotentialFile: float
    def __init__(self):
        self.TimeAdjListDefault = 0
        self.TimeDegDefault = 0
        self.TimeAddVertexDefault = 0
        self.TimeAnnihilationDefault = 0
        self.TimePotentialDefault = 0
        self.TimeAdjListFile = 0
        self.TimeDegFile = 0
        self.TimeAddVertFile = 0
        self.TimeAnnihilationFile = 0
        self.TimePotentialFile = 0

    def set_TimeAdjListDefault(self, time):
        self.TimeAdjListDefault = time
    def set_TimeDegDefault(self, time):
        self.TimeDegDefault = time
    def set_TimeAddVertexDefault(self, time):
        self.TimeAddVertexDefault = time
    def set_TimeAnnihilationDefault(self, time):
        self.TimeAnnihilationDefault = time
    def set_TimePotentialDefault(self, time):
        self.TimePotentialDefault = time
    def set_TimeAdjListFile(self, time):
        self.TimeAdjListFile = time
    def set_TimeAddVertFile(self, time):
        self.TimeAddVertFile = time
    def set_TimeDegFile(self, time):
        self.TimeDegFile = time
    def set_TimeAnnihilationFile(self, time):
        self.TimeAnnihilationFile = time
    def set_TimePotentialFile(self, time):
        self.TimePotentialFile = time
    


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
timeStats = Statistics()
graph = Graph()
timer_start_adjList_default = time()
graph.matrix_to_list(matrix)
timer_end_adjList_default = time()

timeStats.set_TimeAdjListDefault(timer_end_adjList_default - timer_start_adjList_default)

timer_start_deg_default = time()
graph.calculate_degrees(graph.adjacency_list)
timer_end_deg_default = time()

timeStats.set_TimeDegDefault(timer_end_deg_default - timer_start_deg_default)

timer_start_anihilation_default = time()
graph.annihilation_number(graph.adjacency_list)
timer_end_anihilation_default = time()

timeStats.set_TimeAnnihilationDefault(timer_end_anihilation_default - timer_start_anihilation_default)

timer_start_potential_default = time()
graph.graph_potential()
timer_end_potential_default = time()

timeStats.set_TimePotentialDefault(timer_end_potential_default - timer_start_potential_default)

graphFile = Graph()
timer_start_adjList_File = time()
graphFile.read_snap_file("graph.snap")
timer_end_adjList_File = time()

timeStats.set_TimeAdjListFile(timer_end_adjList_File - timer_start_adjList_File)

timer_start_deg_File = time()
graphFile.calculate_degrees(graphFile.adjacency_list)
timer_end_deg_File = time()

timeStats.set_TimeDegFile(timer_end_deg_File - timer_start_deg_File)

timer_start_anihilation_File = time()
graphFile.annihilation_number(graphFile.adjacency_list)
timer_end_anihilation_File = time()

timeStats.set_TimeAnnihilationFile(timer_end_anihilation_File - timer_start_anihilation_File)

timer_start_potential_File = time()
graphFile.graph_potential()
timer_end_potential_File = time()

timeStats.set_TimePotentialFile(timer_end_potential_File - timer_start_potential_File)

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
                    timeStats.set_TimeAddVertexDefault(timer_end_addVertex - timer_start_addVertex)
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
                    print(f"Liczba anihilacji: {graph.annih_number}")
                    UI_LowLvL(int_input_graphType)
                case 9:
                    print(f"Potencjał grafu: {graph.poten}")
                    UI_LowLvL(int_input_graphType)
                case 10:
                    target_length = int(input("Podaj długość ścieżki: "))
                    timer_start_paths_default = time()
                    graph.all_dfs_paths(target_length)
                    timer_end_paths_default = time()
                    print(f"Czas wyliczania stopni wierzchołków z pliku: {timer_end_paths_default - timer_start_paths_default} s")
                    UI_LowLvL(int_input_graphType)
                case 11:
                    print(f"Czas wyliczenia listy sąsiedztwa dla grafu przykładowego: {timeStats.TimeAdjListDefault} s")
                    print(f"Czas wyliczania stopni wierzchołków: {timeStats.TimeDegDefault} s")
                    print(f"Czas dodawania wierzchołka: {timeStats.TimeAddVertexDefault} s")
                    print(f"Czas wyliczania liczby anihilacji: {timeStats.TimeAnnihilationDefault} s")
                    print(f"Czas wyliczania potencjałów wierzchołków: {timeStats.TimePotentialDefault} s")
                    UI_LowLvL(int_input_graphType)
                case 12:
                    input_file = str(input("Podaj nazwę pliku: "))
                    graph.write_snap_file(input_file)
                    print("Zapisano")
                    UI_LowLvL(int_input_graphType)
                case 13:
                    print("Zmień graf.")
                    UI_HighLvL()
        case 2:
            print("""
Wybierz akcję którą chcesz wykonać dla grafu z pliku:
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
                    UI_LowLvL(int_input_graphType)
                case 3:
                    graphFile.print_matrix(graphFile.adjacency_list)
                    UI_LowLvL(int_input_graphType)
                case 4:
                    vertex = int(input("Podaj wierzchołek do dodania: "))
                    timer_start_addVertex = time()
                    graphFile.add_vertex(vertex)
                    timer_end_addVertex = time()
                    timeStats.set_TimeAddVertFile(timer_end_addVertex - timer_start_addVertex)
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
                    print(f"Liczba anihilacji: {graphFile.annih_number}")
                    UI_LowLvL(int_input_graphType)
                case 9:
                    print(f"Potencjał grafu: {graphFile.poten}")
                    UI_LowLvL(int_input_graphType)
                case 10:
                    target_length = int(input("Podaj długość ścieżki: "))
                    timer_start_paths = time()
                    graphFile.all_dfs_paths(target_length)
                    timer_end_paths = time()
                    print(f"Czas wyliczania stopni wierzchołków z pliku: {timer_end_paths - timer_start_paths} s")
                    UI_LowLvL(int_input_graphType)
                case 11:
                    print(f"Czas wyliczenia listy sąsiedztwa dla grafu przykłądowego: {timeStats.TimeAdjListFile} s")
                    print(f"Czas wyliczania stopni wierzchołków: {timeStats.TimeDegFile} s")
                    print(f"Czas dodawania wierzchołka: {timeStats.TimeAddVertFile} s")
                    print(f"Czas wyliczania liczby anihilacji: {timeStats.TimeAnnihilationFile} s")
                    print(f"Czas wyliczania potencjałów wierzchołków: {timeStats.TimePotentialFile} s")
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
[2] Dodaj koło
[3] Usuń koło
[4] Narysuj graf
[5] Zapisz graf do pliku
[6] Zmień graf
""")
            int_input_actionType = int(input())
            match(int_input_actionType):
                case 1:
                    print(f"Lista sąsiedztwa:\n{graphCircle.show_adjacency_list()}\n")
                    UI_LowLvL(int_input_graphType)
                case 2:
                    circle_id = int(input("Podaj id koła: "))
                    x = float(input("Podaj współrzędną x: "))
                    y = float(input("Podaj współrzędną y: "))
                    radius = float(input("Podaj promień: "))
                    circle = Circle(circle_id, x, y, radius)
                    graphCircle.add_circle(circle)
                    print(f"Dodano koło o id: {circle_id}")
                    UI_LowLvL(int_input_graphType)
                case 3:
                    graphCircle.show_adjacency_list()
                    circle_id = int(input("Podaj id koła do usunięcia: "))
                    graphCircle.delete_circle_by_id(circle_id)
                    print(f"Usunięto koło o id: {circle_id}")
                    UI_LowLvL(int_input_graphType)
                case 4:
                    graphCircle.plot_circles()
                    UI_LowLvL(int_input_graphType)
                case 5:
                    input_file = str(input("Podaj nazwę pliku: "))
                    graphCircle.write_to_file(input_file)
                    print("Zapisano")
                    UI_HighLvL()
                case 6:
                    print("Zmień graf.")
                    UI_HighLvL()   
        case 4:
            print("Koniec programu.")
            exit(0)

UI_HighLvL()