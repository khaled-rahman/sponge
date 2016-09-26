reset
set terminal postscript enhanced color 20
set output 'load-distribution.eps'
set title "Load distribution to different nodes"
set xlabel 'Node'
set ylabel 'Load'



plot './loaddist.txt' u 3:7 title 'replica node' w lp lw 6, \
	 './loaddist.txt' u 3:11 title 'content node' w lp lw 6	
