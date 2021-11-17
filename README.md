Plotly Dash App with Authentication
===================================

## Intro

Multipage [Plotly Dash](https://dash.plotly.com/) app with basic authentication
using [Flask-Login](https://flask-login.readthedocs.io/en/latest/)

## Usage

### Clone Repo

```bash
$ git clone https://github.com/andrespp/dash-auth.git
```

### App settings

Adjust necessary `config.ini` file, if necessary.

### Build environment

```bash
$ conda env create -f environment.yml
```

### Select app language translation (optional)

Edit `LANG` parameter on `config.ini` file.
```ini
...
;LANG=en_US.UTF-8
LANG=pt_BR.UTF-8
...
```

Generate MO files.

```bash
 $ cd locales/pt-br/LC_MESSAGES/
 $ msgfmt messages.po -o messages.mo
 $ cd -
```


### Run the app
```bash
$ conda activate dash-auth
$ python index.py
```

### Create first user
```bash
$ ./createUser.py --name John --email foo@bar.com
```
