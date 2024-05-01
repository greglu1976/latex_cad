
делаем дамп
docker exec -t psql-confluence pg_dumpall -c -U admin > /home/greglu/confluence/dump.sql

восстанавливаем дамп
cat e:\temp\dump.sql | docker exec -i psql-confluence psql -U admin

копируем confluence
sudo cp -rv /home/greglu/confluence/confluence /media/greglu/ESD-USB