# Gnuplot script file for plotting data in file "force.dat"
      # This file is called   force.p
      set   autoscale                        # scale axes automatically
      set terminal postscript enhanced color 20
      set output 'nkoutput.eps'
      unset log                              # remove any log-scaling
      unset label                            # remove any previous labels
      set xtic auto                          # set xtics automatically
      set ytic auto                          # set ytics automatically
      set title "Overhead Calculation for k=1,2,3"
      set xlabel "# of objects"
      set ylabel "overhead (KB)"
      set xr [1000:11000]
      set yr [0:150000]
      plot    "nk1" using 1:2 title 'k=1' with linespoints lw 6 , \
            "nk2" using 1:2 title 'k=2' with linespoints lw 6 , \
	    "nk3" using 1:2 title 'k=3' with linespoints lw 6	
