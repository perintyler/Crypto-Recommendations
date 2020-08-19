import React, { Component} from "react";
import Navbar from './components/navbar.component';
import ExchangeHub from './components/exchange/exchange-hub.component';
import { Typography } from '@material-ui/core';
import { ThemeProvider } from '@material-ui/styles';
import { createMuiTheme } from '@material-ui/core/styles';
import Divider from '@material-ui/core/Divider';
import Link from '@material-ui/core/Link';

import "./App.css";
import 'fontsource-roboto';

const theme = createMuiTheme({
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"',
    ].join(','),
  },
});
// const EXCHANGES = ["Coinbase", "Bitfinex"];
const NAV_TITLE = "Tyler Perin | Chainalysis Test |";
// const NAV_ITEMS = [{
//   title: "repo",
//   link: "http://www.github.com/perintyler/chainalysis"
// }];

class App extends Component {

  render(){
    return(
      <ThemeProvider theme={theme}>
        <div className="App">
          <div id="navbar">
            <Typography id='test-title' gutterBottom variant="h2">
              Chainalysis Assignment
            </Typography>
            <div id="header-right">
              <Link underline='always' id='repo' variant="h4" href='https://github.com/perintyler/realtime-crypto'>
                git repo
              </Link>
              <Typography id='name' gutterBottom variant="h4">
                Tyler Perin
              </Typography>
            </div>
        </div>
        <Divider id='header-divider' variant="middle" />
        <ExchangeHub></ExchangeHub>
        </div>
      </ThemeProvider>
    );
  }
}

export default App;
