window.app = {
    latency: {},
    calculateLatency: function(command){
        let values = app.latency[command];
        let requests = Object.keys(values).length;
        totalDiff = 0;
        for (let v of Object.entries(values)){
            if (v[1][1] === -1){
                requests--;
                continue;
            }
            totalDiff += (v[1][1] - v[1][0]);
        }
    
        return totalDiff/requests;
    },
    ws: null,
    config: {
        percentageLimit: 0.2
    },
    labels: [],
    loadStream: function (){
        $('#streamId').val();
        app.ws.send('start-stream');

        setTimeout(function (){
            app.labelInterval = setInterval(function (){ 
                app.ws.send('label');
            }, 100);
        }, 5000);
    },
    //Todo: Replace with socket event in detect.py to announce detection
    pingInterval: function (){
        setInterval(function (){ 
            if (app.ws.readyState === 1){
                app.handle.send('ping');
            };
        }, 50);
    },
    connect: function (){
        let ws_path = 'ws://'+window.location.hostname+':'+WEBSOCKET_PORT+'/ws';
        app.ws = new WebSocket (ws_path);

        app.ws.onopen = app.handle.open;
        app.ws.onmessage = app.handle.message;
        app.ws.onerror = app.handle.error;
    },
    init: function () {
        if (!("WebSocket" in window)) {
            alert("WebSocket not supported");
        }
        
        app.connect();
        app.pingInterval();
    }
}

$(document).ready(app.init);
