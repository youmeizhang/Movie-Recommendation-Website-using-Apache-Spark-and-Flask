## Movie Recommendation Website using Apache Spark and Flask

* Usage
  * Spark
  * Flask
  * CherryPy
  * Bootstrap
  * Jinja
  * HTML
  * CSS
  * BeautifulSoup
  
### Quick Start
Models can be trained first by running **preprocessing.ipynb** and save the models. For creating the SQLite database for storing username and password, run **tabledef.py** first and then **dummy.py** for dummy username.
After running **server.py**, you can check the website on http://0.0.0.0:5432 and see the results. The movie posters are obtained by web crawling [this website](https://www.imdb.com) 
using **BeautifulSoup**.

```C++
git clone https://github.com/youmeizhang/Movie-Recommendation-Website-using-Apache-Spark-and-Flask.git

cd /Desktop/Movie-Recommendation-Website-using-Apache-Spark-and-Flask
/usr/local/spark/bin/spark-submit server.py
```
### Some Snapshots
<img width="50%" height="50%" alt="portfolio_view" 
src="https://github.com/youmeizhang/Data-Analysis-and-Machine-Learning/blob/master/Airbnb%20Toronto/airbnb.png">

credit to: [Jose A Dianes](https://github.com/jadianes/spark-movie-lens)




