import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

edges = [
    ("Library South", "Langdale Hall", 137),
    ("Langdale Hall", "25 Park Place", 483),
    ("25 Park Place", "55 Park Place", 644),
    ("55 Park Place", "Petit Science Center", 2897),
    ("Petit Science Center", "Aderhold", 966),
    ("Aderhold", "University Commons", 805),
    ("University Commons", "University Lofts", 483),
    ("University Lofts", "Library South", 805),
    ("25 Park Place", "Aderhold", 644),
    ("Langdale Hall", "Aderhold", 644),
]


positions = {
    "Library South": (0, 0),
    "Langdale Hall": (1, 2),
    "25 Park Place": (2, 3),
    "55 Park Place": (3, 2),
    "Petit Science Center": (4, 1),
    "University Commons": (3, 0),
    "University Lofts": (2, -1),
    "Aderhold": (1, -1)
}


class CampusNavigator:
    def __init__(self, root):
        self.root = root
        self.G = nx.Graph()

        for u, v, w in edges:
            self.G.add_edge(u, v, weight=w)

        self.setup_gui()
        self.setup_graph()

    def setup_gui(self):
        self.root.title("Campus Path Finder with Edge Weights")
        self.root.geometry("900x750")

        # Building selection
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)

        ttk.Label(control_frame, text="Start:").grid(row=0, column=0, padx=5)
        self.start_var = tk.StringVar()
        self.start_cb = ttk.Combobox(control_frame, textvariable=self.start_var,
                                     values=sorted(self.G.nodes), width=20, state="readonly")
        self.start_cb.grid(row=0, column=1, padx=5)

        ttk.Label(control_frame, text="End:").grid(row=0, column=2, padx=5)
        self.end_var = tk.StringVar()
        self.end_cb = ttk.Combobox(control_frame, textvariable=self.end_var,
                                   values=sorted(self.G.nodes), width=20, state="readonly")
        self.end_cb.grid(row=0, column=3, padx=5)

        ttk.Button(control_frame, text="Find Path", command=self.find_path).grid(row=0, column=4, padx=10)
        ttk.Button(control_frame, text="Reset", command=self.reset).grid(row=0, column=5, padx=5)

        self.status = ttk.Label(self.root, text="Select buildings and click Find Path")
        self.status.pack(pady=5)

    def setup_graph(self):
        self.fig, self.ax = plt.subplots(figsize=(9, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.draw_graph()

    def draw_graph(self, path=None):
        self.ax.clear()

        # Draw all components
        nx.draw_networkx_nodes(self.G, pos=positions, ax=self.ax,
                               node_size=800, node_color="lightblue")
        nx.draw_networkx_edges(self.G, pos=positions, ax=self.ax,
                               edge_color="gray", width=2)
        nx.draw_networkx_labels(self.G, pos=positions, ax=self.ax, font_size=10)

        # Draw edge weights - handle both (u,v) and (v,u) cases
        edge_labels = {}
        for u, v, data in self.G.edges(data=True):
            edge_labels[(u, v)] = data['weight']
            edge_labels[(v, u)] = data['weight']  # Add reverse direction

        nx.draw_networkx_edge_labels(self.G, pos=positions, ax=self.ax,
                                     edge_labels=edge_labels, font_size=8)

        # Highlight path if exists
        if path:
            path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            nx.draw_networkx_nodes(self.G, pos=positions, nodelist=path,
                                   node_color="orange", ax=self.ax, node_size=800)
            nx.draw_networkx_edges(self.G, pos=positions, edgelist=path_edges,
                                   edge_color="red", width=4, ax=self.ax)

            # Highlight path edge weights - handle both directions
            path_edge_labels = {}
            for u, v in path_edges:
                if (u, v) in edge_labels:
                    path_edge_labels[(u, v)] = edge_labels[(u, v)]
                elif (v, u) in edge_labels:
                    path_edge_labels[(v, u)] = edge_labels[(v, u)]

            nx.draw_networkx_edge_labels(self.G, pos=positions, ax=self.ax,
                                         edge_labels=path_edge_labels, font_size=8,
                                         font_color='red')

        self.ax.set_title("GSU Campus Map with Distances (meters)")
        self.ax.axis('off')
        self.canvas.draw()

    def find_path(self):
        start = self.start_var.get()
        end = self.end_var.get()

        if not start or not end:
            self.status.config(text="Please select both buildings", foreground="red")
            return

        if start == end:
            self.status.config(text="Start and end must be different", foreground="red")
            return

        try:
            path = nx.shortest_path(self.G, start, end, weight='weight')
            distance = nx.shortest_path_length(self.G, start, end, weight='weight')
            self.draw_graph(path)
            self.status.config(text=f"Path found! Distance: {distance} meters", foreground="green")
        except nx.NetworkXNoPath:
            self.status.config(text="No path exists between these buildings", foreground="red")
            self.draw_graph()

    def reset(self):
        self.start_var.set('')
        self.end_var.set('')
        self.status.config(text="Select buildings and click Find Path")
        self.draw_graph()


if __name__ == "__main__":
    root = tk.Tk()
    app = CampusNavigator(root)
    root.mainloop()
