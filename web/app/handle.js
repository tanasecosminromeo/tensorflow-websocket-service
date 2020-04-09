app.handle = {
    commandId: 0,
    lastCommand: null,
    detect: function (){
        let url = $('#streamId').val(),
            img = $('#cam');

        if (url.indexOf('.mjpg')){
            app.handle.send('detect', ['stream', url]);
        } else {
            app.handle.send('detect', ['url', url]);
        }
        
        img.attr('src', url)

    },
    send: function (action, parameters){
        switch (app.ws.readyState){
            case 0:
                console.log('ws connecting');
                break;
            case 1:
                if (typeof parameters === 'undefined'){
                    parameters = [];
                }
                
                app.handle.commandId += 1;

                let sendCommand = JSON.stringify([app.handle.commandId, action, parameters, app.handle.commandId]);
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

        app.call.getLabels();
    },
    message: function (msg) {
        app.lastMessage = JSON.parse(msg.data)
        
        let [commandId, command, status, result] = app.lastMessage;

        if (status !== "ok"){
            console.log('error', app.lastMessage);
            return;
        }

        if (command === 'ping') { //Ignore ping-pong
            return;
        }

        switch (command){
            case "detect": 
                let [detectionStatus, detectionId, detections] = result;

                if (detectionStatus !== "ok"){
                    console.log('invalid detection', detectionId);
                    return;
                }

                if ($('#streamId').val().indexOf('.mjpg')){
                    app.handle.detect();
                }

                app.call.drawImage(detections);
            break;
            case "labels": 
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