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

function ErrorView()
{
    return (
        <Box
          display="flex" 
          justifyContent="center" 
          alignItems="center" 
          height="75vh"
          width="100%"
        >       
            <Typography color="white">Something went wrong... Trying to reconnect.</Typography>
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

    state = { prices: null, recommendations: [], error: false };

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
        console.warn(error);
        this.setState({ error: true });
    }

    componentDidMount()
    {
        if (this.state.error == true) {
            return;
        }

        if (!isWebSocketOpen()) {
            try {
                this.connectWebSocket();
            } catch(err) {
                console.warn(err);
                this.setState({ error: true });
            }
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
        var contentView;

        if (this.state.error === true) {
            contentView = <ErrorView />;
        } else if (this.state.prices === null) {
            contentView = <LoadingView />;
        } else {
            contentView = <HomeView prices={this.state.prices} recommendations={this.state.recommendations} />
        }

        var appView = <><HeaderBar />{contentView}</>;

        return <div style={{minHeight: "100vh"}}>{ appView }</div>;
    }
}
