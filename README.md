# Hasker
Simple clone of [Stackoverflow](https://stackoverflow.com). User can:
- create a new account/sign in
- ask a question
- create an answer
- vote for question/answer
- mark answer as correct
- change profile image

![Main screen](screenshots/main_screen.png?raw=true)
## Environment
Application requires docker and make to be installed.

## How to run server
```bash
$ git clone https://github.com/ivanpobeguts/hasker
$ cd hasker
$ make prod
```

The main page should be accessible on http://0.0.0.0:8000/ .

## Tests

```bash
$ make test
```
