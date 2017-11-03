/*
Custom Component qui gère les requête et qui affiche le texte de la réponse du bot
*/

import React, { Component } from 'react';
var request = require('request')


class Answer extends Component {
  constructor(props){
    super(props);
    this.state = {
      message: '...',
      token: props.token,
    }
    this.displayText = this.displayText.bind(this);
    this.setOptions = this.props.setOptions
  }

  componentDidMount() {
    const self = this;
    const { steps } = this.props;
    const msg = steps.userMsg.value;



    request.post({
      url: 'http://localhost:5001/msg',
      form: { message: msg, token: this.state.token}},
      function (error, response, body) {
	      console.log('Ok requete au front, err : ' + String(error));
        if (!error && response.statusCode === 200) {
          console.log(body)
          self.setState({message: body});
          self.props.triggerNextStep();
        }
        if(error){
          console.error(error);
        }
      }
    )
  }

  // Fix pour afficher les sauts de ligne
  displayText(txt) {
      return txt.split('\n').map((item, key) => {
        return <span key={key}>{item}<br/></span>
      })
  }

  render() {
    return (
      <div align='left'>
        {
          this.displayText(this.state.message)
        }
      </div>
    )
  }
}

export default Answer;
