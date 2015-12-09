console.log("Tesismometro")


function draw_chart_words(draw_data) {
    var container = document.getElementById('visualization');
    console.log(draw_data);
    var dataset = new vis.DataSet();
    var groups = new vis.DataSet();

    for(doctor in draw_data) {
        var values = draw_data[doctor];
        groups.add({
            id:doctor,
            content:doctor
        });
        for (var r in values) {
            dataset.add({
                x: values[r][0],
                y: values[r][1],
                group: doctor
            });
        }
    }
    var today = new Date();
    var tomorrow = new Date();
    tomorrow.setDate(today.getDate()+1);
    var options = {
        start: '2015-10-23',
        end: tomorrow,
        dataAxis: {visible: true},
        legend: true
    };
    var graph2d = new vis.Graph2d(container, dataset, groups, options);

}


function draw_hist_words(difs, dates, field) {
    var container = document.getElementById('visualization');
    console.log(difs);


    var items = [];
    var groups = new vis.DataSet();
    groups.add(
        {
            id:0
        }
    );
    groups.add(
        {
            id:1
        }
    );
    for (var i in difs) {
        var group = difs[i][field] < 0? 0: 1;
        items.push({x:dates[i],
            y:difs[i][field],
            group: group
        });
    }

    var dataset = new vis.DataSet(items);
    var today = new Date();
    var tomorrow = new Date();
    tomorrow.setDate(today.getDate()+1);
    var options = {
        start: '2015-10-23',
        end: tomorrow,
        dataAxis: {visible: true},
        style: 'bar',
        //legend: true
    };
    var graph2d = new vis.Graph2d(container, dataset, groups, options);

}