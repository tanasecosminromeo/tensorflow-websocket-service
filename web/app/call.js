app.call = {
    lastDetectionId: 0,
    drawImage: function (result){
        [detectionId, detections] = result;

        setTimeout(function (){ app.ws.send('image'); }, 100);
        if (detectionId <= app.call.lastDetectionId){
            return;
        }
        app.call.lastDetectionId = detectionId;
        console.log('detectionId', detectionId);
        console.log('detections', detections);


        let canvas = document.getElementById('myCanvas');
        let context = canvas.getContext('2d');

        context.clearRect(0,0,canvas.width, canvas.height);

        for (let detection of detections){
            let [percentage, [ymin, xmin, ymax, xmax], label] = detection
            if (percentage < app.config.percentageLimit) continue;

            let labelName = app.call.labels[label] ? app.call.labels[label].name : 'Unknown';
            let percentageString = parseInt(percentage*100);
            app.draw(canvas, context, labelName, percentageString, xmin, xmax, ymin, ymax);
        }
    },
    saveLabels: function (labels){
        console.log('set labels to ',labels);
        app.call.labels = labels;
    }
}