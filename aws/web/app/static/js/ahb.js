$(document).ready(function(){
// $(window).load( function(){
    var jdata = JSON.parse($('#jdata').html()); 
    
    var d1 =  JSON.parse($('#d1data').html());// '{{ date1 }}';
    var d2 =  JSON.parse($('#d2data').html());// '{{ date2 }}';
	
    var mychart = c3.generate({
     bindto: '#mychart',
     data: {
         x: 'date',
         json: jdata
     },
     axis: {
             x: {
                 type: 'timeseries',
                 tick: {
                        format: "%Y-%m",
                        count: 10,
                    },
                 label: 'Submission Date',
             },
             y: {
                 label: "# H-1B",
                 tick: {
                     format: d3.format("s")
                 }
             }
         },
             regions: [
                {start: new Date(d1), end: new Date(d2), class: 'regionY'}
            ]
    });

    var samplechart = c3.generate({
        bindto: '#samplechart',
        data: {
            x: 'x',
            columns: [
                ['x', '2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04', '2013-01-05', '2013-01-06'],
                ['data1', 30, 200, 100, 400, 150, 250],
                ['data2', 130, 340, 200, 500, 250, 350]
            ]
        },
        axis: {
            x: {
                type: 'timeseries',
                tick: {
                    format: '%Y-%m-%d'
                }
            }
        }
    });
    
    $(window).resize();
	
});
	