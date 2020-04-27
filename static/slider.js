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
                $("#crop").attr("src", data.crop);
                $("#year").html(data.year);
                $("#year-text").html("Year: " + data.year);
            }
        );
    });
});
