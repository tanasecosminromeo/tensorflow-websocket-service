app.call = {
    lastDetectionId: 0,
    labels: {},
    getLabels: function (){
        app.handle.send('labels');
    },
    drawImage: function (detections){
        let canvas = document.getElementById('myCanvas');
        let context = canvas.getContext('2d');

        context.clearRect(0,0,canvas.width, canvas.height);

        for (let detection of detections){
            console.log(detection);
            let [percentage, [ymin, xmin, ymax, xmax], label] = detection;
            if (percentage < app.config.percentageLimit) continue;

            let labelName = app.call.labels[label] ? app.call.labels[label].name : 'Unknown';
            let percentageString = parseInt(percentage*100);
            app.draw(context, labelName, percentageString, xmin, xmax, ymin, ymax);
        }
    },
    saveLabels: function (labels){
        console.log('set labels to ',labels);
        app.call.labels = labels;
    }
}