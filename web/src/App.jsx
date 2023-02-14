/* App.jsx */

import React, { Component} from "react";
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import HeaderBar from './HeaderBar';
import PriceTableGrid from './PriceTableGrid';
import RecommendationList from './RecommendationList'
import { isWebSocketOpen, openWebSocket, closeWebSocket } from './API';

function LoadingView()
{
    return (
        <Box
          display="flex" 
          justifyContent="center" 
          alignItems="center" 
          height="75vh"
          width="100%"
          flexDirection="column"
        >
            <CircularProgress size="100px" />
            <Typography color="white" paddingTop={4}>Waiting for Bitfinex/Kraken...</Typography>
        </Box>
    );
}

function HomeView({ prices, recommendations })
{
    return (
        <Box>
            <Box 
              paddingTop="30px" 
              paddingBottom="50px" 
              backgroundColor="#0e1111" 
              borderBottom={1} 
              borderColor="#7F0799" 
              children={<PriceTableGrid prices={prices} />} 
            />
            <Box 
              paddingTop={1}
              paddingLeft={3}
              paddingRight={3}
              borderBottom={1} 
              borderColor="#7F0799" 
              children={<RecommendationList recommendations={recommendations} />} 
            />
        </Box>
    );
}

export default class App extends Component {

    state = { prices: null, recommendations: [] };

    connectWebSocket()
    {
        const handleRecommendations = (recs)   => this.setState({recommendations: recs});
        const handlePricePoints     = (prices) => this.setState({prices: prices});
        const onClose               = ()       => this.connectWebSocket();
        const onError               = (error)  => this.handleError(error);
        openWebSocket(handleRecommendations, handlePricePoints, onError, onClose);
    }

    handleError(error)
    {
        this.connectWebSocket()
    }

    componentDidMount()
    {
        if (!isWebSocketOpen()) {
            this.connectWebSocket();
        }
    }

    componentWillUnmount()
    {
        if (isWebSocketOpen()) {
            closeWebSocket();
        }
    }

    render()
    {
        const homeView = (
            <HomeView 
              prices={this.state.prices} 
              recommendations={this.state.recommendations} 
            />
        );

        return (
            <div style={{minHeight: "100vh"}}>
                <HeaderBar />
                {this.state.prices === null ? <LoadingView /> : homeView}
            </div>
        );
    }
}
