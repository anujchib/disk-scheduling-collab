# Enhanced Disk Scheduling Simulator (Modified)
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation

class DiskSchedulingSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Scheduling Simulator - Visual Learning Edition")
        self.root.geometry("850x700")
        self.setup_gui()
        self.canvas = None
        self.ani = None  # Store animation reference

    def setup_gui(self):
        # Create main container frames
        left_frame = tk.Frame(self.root, padx=20, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        right_frame = tk.Frame(self.root, padx=20, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Input section in left frame
        input_frame = tk.LabelFrame(left_frame, text="Input Parameters", padx=10, pady=10)
        input_frame.pack(fill=tk.X, pady=5)

        tk.Label(input_frame, text="Enter Disk Request Sequence\n(space-separated):").pack(pady=5)
        self.request_entry = tk.Entry(input_frame, width=40)
        self.request_entry.pack(pady=5)

        tk.Label(input_frame, text="Enter Initial Head Position:").pack(pady=5)
        self.head_entry = tk.Entry(input_frame, width=20)
        self.head_entry.pack(pady=5)

        tk.Label(input_frame, text="Enter Maximum Cylinder\n(default 199):").pack(pady=5)
        self.max_cylinder_entry = tk.Entry(input_frame, width=20)
        self.max_cylinder_entry.insert(0, "199")
        self.max_cylinder_entry.pack(pady=5)

        # Algorithm selection in left frame
        algo_frame = tk.LabelFrame(left_frame, text="Algorithm Selection", padx=10, pady=10)
        algo_frame.pack(fill=tk.X, pady=5)

        self.algorithm_var = tk.IntVar(value=1)
        algorithms = ["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"]
        for i, name in enumerate(algorithms, 1):
            tk.Radiobutton(algo_frame, text=name, variable=self.algorithm_var, value=i).pack(anchor=tk.W)

        # SCAN direction in left frame
        direction_frame = tk.LabelFrame(left_frame, text="Direction", padx=10, pady=10)
        direction_frame.pack(fill=tk.X, pady=5)

        self.scan_direction_var = tk.StringVar(value="right")
        tk.Radiobutton(direction_frame, text="Right", variable=self.scan_direction_var, value="right").pack(anchor=tk.W)
        tk.Radiobutton(direction_frame, text="Left", variable=self.scan_direction_var, value="left").pack(anchor=tk.W)

        # Buttons frame
        button_frame = tk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Run button in left frame
        tk.Button(button_frame, text="Run Simulation", command=self.run_simulation, 
                 bg="#4CAF50", fg="white", padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        # Compare button in left frame
        self.compare_button = tk.Button(button_frame, text="Compare with Optimal", 
                                      command=self.show_comparison, state=tk.DISABLED,
                                      bg="#2196F3", fg="white", padx=20, pady=5)
        self.compare_button.pack(side=tk.LEFT, padx=5)

        # Results and visualization in right frame
        self.result_label = tk.Label(right_frame, text="", wraplength=600, 
                                   justify="left", font=("Arial", 11, "bold"))
        self.result_label.pack(pady=5)

        self.canvas_frame = tk.Frame(right_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Store simulation results
        self.simulation_results = None
         def fcfs(self, requests, head):
        order = [head] + requests
        return order, self.calculate_seek_time(order)

    def sstf(self, requests, head):
        requests = requests.copy()
        order = [head]
        while requests:
            closest = min(requests, key=lambda x: abs(x - head))
            requests.remove(closest)
            order.append(closest)
            head = closest
        return order, self.calculate_seek_time(order)

    def scan(self, requests, head, direction='right', max_cylinder=199):
        requests = sorted(set(requests))
        order = [head]
        if direction == 'right':
            right = [r for r in requests if r >= head]
            left = [r for r in requests if r < head]
            order += right
            if right and right[-1] != max_cylinder:
                order.append(max_cylinder)
            order += left[::-1]
        else:
            left = [r for r in requests if r <= head]
            right = [r for r in requests if r > head]
            order += left[::-1]
            if left and left[0] != 0:
                order.append(0)
            order += right
        return order, self.calculate_seek_time(order)

    def c_scan(self, requests, head, direction='right', max_cylinder=199):
        requests = sorted(set(requests))
        order = [head]
        
        if direction == 'right':
            # Move right first
            right = [r for r in requests if r >= head]
            left = [r for r in requests if r < head]
            order += right
            if right and right[-1] != max_cylinder:
                order.append(max_cylinder)
            if left:
                order.append(0)  # Jump to beginning
                order += left
        else:
            # Move left first
            left = [r for r in requests if r <= head]
            right = [r for r in requests if r > head]
            order += left[::-1]  # Reverse left requests
            if left and left[0] != 0:
                order.append(0)
            if right:
                order.append(max_cylinder)  # Jump to end
                order += right[::-1]  # Reverse right requests
                
        return order, self.calculate_seek_time(order)

    def look(self, requests, head, direction='right', max_cylinder=199):
        requests = sorted(set(requests))
        order = [head]
        
        if direction == 'right':
            # Move right first
            right = [r for r in requests if r >= head]
            left = [r for r in requests if r < head]
            order += right
            order += left[::-1]  # Reverse left requests
        else:
            # Move left first
            left = [r for r in requests if r <= head]
            right = [r for r in requests if r > head]
            order += left[::-1]  # Reverse left requests
            order += right
            
        return order, self.calculate_seek_time(order)

    def c_look(self, requests, head, direction='right', max_cylinder=199):
        requests = sorted(set(requests))
        order = [head]
        
        if direction == 'right':
            # Move right first
            right = [r for r in requests if r >= head]
            left = [r for r in requests if r < head]
            order += right
            if left:
                order += left  # Serve left requests in order
        else:
            # Move left first
            left = [r for r in requests if r <= head]
            right = [r for r in requests if r > head]
            order += left[::-1]  # Reverse left requests
            if right:
                order += right[::-1]  # Reverse right requests
                
        return order, self.calculate_seek_time(order)

    def calculate_seek_time(self, order):
        return sum(abs(order[i] - order[i - 1]) for i in range(1, len(order)))
    def visualize(self, order, title, callback=None):
        def animate(i):
            if i == 0:
                return line, head
            x = [order[i - 1], order[i]]
            y = [i - 1, i]
            line.set_data(x, y)
            head.set_data([order[i]], [i])
            return line, head

        if self.canvas:
            plt.close(self.canvas.figure)

        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor('#f4f4f8')
        ax.set_facecolor('#eef2f3')

        ax.set_xlim(0, max(order) + 20)
        ax.set_ylim(-1, len(order))
        ax.set_xlabel('Cylinder', fontsize=13, weight='bold', color='#333')
        ax.set_ylabel('Step', fontsize=13, weight='bold', color='#333')
        ax.set_title(title, fontsize=16, color="#0a58ca", weight='bold', pad=15)

        ax.invert_yaxis()
        ax.grid(True, linestyle='--', alpha=0.5)

        ax.plot(order, list(range(len(order))), color='lightblue', linestyle='--', marker='o', markersize=7, linewidth=1.5, label="Disk Path")

        line, = ax.plot([], [], 'r-', linewidth=2.5, label='Head Movement')
        head, = ax.plot([], [], marker='*', color='orange', markersize=16, label='Current Head')

        ax.legend(loc='upper right', fontsize=9)

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        ani = animation.FuncAnimation(fig, animate, frames=len(order), interval=700, repeat=False, blit=False)
        self.canvas.draw()

        if callback:
            self.root.after(len(order) * 700 + 1000, callback)

    def show_comparison(self):
        if not self.simulation_results:
            return
            
        selected_algo, best_algo, algorithms, optimal_directions, selected_result = self.simulation_results
        
        # Create figure with two subplots side by side
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        fig.patch.set_facecolor('#f4f4f8')
        
        # Get orders for both algorithms
        order1, _ = selected_result  # Use the selected result with user's direction
        order2, _ = algorithms[best_algo]  # Use the optimal result
        
        # Setup first subplot (Selected Algorithm)
        ax1.set_facecolor('#eef2f3')
        ax1.set_xlim(0, max(order1) + 20)
        ax1.set_ylim(-1, len(order1))
        ax1.set_xlabel('Cylinder', fontsize=12, weight='bold', color='#333')
        ax1.set_ylabel('Step', fontsize=12, weight='bold', color='#333')
        ax1.set_title(f"Selected: {selected_algo}", fontsize=14, color="#0a58ca", weight='bold', pad=15)
        ax1.invert_yaxis()
        ax1.grid(True, linestyle='--', alpha=0.5)
        
        # Setup second subplot (Optimal Algorithm)
        ax2.set_facecolor('#eef2f3')
        ax2.set_xlim(0, max(order2) + 20)
        ax2.set_ylim(-1, len(order2))
        ax2.set_xlabel('Cylinder', fontsize=12, weight='bold', color='#333')
        ax2.set_ylabel('Step', fontsize=12, weight='bold', color='#333')
        ax2.set_title(f"Optimal: {best_algo}", fontsize=14, color="#0a58ca", weight='bold', pad=15)
        ax2.invert_yaxis()
        ax2.grid(True, linestyle='--', alpha=0.5)
        
        # Plot the complete paths
        ax1.plot(order1, list(range(len(order1))), color='lightblue', linestyle='--', 
                marker='o', markersize=7, linewidth=1.5, label="Disk Path")
        ax2.plot(order2, list(range(len(order2))), color='lightblue', linestyle='--', 
                marker='o', markersize=7, linewidth=1.5, label="Disk Path")
        
        # Create animation lines and head markers for both plots
        line1, = ax1.plot([], [], 'r-', linewidth=2.5, label='Head Movement')
        head1, = ax1.plot([], [], marker='*', color='orange', markersize=16, label='Current Head')
        line2, = ax2.plot([], [], 'r-', linewidth=2.5, label='Head Movement')
        head2, = ax2.plot([], [], marker='*', color='orange', markersize=16, label='Current Head')
        
        # Add legends
        ax1.legend(loc='upper right', fontsize=9)
        ax2.legend(loc='upper right', fontsize=9)
        
        plt.tight_layout()
        
        def animate(i):
            if i == 0:
                # Initialize positions
                line1.set_data([], [])
                head1.set_data([], [])
                line2.set_data([], [])
                head2.set_data([], [])
                return line1, head1, line2, head2
                
            # Update first plot
            if i < len(order1):
                x1 = [order1[i - 1], order1[i]]
                y1 = [i - 1, i]
                line1.set_data(x1, y1)
                head1.set_data([order1[i]], [i])
            
            # Update second plot
            if i < len(order2):
                x2 = [order2[i - 1], order2[i]]
                y2 = [i - 1, i]
                line2.set_data(x2, y2)
                head2.set_data([order2[i]], [i])
            
            return line1, head1, line2, head2
        
        # Clear previous canvas
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
            
        # Create new canvas
        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Create animation
        self.ani = animation.FuncAnimation(fig, animate, 
                                         frames=max(len(order1), len(order2)), 
                                         interval=700, 
                                         repeat=False, 
                                         blit=True)
        
        # Store the animation to prevent garbage collection
        self.canvas.draw()
        
        # Update results label with direction information
        direction_info = ""
        if best_algo in optimal_directions:
            direction_info = f"\nOptimal Direction: {optimal_directions[best_algo].upper()}"
        
        self.result_label.config(text=f"\n\U0001F3AF Selected Algorithm: {selected_algo}\nSeek Time: {selected_result[1]} cylinders\n\n\U0001F3C6 Optimal Algorithm: {best_algo}\nSeek Time: {algorithms[best_algo][1]} cylinders{direction_info}\n\n\U0001F4DA {best_algo} was optimal here because it reduced the total movement!\n")
