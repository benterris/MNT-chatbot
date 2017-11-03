/*
Component qui contient et fixe les paramètres du bot ainsi que son style
*/
import React, { Component } from 'react';
import ChatBot from 'react-simple-chatbot';
import { ThemeProvider } from 'styled-components';
import Answer from './Answer.js'


const theme = {
  background: '#fff',
  fontFamily: 'Helvetica Neue',
  headerBgColor: '#3277A6',
  headerFontColor: '#fff',
  headerFontSize: '15px',
  botBubbleColor: '#edf2ff',
  botFontColor: '#000',
  userBubbleColor: '#3277A6',
  userFontColor: '#fff',
};


class Bot extends Component {
  constructor(props) {
    super(props);
    this.state = {
      token: props.token,
      options: [{value: 1, label: '...', trigger: '1' }],
    }
  }

  render() {
    return (
      <div align="center">
          <ThemeProvider theme={theme}>
            <ChatBot
              steps={[
                {
                  id: '1',
                  message: 'Bonjour ! Je suis Albert le robot de la MNT, je peux me charger des réservations de train ou vous aider à vous connecter au VPN.',
                  trigger: 'userMsg',
                },
                {
                  id: 'userMsg',
                  user: true,
                  trigger: '3',
                },
                {
                  id: '3',
                  component: <Answer token={this.props.token} setOptions={this.setOptions}/>,
                  waitAction: true,
                  asMessage: true,
                  trigger: 'userMsg',
                }
              ]}
              botDelay = '0'
              userDelay = '0'
              customDelay = '0'
              width = '50%'
              headerTitle = 'Albert le robot'
            />
          </ThemeProvider>
      </div>
    )
  }
}

export default Bot;
