#!/bin/sh
f=6
while [ "$f" -lt 10 ] 
do 
	
	echo "Enter Operation 1:Add,2:Sub,3:Mul,4:Div,5:Modulus,0:exiting the calculator  "
	read Op
	var=-1
	if [ $Op -ne 0 ]
	then
	echo "Enter Number 1:  "
	read a;
	echo "Enter Number 2:  "
	read b;
	fi
	
	case $Op in
	0)f=11;;
	1) c=`echo $a + $b | bc`
	   echo "Answers of $a + $b is : $c" ;;

	2) c=`echo $a - $b | bc` 
		echo "Answers of $a - $b is : $c" ;;
	3) c=`echo $a \* $b | bc` 
		echo "Answer of $a \* $b   is : $c" ;;
	4) c=`echo "scale=2; $a / $b"  | bc ` 
		echo "Answers of $a / $b is : $c" ;;
	5) c=`expr $a % $b` 
		echo "Answers of $a % $b is : $c" ;;
	*) echo "INVALID INPUT!" ;;
	esac
	
done	


