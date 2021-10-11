# sgwf-gene-web
Web based workflow for sgwf

## Install
This project needs Node 12+ and Python 3.5+

### NVM install

```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash
```

Restart terminal and goes to project folder and type

```
nvm use
```

to use project node version

### Dependencies

Inside Python 3.5+ virtualenv

```
make install
```

### Create admin user
```
make admin
```

### DB migrations

```
make migrate
```

## Run

```
make run
```