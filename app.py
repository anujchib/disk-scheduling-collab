
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
