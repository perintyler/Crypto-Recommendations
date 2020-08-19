import React from 'react';
import '../../stylesheets/exchange-hub.style.css';
import PropTypes from 'prop-types';
import ExchangeTable from './exchange-table.component';
import { Typography } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';
import Divider from '@material-ui/core/Divider';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import CardHeader from '@material-ui/core/CardHeader';

const COLORS = ['#f44336', '#673ab7', '#2196f3', '#00bcd4', '#cddc39']
/**
 * Manages websocket that provides price data to
 * exchange tables, which update upon price changes.
 */
class ExchangeHub extends React.Component {

  static propTypes = {
    exchanges: PropTypes.array,
    coins: PropTypes.array
  }

  static defaultProps = {
    exchanges: ["bitfinex", "kraken"],
    coins: ["BTC", "ETH"]
  }

  host = 'ws://0.0.0.0:8080'
  state = {recommendations: [], exchanges: {}}
  // constructor(props) {
  //   super(props);
  //   this.state = {bitfinex: [], kraken: []}
  //
  // }

  componentDidMount() { this.setup(); }
  componentWillUnmount() { this.ws.close(); }

  /*
   * Creates the websocket and adds the event listeners
   */
  setup() {
    console.log('setting up')
    this.ws = new WebSocket('ws://crypto-data-286721.uc.r.appspot.com')
    // this.ws = new WebSocket('ws:cryptodataws.herokuapp.com:80')
//https://git.heroku.com/cryptodataws.git
    // if(this.ws.readyState < 3) { return; }

    // this.close = () => { ws.close() }
    this.ws.onmessage = msg => {
      console.log('got message')
      console.log(msg)
      let data = JSON.parse(msg['data']);
      var prices = {}
      this.props.exchanges.forEach(exchange => {
        if(exchange in data) {
          prices[exchange] = data[exchange];
        }
      });
      console.log(prices)
      let recs =  data['recommendations'];
      this.setState({recommendations: recs, exchanges: prices});
      // this.setState(msg);
    }

    this.ws.onopen = () => {
      console.log('opening ws')
      // setInterval(()=>{this.setup()}, 1000);
    }

    this.ws.onclose = msg => {
      console.log('closing')
    //  setInterval(()=>{this.setup()}, 1000);
    }

    this.ws.onerror = err => {
      console.log('error')
      console.log(err)
    }

  }
  create_title(exchange) {
    return exchange.charAt(0).toUpperCase() + exchange.slice(1);
  }

  get_table(exchange) {
    var coins = this.state.exchanges[exchange];
    return <ExchangeTable exchange={exchange} coins={coins}></ExchangeTable>;
  }

  create_exchange(exchange, i) {
    console.log(exchange)
    let table = this.get_table(exchange)
    // <Exchange name={exchange} coins={this.props.coins}/>

    return (
      <Grid item key={i}>
        <Divider/>
        <Typography variant="h4" component="h3">
        {this.create_title(exchange)}
        </Typography>
        <Divider/>
        <div className='exchange-name'></div>
        {table}
      </Grid>
    );
  }

  get_exchanges() {
    return Object.keys(this.state.exchanges).map((exchange,i) => {
      return this.create_exchange(exchange, i);
    })
  }

  get_recommendations() {

    return this.state.recommendations.map((rec,i) => {
      return (
        <li key={i}>
          <Card style={{backgroundColor: COLORS[i]}}>
            <CardContent>
              <Typography style={{color: 'white'}} variant="body1">
              {i+1}. &nbsp;&nbsp; {rec}
              </Typography>
            </CardContent>
          </Card>
        </li>
      );
    })
  }
  render(){

    if(this.state.recommendations.length===0) { return <div></div> }

    return (
      <div>
        <Typography id='price-title' variant="h4">
          Realtime Best Orders
        </Typography>
        <Grid container spacing={5} wrap="wrap" justify="space-evenly">
          {this.get_exchanges()}
        </Grid>
        <Divider id="exchange-divider"></Divider>
        <Typography variant="h4">
          Recommendations
        </Typography>
        <ul id='rec-list'>
          {this.get_recommendations()}
        </ul>
      </div>
    )
    // return <ul id='exchange-hub'>{this.get_exchanges()}</ul>;
  }
}


export default ExchangeHub;
