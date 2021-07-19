:: This batch file ver2
@ECHO ON 
:: Echo on means open a windows terminal
:: Go to Root directory - Flask_React_Merged- e.g C:\Users\Dell\Desktop\Final_Project\Flask_React_Merged
cd ..
:: This actives the client
start npm start
:: This actives the server
start yarn start-api
PAUSE
:: This holds the terminal open