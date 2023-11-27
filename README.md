Cloud Computing and SOA Assignment
Liudmila Zhdanovich 20299, Pouyan Ghalehmalek 16500

The project is a single streamlit-hosted page that has 4 widgets: 
1) Fetches weather data for Limassol from openweathermap api
2) Fetched exchange rates for GBP, JPY and USD against EUR from exchangerates api
3) From a list in json format downloaded from openweathermap, users can select a city for which weather data will be fetched using aws api gateway and aws lambda function
4) From a list fetched from exchagerates api, users can select a currency or multiple currencies the rates of ehich against EUR will be fetched using aws api gateway and aws lambda function


Link to page: https://cloud-assignment-cei521.streamlit.app/

Additional details on the implementation:

While the first two widgets call the endpoints of the free web services directly, the 3rd and 4th widget call the API endpoints created in AWS that each have a lambda function as a resource (e.g the /weather endpoint has a query param of city and executes a lambda function calles weatherLambda which contains the python file with the funciton itself plus the packaged requests library). Each lambda needed to be imported as a .zip file as it needed the requests library to be included along with the lambda funtion definition file. They were both tested inside the editor using a mock json containing the query param that would be sent as an event and then deployed to the $default stage as there was no need for testing and prod stages. Once deployed, the APIs were created in API Gateway with the desired endpoint names and lambdas attached and then they were also deployed to the $default stage. Inside the application the newly created APIs were used in a similar way as the original endpoints with the exception that the uri and path were different as well as the lack of token in the request (it was added inside the lambda function). 
