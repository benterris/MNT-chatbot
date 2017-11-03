var request = require('request');




request.post(
  {url: 'http://127.0.0.1:5001/msg', form: {message: 'yololo', token: 'abcde'}},
  function (error, response, body) {
    console.log(response.statusCode);
    if (!error && response.statusCode == 200) {
            console.log(body)
        }
  }
)
