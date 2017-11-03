import React, { Component } from 'react';
import './App.css';
import Bot from './Bot.js'
var crypto = require('crypto')


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {token: 'loading...'};
  }

  componentWillMount() {
    crypto.randomBytes(48, (err, buffer) => {
      this.setState({token: buffer.toString('hex')})
      console.log('Token generated');
    });
  }


  render() {
    if(this.state.token === 'loading...'){
      return (
        <p>Loading...</p>
      )
    }
    else {
      return (
          <div className="App">
            <header className="App-header"></header>
            <Bot token={this.state.token} />
            <footer className="App-footer"></footer>
          </div>
      );
    }
  }
}




export default App;
