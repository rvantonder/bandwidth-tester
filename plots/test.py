#!/usr/bin/python
import simple_plot as p
plot = p.simple_plot()
plot.new_plot(True, "Test Plot 1")
plot.add_curve_data([1, 2, 3, 4, 5], [100, 110, 90, 120, 140], "Curve 1", "Time (seconds)", "value")
plot.add_curve_data([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], "Curve 2", "Time (seconds)", "value")
plot.new_plot(False, "Test Plot 2");
plot.add_curve_data([1, 2, 3, 4, 5], [100, 110, 90, 120, 140], "Curve 1", "Time (seconds)", "value")
plot.add_curve_data([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], "Curve 2", "Time (seconds)", "value")
plot.generate_plots()
plot.save_plots("data")

