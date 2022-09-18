##  Developer Training 

### Exppected Outcomes:
* Build a simulator to simulate the holy grail strategy of Ray Dalio, described on this video https://youtu.be/Nu4lHaSh7D4

### install
```
pip install -r requirements.txt
```

### usage:
```
python simulator.py --savefigure False
# specific correlation list
python simulator.py --correlations 10,20,30,40,50,60

# specific correlation list and risk
python simulator.py --correlations 10,20,30,40,50,60 --risk 20
```

### Example of results:
![simulator-result](simulator-holy-grail-result.png)


resource: https://dvcadmael.com/blog/the-holy-grail-dalio.html