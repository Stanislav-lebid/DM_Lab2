from itertools import combinations
class RouteInspectionSolver:
    def __init__(self, graph):
        self.graph = graph
        self.num_vertices = len(graph)
        self.visited = [False] * self.num_vertices

    def min_edge(self, dist, visited):
        min_distance = float('inf')
        min_index = -1
        for v in range(self.num_vertices):
            if dist[v] < min_distance and not visited[v]:
                min_distance = dist[v]
                min_index = v
        return min_index

    def dijkstra(self, src):
        dist = [float('inf')] * self.num_vertices
        dist[src] = 0

        for _ in range(self.num_vertices):
            u = self.min_edge(dist, self.visited)
            self.visited[u] = True
            for v in range(self.num_vertices):
                if (not self.visited[v]) and (self.graph[u][v] != 0) and (dist[u] + self.graph[u][v] < dist[v]):
                    dist[v] = dist[u] + self.graph[u][v]

        return dist

    def route_inspection(self):
        min_distances = []

        for src in range(0, self.num_vertices):
            dist = self.dijkstra(src)

            min_distances.append(dist)

            self.visited = [False] * self.num_vertices

        odd_vertices = []
        for i in range(0, self.num_vertices):
            neighbors = sum(
                [1 if self.graph[i][j] > 0 else 0 for j in range(0, self.num_vertices)])

            if neighbors % 2 != 0:
                odd_vertices.append(i)

        sum_of_weights = sum(graph[i][j] for i in range(
            0, self.num_vertices) for j in range(0, self.num_vertices)) // 2

        if len(odd_vertices) == 0:
            print("Початковий граф має ейлеровий цикл")

            return sum_of_weights

        odd_verices_count = len(odd_vertices)
        if len(odd_vertices) % 2 != 0:
            print("Додавання фіктивної вершини: ", self.num_vertices + 1)
            odd_verices_count += 1

        pairs = []
        for i in range(0, len(odd_vertices)):
            src = odd_vertices[i]

            for j in range(i + 1, len(odd_vertices)):
                dest = odd_vertices[j]

                pairs.append((src + 1, dest + 1, min_distances[src][dest]))

            if len(odd_vertices) % 2 != 0:
                pairs.append((src + 1, self.num_vertices + 1, 0))

        combined_pairs = combinations(pairs, odd_verices_count // 2)

        def filter_combination(combination):
            vertices = []

            for (i, j, w) in combination:
                vertices.append(i)
                vertices.append(j)

            if len(set(vertices)) != len(vertices):
                return False

            return True

        filtered_pairs = filter(filter_combination, combined_pairs)
        results = []
        for plist in filtered_pairs:
            total = sum([p[2] for p in plist])

            pItems = [p for p in plist]

            results.append((*pItems, total))

        # отримання ваги ребер які потрібно додати
        min_weight = 10**20
        result = None
        for r in results:
            if r[-1] < min_weight:
                result = r
                min_weight = r[-1]

        path = " -> ".join(
            [f"({result[p][0]}, {result[p][1]})" for p in range(0, len(result) - 1)])

        print(
            f"Мінімальна вага ребер які потрібно додати: {path} = {result[-1]}")

        print("Сума ваг усіх ребер:", sum_of_weights)

        return min_weight + sum_of_weights

if __name__ == "__main__":
    # f = open("l2-2.txt", "r")
    # f = open("l2-1.txt", "r")
    f = open("l2-3.txt", "r")
    n = int(f.readline())

    graph = []
    for i in range(0, n):
        s = [int(j) for j in f.readline().strip().split(" ")]

        graph.append(s)

    solver = RouteInspectionSolver(graph)
    min_distance = solver.route_inspection()

    print("Мінімальна відстань після обходження листоношею:",
          min_distance)
