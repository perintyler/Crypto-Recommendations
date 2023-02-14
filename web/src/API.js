/* API.js */

const DEVELOP = false;

const DEBUG = true;

const LOCAL_ADDRESS = 'ws://127.0.0.1:8080';

const HOSTED_ADDRESS = 'wss://crypto-order-books-376705.ue.r.appspot.com';

const WEBSOCKET_ADDRESS = DEVELOP ? LOCAL_ADDRESS : HOSTED_ADDRESS;

var websocket;

export function isWebSocketOpen()
{
    return (websocket !== undefined && websocket !== null)
        && (websocket.readyState === 0 /* open */ || websocket.readyState === 1 /* opening */);
}

export function closeWebSocket()
{
    if (isWebSocketOpen()) {
        websocket.close();
        websocket = null;
    }
}

export function openWebSocket(
    handleRecommendations, 
    handlePricePoints,
    handleError,
    onClose
)
{
    websocket = new WebSocket(WEBSOCKET_ADDRESS);

    websocket.onopen = () => {
        if (DEBUG) { console.log('opened websocket'); }
    };

    websocket.onclose = (msg) => {
        if (onClose !== null) {
            onClose(msg);
        }
    };

    websocket.onerror = (error) => {
        closeWebSocket();
        handleError(error);
    };

    websocket.onmessage = (payload) => {
        let message = JSON.parse(payload['data']);
        
        if (message.event === 'subscribed') {
            if (DEBUG) { console.log('subscribed to ' + message.exchange); }
        }

        else if (message.event === 'recommendations') {
            if (DEBUG) {
                console.log('recommendations', message.recommendations);
                console.log('prices', message.prices)
            }
            handleRecommendations(message.recommendations);
            handlePricePoints(message.prices);
        }

        else {
            console.warn('unexpected message: ', message)
        }
    };

    return websocket;
}

