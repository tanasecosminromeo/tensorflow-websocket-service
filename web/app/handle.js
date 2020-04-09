app.handle = {
    commandId: 0,
    lastCommand: null,
    detect: function (webcamOff){
        if (webcamOff){
            let videoObj = $('#videoElement');
            videoObj[0].srcObject = null;
            $('#cam').css('display', 'block');
            videoObj.css('display', 'none');

            app.handle.webcamOn = false;
        }
        
        if (app.handle.webcamOn){
            app.handle.send('detect', ['base64', app.handle.capture()])
        } else {

                let url = $('#streamId').val(),
                img = $('#cam');

            if (url.indexOf('.mjpg')){
                app.handle.send('detect', ['stream', url]);
            } else {
                app.handle.send('detect', ['url', url]);
            }
            
            img.attr('src', url)
        }

    },
    capture: function () {
        let video = $('#videoElement')[0];
        scaleFactor = 1;

        var w = video.videoWidth * scaleFactor;
        var h = video.videoHeight * scaleFactor;
        var canvas = document.createElement('canvas');
        canvas.width  = w;
        canvas.height = h;
        var ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, w, h);
    
        return canvas.toDataURL('image/jpeg').split(',')[1]
    },
    webcam: function (){
        app.handle.webcamOn = true
        let obj = $('#videoElement'),
            video = obj[0];
        $('#cam').css('display', 'none');
        obj.css('display', 'block');

        if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                video.srcObject = stream;
                setTimeout(function (){
                    app.handle.send('detect', ['base64', app.handle.capture()])
                }, 1000);
            })
            .catch(function (err0r) {
                console.log("Something went wrong!");
            });
        }
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
                if (typeof app.latency[action] === "undefined"){
                    app.latency[action] = {}
                }
                app.latency[action][app.handle.commandId] = [new Date().getTime(), -1];
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
        app.latency[command][commandId][1] = new Date().getTime();

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