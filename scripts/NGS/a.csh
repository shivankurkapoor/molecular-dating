awk '{if($9<$4)print($4,$9,$7,$12,$13)}' OUTPUT_CHRONIC_0/final.csv.txt > reduce_chronic_0.dat
awk '{if($9<$4)print($4,$9,$7,$12,$13)}' OUTPUT_CHRONIC_0.381/final.csv.txt > reduce_chronic_0.381.dat
awk '{if($9<$4)print($4,$9,$7,$12,$13)}' OUTPUT_CHRONIC_0.71/final.csv.txt > reduce_chronic_0.71.dat
