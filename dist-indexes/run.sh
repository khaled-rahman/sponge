N=5000
K=2
Q=1500
for K in 2;
do for N in 100000;
do
echo "$N $K $Q"
python query-indexing-single-nopush.py $N $K $Q > loaddist-nopush-$K.txt
done
echo "Experiment Completed!"
done 

