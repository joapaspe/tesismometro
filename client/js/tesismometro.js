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
    var options = {
        start: '2015-10-23',
        end: '2015-11-15',
        dataAxis: {visible: true},
        legend: true
    };
    var graph2d = new vis.Graph2d(container, dataset, groups, options);

}