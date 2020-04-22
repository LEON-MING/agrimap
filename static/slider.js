$(window).on('load', function() {
    console.log("loaded js");
    $("#slider").on('input',function() {
        console.log("year change!");
        $.getJSON('/data',
            { "year" : this.value },
            function (data) {
                console.log("got json");
                $("#rainfall").attr("src", data.rainfall);
                $("#temp").attr("src", data.temp);
                $("#year").html("Year: " + data.year);
            }
        );
    });
});
