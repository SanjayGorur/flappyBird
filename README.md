# How to set up correct environment
The key issue is that tensorflow (as of writing this) has compatibility with python versions 3.5 - 3.7 while my machine was running 3.8. Hence, I made a virtual environment for this project. Code below:
```
# if not done already
brew update
brew install pyenv 
vim ~/.zshrc # add to end: eval "$(pyenv init -)"
# now for relevant stuff
pyenv install 3.7.6
cd project-dir
pyenv local 3.7.6
python3.7 -m venv env
source env/bin/activate
...
deactivate 
```
