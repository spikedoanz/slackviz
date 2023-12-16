# Slackviz #

![Slackviz](./assets/slackviz.png)

Convert your slack chat logs into a beautiful graph

Bootstrapped off of [Gource](https://github.com/acaudwell/Gource)

---

## Usage ##

Clone the repo
```
git clone git@github.com:spikedoanz/slackviz.git
```

Add your slack logs into slackviz/export
```
cd slackviz
mkdir export
cp -r <your slack log directory> ./export
```

Convert the log into a git repo for Gource to interpret
```
python3 main.py
```

Visualize the graph using gource, or use my config by running slackviz
```
gource repo
```

or 

```
chmod +x slackviz
./slackviz
```


