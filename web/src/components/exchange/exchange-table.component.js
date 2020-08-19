import React from 'react';
import '../../stylesheets/exchange-table.style.css';
import PropTypes from 'prop-types';
import { Typography } from '@material-ui/core';

import { withStyles } from "@material-ui/core/styles";
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import { useTheme } from '@material-ui/core/styles';

const COLORS = ['#e91e63', '#673ab7', '#2196f3', '#00bcd4', '#cddc39']

class ExchangeTable extends React.Component {

  static propTypes = {
    exchange: PropTypes.string.isRequired,
    coins: PropTypes.array.isRequired,
  }

  get_header() {
    var headers = this.props.coins.map(coin => <th>{coin.symbol}</th>);
    return <tr>{ headers }</tr>;
  }

  get_row(isBuyRow = true) {
    let rowHeader = <th> { isBuyRow ? 'Buy' : 'Sell' } </th>;
    let priceDataCells = this.props.coins.map(coin => {
      return <td> { isBuyRow ? coin.bid : coin.ask } </td>;
    });
    return (
      <tr>
        { rowHeader }
        { priceDataCells }
      </tr>
    );
  }

  get_exchange_title(exchange) {
    let title = exchange.charAt(0).toUpperCase() + exchange.slice(1);
    return <Typography variant="h5" component="h2">{title}</Typography>;
  }

  get_buy_row()  { return this.get_row(true);  }
  get_sell_row() { return this.get_row(false); }

  render(){
    var formatValue = value => value.toFixed(0);// sets the amount of decimals

    // const theme = useTheme();
  	return (
      <div>
      <TableContainer component={Paper}>
        <Table style={{backgroundColor: '#ff7043'}} className='exchange-table' aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>
            </TableCell>
            <TableCell width='120px' align="right"><b>BUY</b></TableCell>
            <TableCell width='120px' align="right"><b>SELL</b></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {this.props.coins.map((coin,i) => (
            <TableRow key={i}>
              <TableCell className='symbol-cell' component="th" scope="row">
                <b>{coin.symbol}</b>
              </TableCell>
              <TableCell width='120px' align="right">{coin.bid}</TableCell>
              <TableCell width='120px' align="right">{coin.ask}</TableCell>
            </TableRow>
          ))}
        </TableBody>
        </Table>
      </TableContainer>
      </div>
  	);
  }
}

export default ExchangeTable;
