# MNTBot

**MNTBot** is a chatbot I made for the **Mutuelle Nationale Territoriale**.

## How to install

You need to have at least python 3.6. You can use pip to install the python requirements.
```bash
sudo apt-get install python3 pip
pip install -r requirements.txt
```

### Create the database and the classifier

Run these two scripts to initialize the database and create the classifier :
```bash
python train_bot_script.py  # to train the classifier  
python db_create.py  # to initialize the database
```

### Run Duckling

The date and time parsing uses Facebook's [Duckling](https://github.com/facebook/duckling) library.
It is written in Haskell, so you need to run a Haskell environment : we recommand using [stack](https://docs.haskellstack.org/en/stable/README/).
When you have downloaded or cloned the repo, `cd` into it and :
```bash
stack setup
stack build
stack exec duckling-example-exe
```
This will launch a local Duckling server on the port 8000.

### Running the back

Then you have to launch the back :
```bash
python run.py
```
The back will run on the port 5000.

### Running the chat interface

Here we have two options to run the chat interface :

#### With Slack

If you want to run the bot on [Slack](https://slack.com/), you need to create a bot account with a valid token, and then set this token as an environment variable.
You can then run the interface.
```bash
 export SLACK_BOT_TOKEN=xoxb-24767...
 python slackinterface.py
 ```
That's it ! You can talk to the bot on Slack.

#### With the custom front

You can also run the special chat interface which is built in [React](https://reactjs.org/), and uses [react-simple-chatbot](https://github.com/LucasBassetti/react-simple-chatbot).
You need to have node and npm installed, and then you can launch the front :

```bash
sudo apt-get install nodejs npm
cd reactFront
npm install
npm start
```
The React app will run on the port 3000.
You finally have to launch the middleware, which will connect your front with your back :
```bash
python runMiddleware.py
```
The middleware will run on the port 5001.
That's it ! You just have to point your browser to http://localhost:3000.

You can read the doc file for more info (in French, sorry !)
