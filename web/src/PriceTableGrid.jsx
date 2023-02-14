/* PriceTableGrid.jsx */

import React from "react";
import { Typography } from '@mui/material';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import AnimatedNumbers from "react-animated-numbers";

function PriceTableBodyCell(props)
{
    return <TableCell {...props} sx={{backgroundColor: "#232b2b", color: "white", borderColor: "#F2BB05"}} align="center" />
}

function PriceTableHeaderCell(props)
{
    return <TableCell {...props} sx={{backgroundColor: "black", color: "white"}} align="center" />
}

function PriceTableHead()
{
    return (
        <TableHead>
            <TableRow sx={{backgroundColor:"black"}}>
                <PriceTableHeaderCell></PriceTableHeaderCell>
                <PriceTableHeaderCell width='120px'><b>BUY</b></PriceTableHeaderCell>
                <PriceTableHeaderCell width='120px'><b>SELL</b></PriceTableHeaderCell>
            </TableRow>
        </TableHead>
    );
}

function PriceCell({ price })
{
    const animatedPrice = <AnimatedNumbers includeComma animateToNumber={price} />;
    return (
        <PriceTableBodyCell width='120px'>
            <Box display="flex" justifyContent="center">
                <b>{ animatedPrice }</b>
            </Box>
        </PriceTableBodyCell>
    );
}

function PriceTableRow({ price_point })
{
    return (
        <TableRow>
            <PriceTableBodyCell className='symbol-cell' component="th" scope="row">
                <b>{price_point.symbol}</b>
            </PriceTableBodyCell>
            <PriceCell price={price_point.bid} />
            <PriceCell price={price_point.ask} />
        </TableRow>
    );
}

function PriceTable({ price_points })
{
    const rows = price_points.map((pp, index) => <PriceTableRow price_point={pp} key={index} />)

    return (
      <TableContainer component={Paper} sx={{backgroundColor: "#F0F0C9"}}>
        <Table>
            <PriceTableHead />
            <TableBody>{rows}</TableBody>
        </Table>
      </TableContainer>
    );
}

function PriceTableGridItem({ exchange, price_points })
{
    const exchangeTitle = exchange.charAt(0).toUpperCase() + exchange.slice(1);
    return (
        <Grid item>
            <Typography align="center" variant="h5" component="h3" style={{color:"white", paddingBottom: "10px  "}}>{exchangeTitle}</Typography>
            <PriceTable price_points={price_points} />
        </Grid>
    );
}

export default function PriceTableGrid({ prices })
{
    const gridItems = Object.keys(prices).map(
        (exchange, index) => <PriceTableGridItem exchange={exchange} price_points={prices[exchange]} key={index} />
    );

    return <Grid container spacing={5} wrap="wrap" justifyContent="space-evenly">{gridItems}</Grid>;
}

