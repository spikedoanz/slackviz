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

Add your slack logs into slackviz/export, and one to store the generated git repo
```
cd slackviz
mkdir export
cp -r <your slack log directory> ./export
mkdir repo
```

Convert the log into a git repo for Gource to interpret
```
python3 main.py
```

Install [Gource](https://github.com/acaudwell/Gource) as per your distribution requirements, For Ubuntu-based linux:
```
sudo apt install gource
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


