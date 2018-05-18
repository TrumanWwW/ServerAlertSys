# run server
if ["$1"==true]
then
  	manage.py runserver -h "$1"  -p "$2"
  	echo "启动 $1:$2"
else
 	manage.py runserver -h 0.0.0.0  -p 5000
 	echo "启动 0.0.0.0:5000"
fi
