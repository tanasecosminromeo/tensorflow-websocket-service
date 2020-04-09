app.handle = {
    commandId: 0,
    lastCommand: null,
    send: function (command, parameters){
        switch (app.ws.readyState){
            case 0:
                console.log('ws connecting');
                break;
            case 1:
                if (typeof parameters === 'undefined'){
                    parameters = [];
                }
                
                app.handle.commandId += 1;

                let sendCommand = JSON.stringify([command, parameters, app.handle.commandId]);
                app.ws.send(sendCommand)

                app.handle.lastCommand = sendCommand;
                break;
            case 2:
            case 3:
                if (app.handle.commandId > 0){
                    console.log('There was an error sending command id', app.handle.commandId, app.handle.lastCommand);
                }
                console.log('ws disconnected');
                app.connect();
                break;
        }
    },
    open: function (){
        console.log('connection on');

        app.handle.commandId = 0;
        app.handle.lastCommand = null;
    },
    handle: function (msg) {
        app.lastMessage = JSON.parse(msg.data)
        
        let [status, command, result] = app.lastMessage;

        if (status !== "ok"){
            console.log('error', app.lastMessage);
            return;
        }

        console.log('status', status);
        console.log('command', command);

        switch (command){
            case "image": 
                if (typeof app.imageInterval == 'number'){
                    clearInterval(app.imageInterval);
                }
                app.call.drawImage(result);
            break;
            case "label": 
                if (typeof app.labelInterval == 'number'){
                    clearInterval(app.labelInterval);

                    app.imageInterval = setInterval(function (){ 
                        app.ws.send('image');
                    }, 100);
                }
                app.call.saveLabels(result);
            break;
            default:
                console.log('invalid command')
            return;
        }
        
    },
    error: function (e) {
        console.log('error', e);
    }
};