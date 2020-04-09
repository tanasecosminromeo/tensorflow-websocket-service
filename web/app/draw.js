class AppDraw {
    constructor (context, label, percentage, xmin, xmax, ymin, ymax){
        let x = xmin * 640;
        let y = ymin * 480;
        let width = xmax * 640 - x;
        let height = ymax * 480 - y;

        context.beginPath();
        context.globalAlpha = 0.2;
        context.rect(x, y, width, height);
        context.fillStyle = 'red';
        context.fill();
        context.lineWidth = 7;
        context.strokeStyle = 'black';
        context.stroke();
        context.closePath();
        context.beginPath();
        context.globalAlpha = 1;
        context.fillText(label, x, y-5);
        context.fillStyle = 'red';
        context.fill();
        context.closePath();
        context.beginPath();
        context.globalAlpha = 1;
        context.fillText(percentage+'%', x+width-20, y-5);
        context.fillStyle = 'red';
        context.fill();
        context.closePath();
    }

    getColorForPercentage = function(pct) {
        let percentColors = [
            { pct: 0.0, color: { r: 0xff, g: 0x00, b: 0 } },
            { pct: 0.5, color: { r: 0xff, g: 0xff, b: 0 } },
            { pct: 1.0, color: { r: 0x00, g: 0xff, b: 0 } } ];

        for (var i = 1; i < percentColors.length - 1; i++) {
            if (pct < percentColors[i].pct) {
                break;
            }
        }
        var lower = percentColors[i - 1];
        var upper = percentColors[i];
        var range = upper.pct - lower.pct;
        var rangePct = (pct - lower.pct) / range;
        var pctLower = 1 - rangePct;
        var pctUpper = rangePct;
        var color = {
            r: Math.floor(lower.color.r * pctLower + upper.color.r * pctUpper),
            g: Math.floor(lower.color.g * pctLower + upper.color.g * pctUpper),
            b: Math.floor(lower.color.b * pctLower + upper.color.b * pctUpper)
        };
        return 'rgb(' + [color.r, color.g, color.b].join(',') + ')';
    };
}

app.draw = function (canvas, context, label, percentage, xmin, xmax, ymin, ymax){
    return new AppDraw(canvas, context, label, percentage, xmin, xmax, ymin, ymax);
}